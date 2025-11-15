"""
Schemas Pydantic para validación de entrada/salida
"""
from .event import (
    EventCreate, 
    EventUpdate, 
    EventResponse, 
    EventStatistics
)
from .participant import (
    ParticipantCreate, 
    ParticipantUpdate, 
    ParticipantResponse
)
from .attendance import (
    AttendanceCreate, 
    AttendanceResponse, 
    AttendanceDetail
)

__all__ = [
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "EventStatistics",
    "ParticipantCreate",
    "ParticipantUpdate",
    "ParticipantResponse",
    "AttendanceCreate",
    "AttendanceResponse",
    "AttendanceDetail"
]