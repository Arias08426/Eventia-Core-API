"""
Schemas Pydantic para Asistencias
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AttendanceCreate(BaseModel):
    """
    Schema para registrar una nueva asistencia.
    
    Relaciona un participante con un evento.
    """
    event_id: int = Field(
        ..., 
        gt=0, 
        description="ID del evento al que se registra"
    )
    participant_id: int = Field(
        ..., 
        gt=0, 
        description="ID del participante que se registra"
    )
    
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "event_id": 1,
                "participant_id": 5
            }
        }


class AttendanceResponse(BaseModel):
    """
    Schema de respuesta básica para asistencias.
    
    Incluye IDs y fecha de registro.
    """
    id: int = Field(..., description="ID único de la asistencia")
    event_id: int = Field(..., description="ID del evento")
    participant_id: int = Field(..., description="ID del participante")
    registered_at: datetime = Field(..., description="Fecha y hora de registro")
    
    class Config:
        """Configuración de Pydantic"""
        from_attributes = True  # Permite crear desde objetos ORM
        json_schema_extra = {
            "example": {
                "id": 1,
                "event_id": 1,
                "participant_id": 5,
                "registered_at": "2024-01-15T14:30:00"
            }
        }


class AttendanceDetail(BaseModel):
    """
    Schema detallado de asistencia con información completa.
    
    Incluye información del evento y del participante.
    Útil para consultas que requieren datos relacionados.
    """
    id: int = Field(..., description="ID único de la asistencia")
    event_id: int = Field(..., description="ID del evento")
    event_name: str = Field(..., description="Nombre del evento")
    participant_id: int = Field(..., description="ID del participante")
    participant_name: str = Field(..., description="Nombre del participante")
    participant_email: str = Field(..., description="Email del participante")
    registered_at: datetime = Field(..., description="Fecha y hora de registro")
    
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "event_id": 1,
                "event_name": "Conferencia Tech 2024",
                "participant_id": 5,
                "participant_name": "Juan Pérez",
                "participant_email": "juan.perez@example.com",
                "registered_at": "2024-01-15T14:30:00"
            }
        }


class EventAttendanceList(BaseModel):
    """
    Schema para listar participantes de un evento específico.
    
    Proporciona un resumen del evento con sus participantes.
    """
    event_id: int = Field(..., description="ID del evento")
    event_name: str = Field(..., description="Nombre del evento")
    total_participants: int = Field(
        ..., 
        description="Número total de participantes registrados"
    )
    participants: list[dict] = Field(
        ..., 
        description="Lista de participantes con su información"
    )
    
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "event_id": 1,
                "event_name": "Conferencia Tech 2024",
                "total_participants": 2,
                "participants": [
                    {
                        "id": 5,
                        "name": "Juan Pérez",
                        "email": "juan.perez@example.com",
                        "registered_at": "2024-01-15T14:30:00"
                    },
                    {
                        "id": 7,
                        "name": "María García",
                        "email": "maria.garcia@example.com",
                        "registered_at": "2024-01-15T15:00:00"
                    }
                ]
            }
        }


class ParticipantAttendanceList(BaseModel):
    """
    Schema para listar eventos de un participante específico.
    
    Proporciona un resumen del participante con sus eventos.
    """
    participant_id: int = Field(..., description="ID del participante")
    participant_name: str = Field(..., description="Nombre del participante")
    total_events: int = Field(
        ..., 
        description="Número total de eventos registrados"
    )
    events: list[dict] = Field(
        ..., 
        description="Lista de eventos con su información"
    )
    
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "participant_id": 5,
                "participant_name": "Juan Pérez",
                "total_events": 2,
                "events": [
                    {
                        "id": 1,
                        "name": "Conferencia Tech 2024",
                        "date": "2024-02-15T09:00:00",
                        "location": "Centro de Convenciones",
                        "registered_at": "2024-01-15T14:30:00"
                    },
                    {
                        "id": 3,
                        "name": "Workshop Python",
                        "date": "2024-03-20T14:00:00",
                        "location": "Universidad Nacional",
                        "registered_at": "2024-01-20T10:00:00"
                    }
                ]
            }
        }