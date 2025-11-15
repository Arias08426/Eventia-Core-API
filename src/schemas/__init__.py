"""
Schemas Pydantic para validación de entrada/salida
"""
from .attendance import AttendanceCreate, AttendanceDetail, AttendanceResponse
from .event import EventCreate, EventResponse, EventStatistics, EventUpdate
from .participant import ParticipantCreate, ParticipantResponse, ParticipantUpdate

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
    "AttendanceDetail",
]
