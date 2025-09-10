import logging
import os

from fastapi import HTTPException, Request

# Import settings to get LOCAL_API_KEY
from .settings import settings


async def require_api_key(request: Request) -> str:
    """
    FastAPI dependency to require API key authentication.
    Returns the API key if valid, raises HTTPException otherwise.
    """
    # 1) Cron / Cloud Task (App Engine target)
    if request.headers.get("X-Appengine-Cron") == "true" or request.headers.get(
        "X-Appengine-Taskname"
    ):
        return "cron_task"

    # 1b) Cloud Tasks HTTP target (no Appengine headers, pero sí User-Agent)
    ua = request.headers.get("User-Agent", "")
    if ua.startswith("Google-Cloud-Tasks"):
        return "cloud_task"

    # 2) Para todo lo demás, exige X-API-KEY
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key != settings.LOCAL_API_KEY:
        logging.warning("No valid APIKEY provided")
        raise HTTPException(status_code=401, detail="Invalid or missing local API key")

    return api_key
