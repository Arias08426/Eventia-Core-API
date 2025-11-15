"""
Eventia Core API - Sistema de Gestión de Eventos

Este es el punto de entrada principal de la aplicación FastAPI.
Configura todos los componentes, middlewares, rutas y eventos del ciclo de vida.

Autor: [Tu nombre]
Versión: 1.0.0
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from src.config.setting import settings
from src.database.connection import init_db
from src.controllers import (
    event_controller,
    participant_controller,
    attendance_controller,
    health_controller
)
from src.middleware.error_handler import (
    eventia_exception_handler,
    general_exception_handler
)
from src.exceptions.custom_exceptions import EventiaException


# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


# ============================================
# CREAR APLICACIÓN FASTAPI
# ============================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Eventia Core API
    
    API REST para gestión de eventos, participantes y asistencias.
    
    ### Funcionalidades principales:
    
    * **Eventos**: Crear, consultar, actualizar y eliminar eventos
    * **Participantes**: Gestionar participantes con email único
    * **Asistencias**: Registrar participantes a eventos con validaciones
    * **Estadísticas**: Consultar ocupación y capacidad de eventos
    * **Caché**: Sistema de caché con Redis para mejorar rendimiento
    
    ### Características técnicas:
    
    * Base de datos: PostgreSQL
    * Caché: Redis
    * Validaciones automáticas con Pydantic
    * Documentación interactiva (Swagger/ReDoc)
    * Manejo centralizado de errores
    * Logging estructurado
    
    ### Endpoints disponibles:
    
    * `/events` - Gestión de eventos
    * `/participants` - Gestión de participantes
    * `/attendances` - Gestión de asistencias
    * `/health` - Health checks
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "soporte@eventia.com"
    },
    license_info={
        "name": "MIT",
    }
)


# ============================================
# CONFIGURAR CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    
    allow_credentials=True,
    
    allow_methods=["*"],
    
    allow_headers=["*"],
    
)


# ============================================
# REGISTRAR EXCEPTION HANDLERS
# ============================================
app.add_exception_handler(EventiaException, eventia_exception_handler)
"""
Handler para excepciones de negocio (404, 409, 400, 422)
"""

app.add_exception_handler(Exception, general_exception_handler)
"""
Handler para excepciones generales no manejadas (500)
"""


# ============================================
# REGISTRAR ROUTERS (ENDPOINTS)
# ============================================
app.include_router(
    health_controller.router,
    tags=["Health"]
)

app.include_router(
    event_controller.router,
    tags=["Events"]
)

app.include_router(
    participant_controller.router,
    tags=["Participants"]
)

app.include_router(
    attendance_controller.router,
    tags=["Attendances"]
)


# ============================================
# EVENTOS DEL CICLO DE VIDA
# ============================================
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    
    Tareas realizadas:
    1. Logging de inicio
    2. Inicialización de base de datos (crear tablas)
    3. Verificación de configuración
    
    Este evento se ejecuta UNA VEZ al levantar el servidor.
    """
    logger.info("=" * 60)
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📦 Entorno: {settings.APP_ENV}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
    logger.info("=" * 60)
    
    # Inicializar base de datos
    try:
        logger.info("🗄️  Inicializando base de datos...")
        init_db()
        logger.info("✅ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {e}")
        raise
    
    # Verificar configuración
    logger.info("⚙️  Verificando configuración...")
    logger.info(f"   - PostgreSQL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configurado'}")
    logger.info(f"   - Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info(f"   - CORS Origins: {len(settings.CORS_ORIGINS)} configurados")
    
    logger.info("=" * 60)
    logger.info(f"✨ {settings.APP_NAME} iniciado exitosamente")
    logger.info(f"📚 Documentación: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al detener la aplicación.
    
    Tareas realizadas:
    1. Logging de cierre
    2. Limpieza de recursos (si es necesario)
    
    Este evento se ejecuta cuando se detiene el servidor (Ctrl+C).
    """
    logger.info("=" * 60)
    logger.info(f"🛑 Cerrando {settings.APP_NAME}...")
    logger.info("👋 Aplicación detenida correctamente")
    logger.info("=" * 60)


# ============================================
# ENDPOINTS RAÍZ
# ============================================
@app.get(
    "/",
    tags=["Root"],
    summary="Endpoint raíz",
    description="Proporciona información básica de la API y enlaces útiles"
)
async def root():
    """
    Endpoint raíz de la API.
    
    Retorna información general sobre la API y enlaces de navegación.
    
    Returns:
        dict: Información de la API
    """
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "operational",
        "links": {
            "documentation": f"http://{settings.HOST}:{settings.PORT}/docs",
            "alternative_docs": f"http://{settings.HOST}:{settings.PORT}/redoc",
            "health_check": f"http://{settings.HOST}:{settings.PORT}/health",
            "detailed_health": f"http://{settings.HOST}:{settings.PORT}/health/detailed"
        },
        "endpoints": {
            "events": f"http://{settings.HOST}:{settings.PORT}/events",
            "participants": f"http://{settings.HOST}:{settings.PORT}/participants",
            "attendances": f"http://{settings.HOST}:{settings.PORT}/attendances"
        }
    }


@app.get(
    "/info",
    tags=["Root"],
    summary="Información de la API",
    description="Detalles técnicos de la API"
)
async def info():
    """
    Proporciona información técnica detallada de la API.
    
    Returns:
        dict: Información técnica
    """
    return {
        "api": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV
        },
        "features": [
            "CRUD de Eventos",
            "CRUD de Participantes",
            "Gestión de Asistencias",
            "Estadísticas en tiempo real",
            "Sistema de caché con Redis",
            "Validaciones automáticas",
            "Documentación interactiva"
        ],
        "technology_stack": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "cache": "Redis",
            "orm": "SQLAlchemy",
            "validation": "Pydantic"
        }
    }


# ============================================
# EJECUTAR APLICACIÓN
# ============================================
if __name__ == "__main__":
    """
    Ejecuta la aplicación usando Uvicorn.
    
    Este bloque solo se ejecuta si se corre el archivo directamente:
        python src/main.py
    
    Para producción, usar:
        uvicorn src.main:app --host 0.0.0.0 --port 8000
    """
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        
        log_level=settings.LOG_LEVEL.lower()
    )


# ============================================
# COMANDOS ÚTILES
# ============================================
"""
DESARROLLO:
-----------
# Ejecutar la aplicación
python src/main.py

# O con uvicorn directamente
uvicorn src.main:app --reload

# Especificar puerto
uvicorn src.main:app --reload --port 8000


PRODUCCIÓN:
-----------
# Ejecutar sin reload
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Con múltiples workers
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Con Gunicorn + Uvicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


ACCEDER A LA DOCUMENTACIÓN:
----------------------------
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json


HEALTH CHECKS:
--------------
- Básico: http://localhost:8000/health
- Detallado: http://localhost:8000/health/detailed
"""