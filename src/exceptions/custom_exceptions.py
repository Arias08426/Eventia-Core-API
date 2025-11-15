"""
Excepciones personalizadas para Eventia Core API.

Estas excepciones permiten manejar errores de negocio de manera específica
y proporcionar mensajes de error claros a los clientes de la API.
"""


class EventiaException(Exception):
    """
    Excepción base para todas las excepciones personalizadas de Eventia.
    
    Todas las excepciones de negocio heredan de esta clase.
    
    Attributes:
        message: Mensaje descriptivo del error
        status_code: Código HTTP asociado al error
    
    Ejemplo:
        raise EventiaException("Error general", status_code=500)
    """
    
    def __init__(self, message: str, status_code: int = 400):
        """
        Inicializa la excepción.
        
        Args:
            message: Mensaje descriptivo del error
            status_code: Código HTTP (default: 400 Bad Request)
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(EventiaException):
    """
    Excepción lanzada cuando un recurso no se encuentra en la base de datos.
    
    Código HTTP: 404 Not Found
    
    Casos de uso:
    - Buscar un evento que no existe
    - Buscar un participante que no existe
    - Buscar una asistencia que no existe
    
    Ejemplo:
        raise NotFoundException("Evento con ID 123 no encontrado")
    """
    
    def __init__(self, message: str = "Recurso no encontrado"):
        """
        Inicializa la excepción con mensaje personalizado.
        
        Args:
            message: Mensaje descriptivo (default: "Recurso no encontrado")
        """
        super().__init__(message, status_code=404)


class AlreadyExistsException(EventiaException):
    """
    Excepción lanzada cuando se intenta crear un recurso que ya existe.
    
    Código HTTP: 409 Conflict
    
    Casos de uso:
    - Intentar crear un participante con email duplicado
    - Intentar crear cualquier recurso que viole restricciones de unicidad
    
    Ejemplo:
        raise AlreadyExistsException("El email juan@example.com ya está registrado")
    """
    
    def __init__(self, message: str = "El recurso ya existe"):
        """
        Inicializa la excepción con mensaje personalizado.
        
        Args:
            message: Mensaje descriptivo (default: "El recurso ya existe")
        """
        super().__init__(message, status_code=409)


class CapacityExceededException(EventiaException):
    """
    Excepción lanzada cuando se excede la capacidad de un evento.
    
    Código HTTP: 400 Bad Request
    
    Casos de uso:
    - Intentar registrar un participante a un evento lleno
    
    Regla de negocio:
    - Un evento tiene capacidad máxima
    - No se pueden registrar más participantes una vez alcanzada la capacidad
    
    Ejemplo:
        raise CapacityExceededException(
            "El evento 'Conferencia Tech' ha alcanzado su capacidad máxima (100 participantes)"
        )
    """
    
    def __init__(self, message: str = "Capacidad del evento excedida"):
        """
        Inicializa la excepción con mensaje personalizado.
        
        Args:
            message: Mensaje descriptivo (default: "Capacidad del evento excedida")
        """
        super().__init__(message, status_code=400)


class DuplicateRegistrationException(EventiaException):
    """
    Excepción lanzada cuando un participante intenta registrarse dos veces al mismo evento.
    
    Código HTTP: 409 Conflict
    
    Casos de uso:
    - Intentar registrar un participante que ya está registrado en el evento
    
    Regla de negocio:
    - Un participante solo puede registrarse una vez por evento
    - Esta restricción está implementada en la BD con UniqueConstraint
    
    Ejemplo:
        raise DuplicateRegistrationException(
            "El participante Juan Pérez ya está registrado en el evento Conferencia Tech"
        )
    """
    
    def __init__(self, message: str = "El participante ya está registrado en este evento"):
        """
        Inicializa la excepción con mensaje personalizado.
        
        Args:
            message: Mensaje descriptivo 
                    (default: "El participante ya está registrado en este evento")
        """
        super().__init__(message, status_code=409)


class ValidationException(EventiaException):
    """
    Excepción lanzada cuando falla la validación de datos.
    
    Código HTTP: 422 Unprocessable Entity
    
    Casos de uso:
    - Datos de entrada inválidos que pasan la validación de Pydantic
    - Validaciones de negocio adicionales
    - Formato de datos incorrecto
    
    Nota:
        Pydantic ya maneja la mayoría de validaciones básicas.
        Esta excepción es para validaciones de negocio más complejas.
    
    Ejemplo:
        raise ValidationException("La fecha del evento debe ser al menos 24 horas en el futuro")
    """
    
    def __init__(self, message: str = "Error de validación"):
        """
        Inicializa la excepción con mensaje personalizado.
        
        Args:
            message: Mensaje descriptivo (default: "Error de validación")
        """
        super().__init__(message, status_code=422)


# ============================================
# JERARQUÍA DE EXCEPCIONES
# ============================================
"""
EventiaException (400)
    ├── NotFoundException (404)
    ├── AlreadyExistsException (409)
    ├── CapacityExceededException (400)
    ├── DuplicateRegistrationException (409)
    └── ValidationException (422)

Todas heredan de EventiaException, lo que permite:
1. Capturar todas las excepciones de negocio con un solo handler
2. Mantener consistencia en el manejo de errores
3. Facilitar el testing
"""