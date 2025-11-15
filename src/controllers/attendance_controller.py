"""
Controller para endpoints de Asistencias
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.attendance import (
    AttendanceCreate,
    AttendanceDetail,
    AttendanceResponse,
)
from src.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendances", tags=["Attendances"])


@router.post(
    "/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED
)
def register_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    """Registra un participante a un evento."""
    service = AttendanceService(db)
    return service.register_attendance(attendance)


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_attendance(attendance_id: int, db: Session = Depends(get_db)):
    """Cancela una asistencia."""
    service = AttendanceService(db)
    service.cancel_attendance(attendance_id)


@router.get("/event/{event_id}", response_model=List[AttendanceDetail])
def get_event_attendances(event_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los participantes registrados en un evento específico."""
    service = AttendanceService(db)
    return service.get_event_attendances(event_id)


@router.get("/participant/{participant_id}", response_model=List[AttendanceDetail])
def get_participant_attendances(participant_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los eventos en los que está registrado un participante."""
    service = AttendanceService(db)
    return service.get_participant_attendances(participant_id)

