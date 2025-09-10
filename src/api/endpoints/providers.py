import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from google.api_core import exceptions as gcloud_exc
from google.cloud import secretmanager
from google.oauth2 import service_account

from core.settings import settings
from core.utils import require_api_key
from schemas.providers import GenerateUrlSchema

router = APIRouter()

# Define API Key security for OpenAPI documentation
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


@router.post("/generate_url", response_model=GenerateUrlSchema)
async def generate_url(
    client_id: int,
    provider: str,
    request: Request,
    api_key: str = Security(api_key_header),
    _: str = Depends(require_api_key),
):
    """
    Generate authentication URL and store it in Google Secret Manager.
    """
    try:
        # Validate provider
        provider = str(provider).strip().lower()
        if not provider:
            raise HTTPException(
                status_code=400, detail="'provider' must be a non-empty string"
            )

        # Load credentials from key.json file
        # key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "key.json")
        # key_path = "key.json"

        try:
            # with open(key_path, "r") as key_file:
            #     key_data = json.load(key_file)

            # credentials = service_account.Credentials.from_service_account_info(
            #     key_data
            # )
            # PROJECT_ID = key_data.get("project_id")
            PROJECT_ID = settings.PROJECT_ID

            if not settings.PROJECT_ID:
                raise HTTPException(
                    status_code=500, detail="project_id not found in key.json"
                )

        except FileNotFoundError:
            raise HTTPException(
                status_code=500, detail="key.json file not found in project root"
            )
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON in key.json file")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading credentials: {str(e)}"
            )

        url = f"https://celestial-gecko-449316-d2.uc.r.appspot.com/auth/{provider}/start?client_id={client_id}"
        secret_id = f"auth_url_{client_id}"
        secret_path = f"projects/{PROJECT_ID}/secrets/{secret_id}"
        version_path = f"{secret_path}/versions/latest"

        # sm_client = secretmanager.SecretManagerServiceClient(credentials=credentials)
        sm_client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{PROJECT_ID}"

        # 1) Intentar leer el secreto
        try:
            secret = sm_client.get_secret(request={"name": secret_path})
            # Si existe, devolver URL vigente y cuánto le queda
            expire_time = getattr(secret, "expire_time", None)
            remaining_seconds = None

            if expire_time:
                try:
                    expire_dt = expire_time.ToDatetime()
                except AttributeError:
                    expire_dt = expire_time
            if getattr(expire_dt, "tzinfo", None) is not None:
                expire_dt = expire_dt.replace(tzinfo=None)

            now_minus_6 = datetime.now() - timedelta(hours=6)
            remaining_seconds = max(0, int((expire_dt - now_minus_6).total_seconds()))

            resp = sm_client.access_secret_version(request={"name": version_path})
            current_url = resp.payload.data.decode("utf-8")

            return GenerateUrlSchema(
                status="exists",
                message="URL vigente en Secret Manager, no se modifica.",
                secret_id=secret_id,
                url=current_url,
                expires_in_seconds=remaining_seconds,
            )

        except gcloud_exc.NotFound:
            # 2) Crear el secreto con TTL de 7 días (604800 segundos)
            secret = {
                "replication": {"automatic": {}},
                "ttl": {"seconds": 604800},  # 7 días
                "labels": {"type": "auth_url", "provider": provider},
            }
            sm_client.create_secret(
                request={"parent": parent, "secret_id": secret_id, "secret": secret}
            )
            sm_client.add_secret_version(
                request={
                    "parent": secret_path,
                    "payload": {"data": url.encode("utf-8")},
                }
            )
            return GenerateUrlSchema(
                status="created",
                message="Se creó el secreto con TTL de 7 días.",
                secret_id=secret_id,
                url=url,
            )

        except gcloud_exc.Forbidden:
            raise HTTPException(
                status_code=403, detail="Forbidden accessing Secret Manager"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Secret Manager error: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
