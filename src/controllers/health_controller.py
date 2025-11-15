"""
Controller para endpoints de Health Check
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.cache.redis_client import cache
from src.config.setting import settings
from src.database.connection import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """Verifica que la API está funcionando."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


@router.get("/detailed", status_code=status.HTTP_200_OK)
def detailed_health_check(db: Session = Depends(get_db)):
    """Verifica estado de API, base de datos y Redis."""
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "checks": {},
    }

    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    try:
        if cache.ping():
            health_status["checks"]["redis"] = "healthy"
        else:
            health_status["checks"]["redis"] = "unhealthy: no response"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    return health_status
