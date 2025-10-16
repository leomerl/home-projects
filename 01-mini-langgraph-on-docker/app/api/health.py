from fastapi import APIRouter
from app.services.redis_client import redis_ping

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok", "redis": "up" if redis_ping() else "down"}