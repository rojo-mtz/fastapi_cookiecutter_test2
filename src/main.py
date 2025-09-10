from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from starlette.middleware.cors import CORSMiddleware

from api.urls import api_router
from core.settings import settings

# from scraper import main as scrape

# Define API Key security scheme for Swagger UI
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

app = FastAPI(
    title=settings.Config.PROJECT_NAME,
    openapi_url=f"{settings.API_V1}/openapi.json",
    description="""
    Template Microservice with FastAPI and Google Cloud integration.

    ## Authentication

    This API requires authentication using an API key in the header:
    - **Header name**: `X-API-KEY`
    - **Value**: Your API key (set in LOCAL_API_KEY environment variable)

    ### How to test in Swagger UI:
    1. Click the "Authorize" button (🔒) at the top right
    2. Enter your API key in the "X-API-KEY" field
    3. Click "Authorize"
    4. Now you can test the protected endpoints

    ### Exceptions:
    - Google Cloud Cron jobs (X-Appengine-Cron: true)
    - Google Cloud Tasks (User-Agent starts with "Google-Cloud-Tasks")
    """,
    version="0.1.0",
)

# # Create DB and load codes from web scraping
# scrape()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1)
