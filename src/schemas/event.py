"""
Schemas Pydantic para Eventos
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EventBase(BaseModel):
    """
    Schema base para eventos con campos comunes.
    """

    name: str = Field(
        ..., min_length=3, max_length=200, description="Nombre del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    location: str = Field(
        ..., min_length=3, max_length=300, description="Ubicación del evento"
    )
    date: datetime = Field(..., description="Fecha y hora del evento")
    capacity: int = Field(..., gt=0, description="Capacidad máxima del evento")

    @field_validator("date")
    @classmethod
    def date_must_be_future(cls, v: datetime) -> datetime:
        """
        Valida que la fecha del evento sea futura.

        Args:
            v: Fecha a validar

        Returns:
            Fecha validada

        Raises:
            ValueError: Si la fecha no es futura
        """
        if v < datetime.utcnow():
            raise ValueError("La fecha del evento debe ser futura")
        return v


class EventCreate(EventBase):
    """
    Schema para crear un nuevo evento.

    Hereda todos los campos de EventBase.
    """

    pass


class EventUpdate(BaseModel):
    """
    Schema para actualizar un evento existente.

    Todos los campos son opcionales para permitir actualizaciones parciales.
    """

    name: Optional[str] = Field(
        None, min_length=3, max_length=200, description="Nombre del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    location: Optional[str] = Field(
        None, min_length=3, max_length=300, description="Ubicación del evento"
    )
    date: Optional[datetime] = Field(None, description="Fecha y hora del evento")
    capacity: Optional[int] = Field(
        None, gt=0, description="Capacidad máxima del evento"
    )

    @field_validator("date")
    @classmethod
    def date_must_be_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        """
        Valida que la fecha del evento sea futura (si se proporciona).

        Args:
            v: Fecha a validar

        Returns:
            Fecha validada o None

        Raises:
            ValueError: Si la fecha no es futura
        """
        if v and v < datetime.utcnow():
            raise ValueError("La fecha del evento debe ser futura")
        return v


class EventResponse(EventBase):
    """
    Schema de respuesta para eventos.

    Incluye campos adicionales como ID y fechas de auditoría.
    """

    id: int = Field(..., description="ID único del evento")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    available_capacity: Optional[int] = Field(
        None, description="Capacidad disponible actual"
    )

    class Config:
        """Configuración de Pydantic"""

        from_attributes = True  # Permite crear desde objetos ORM


class EventStatistics(BaseModel):
    """
    Schema para estadísticas de un evento.

    Proporciona información detallada sobre la ocupación del evento.
    """

    event_id: int = Field(..., description="ID del evento")
    event_name: str = Field(..., description="Nombre del evento")
    total_capacity: int = Field(..., description="Capacidad total del evento")
    registered_participants: int = Field(
        ..., description="Número de participantes registrados"
    )
    available_capacity: int = Field(..., description="Capacidad disponible")
    occupation_percentage: float = Field(
        ..., description="Porcentaje de ocupación (0-100)"
    )

    class Config:
        """Configuración de Pydantic"""

        json_schema_extra = {
            "example": {
                "event_id": 1,
                "event_name": "Conferencia Tech 2024",
                "total_capacity": 100,
                "registered_participants": 75,
                "available_capacity": 25,
                "occupation_percentage": 75.0,
            }
        }
