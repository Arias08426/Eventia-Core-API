"""
Middleware para manejo centralizado de errores.

Este módulo intercepta todas las excepciones lanzadas en la aplicación
y las convierte en respuestas HTTP apropiadas con formato JSON consistente.
"""
import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions.custom_exceptions import EventiaException

# Configurar logger
logger = logging.getLogger(__name__)


async def eventia_exception_handler(
    request: Request, exc: EventiaException
) -> JSONResponse:
    """
    Handler para excepciones personalizadas de Eventia.

    Maneja todas las excepciones que heredan de EventiaException:
    - NotFoundException (404)
    - AlreadyExistsException (409)
    - CapacityExceededException (400)
    - DuplicateRegistrationException (409)
    - ValidationException (422)

    Args:
        request: Request de FastAPI con información de la petición
        exc: Excepción de Eventia lanzada

    Returns:
        JSONResponse con formato consistente de error

    Formato de respuesta:
        {
            "error": "NotFoundException",
            "message": "Evento con ID 123 no encontrado",
            "path": "/events/123"
        }

    Ejemplo de uso:
        En main.py:
        app.add_exception_handler(EventiaException, eventia_exception_handler)
    """
    # Log del error (nivel WARNING porque son errores esperados de negocio)
    logger.warning(
        f"EventiaException: {exc.__class__.__name__} - {exc.message} "
        f"(Path: {request.url.path}, Method: {request.method})"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url.path),
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler para excepciones generales no manejadas.

    Este handler captura todas las excepciones que no son EventiaException,
    como:
    - Errores de Python (ValueError, TypeError, etc.)
    - Errores de base de datos
    - Errores de conexión
    - Cualquier otro error no anticipado

    Args:
        request: Request de FastAPI con información de la petición
        exc: Excepción general de Python

    Returns:
        JSONResponse con error genérico 500

    Formato de respuesta:
        {
            "error": "InternalServerError",
            "message": "Ha ocurrido un error interno en el servidor",
            "path": "/events"
        }

    Nota:
        - No expone detalles del error al cliente (seguridad)
        - Registra el error completo en logs para debugging
        - Siempre retorna 500 Internal Server Error

    Ejemplo de uso:
        En main.py:
        app.add_exception_handler(Exception, general_exception_handler)
    """
    # Log completo del error con stack trace (nivel ERROR)
    logger.error(
        f"Unhandled exception: {exc.__class__.__name__} - {str(exc)} "
        f"(Path: {request.url.path}, Method: {request.method})",
        exc_info=True,  # Incluye el stack trace completo
    )

    # En desarrollo, incluir más detalles
    # En producción, solo mensaje genérico
    error_detail = {
        "error": "InternalServerError",
        "message": "Ha ocurrido un error interno en el servidor",
        "path": str(request.url.path),
    }

    # Opcionalmente, en desarrollo podemos agregar más info
    # if settings.DEBUG:
    #     error_detail["detail"] = str(exc)
    #     error_detail["type"] = exc.__class__.__name__

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_detail
    )


# ============================================
# EJEMPLO DE RESPUESTAS DE ERROR
# ============================================
"""
1. Error de negocio (EventiaException):
   Status: 404
   {
       "error": "NotFoundException",
       "message": "Evento con ID 123 no encontrado",
       "path": "/events/123"
   }

2. Error de duplicado (EventiaException):
   Status: 409
   {
       "error": "AlreadyExistsException",
       "message": "El email juan@example.com ya está registrado",
       "path": "/participants"
   }

3. Error de capacidad (EventiaException):
   Status: 400
   {
       "error": "CapacityExceededException",
       "message": "El evento ha alcanzado su capacidad máxima",
       "path": "/attendances"
   }

4. Error interno (Exception general):
   Status: 500
   {
       "error": "InternalServerError",
       "message": "Ha ocurrido un error interno en el servidor",
       "path": "/events"
   }

5. Error de validación de Pydantic (manejado por FastAPI):
   Status: 422
   {
       "detail": [
           {
               "loc": ["body", "email"],
               "msg": "value is not a valid email address",
               "type": "value_error.email"
           }
       ]
   }
"""

# ============================================
# VENTAJAS DE ESTE ENFOQUE
# ============================================
"""
✅ Respuestas consistentes: Mismo formato JSON para todos los errores
✅ Códigos HTTP apropiados: 404, 409, 400, 500, etc.
✅ Logging centralizado: Todos los errores se registran
✅ Seguridad: No expone detalles internos en producción
✅ Debugging: Stack trace completo en logs
✅ Mantenible: Fácil agregar nuevos tipos de error
✅ Testeable: Fácil probar el manejo de errores
"""
