"""
Controller para endpoints de Health Check
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.cache.redis_client import cache
from src.config.setting import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint de health check básico.
    
    Verifica que la API está funcionando.
    
    **Retorna:**
    - Estado del servicio
    - Nombre de la aplicación
    - Versión
    - Entorno
    
    **Uso:**
    - Útil para balanceadores de carga
    - Monitoreo básico
    - CI/CD pipelines
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }


@router.get("/detailed", status_code=status.HTTP_200_OK)
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Health check detallado con verificación de dependencias.
    
    Verifica:
    - Estado de la API
    - Conexión a PostgreSQL
    - Conexión a Redis
    
    **Retorna:**
    - Estado general del servicio
    - Estado individual de cada componente
    
    **Estados posibles:**
    - **healthy**: Todo funciona correctamente
    - **degraded**: API funcional pero algún servicio secundario tiene problemas (ej: Redis)
    - **unhealthy**: Servicios críticos no funcionan (ej: Base de datos)
    
    **Uso:**
    - Monitoreo detallado
    - Debugging de problemas de infraestructura
    """
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "checks": {}
    }
    
    # Verificar base de datos
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Verificar Redis
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