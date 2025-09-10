from fastapi import APIRouter

from .endpoints import health, providers

api_router = APIRouter()
api_router.include_router(health.router, tags=["health_check"])
api_router.include_router(providers.router, tags=["providers"])
