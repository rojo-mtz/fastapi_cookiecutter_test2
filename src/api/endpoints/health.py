from typing import Dict

from fastapi import APIRouter

from schemas.health import HealthSchema

router = APIRouter()


@router.get("/health", response_model=HealthSchema)
def health_check() -> Dict:
    return {"status": "ok"}
