"""
Excepciones personalizadas de la aplicación
"""
from .custom_exceptions import (
    AlreadyExistsException,
    CapacityExceededException,
    DuplicateRegistrationException,
    EventiaException,
    NotFoundException,
    ValidationException,
)

__all__ = [
    "EventiaException",
    "NotFoundException",
    "AlreadyExistsException",
    "CapacityExceededException",
    "DuplicateRegistrationException",
    "ValidationException",
]
