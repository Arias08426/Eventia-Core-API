"""
Excepciones personalizadas de la aplicación
"""
from .custom_exceptions import (
    EventiaException,
    NotFoundException,
    AlreadyExistsException,
    CapacityExceededException,
    DuplicateRegistrationException,
    ValidationException
)

__all__ = [
    "EventiaException",
    "NotFoundException",
    "AlreadyExistsException",
    "CapacityExceededException",
    "DuplicateRegistrationException",
    "ValidationException"
]