"""
Controller para endpoints de Asistencias
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.services.attendance_service import AttendanceService
from src.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceDetail
from src.exceptions.custom_exceptions import EventiaException

router = APIRouter(prefix="/attendances", tags=["Attendances"])


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def register_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    """
    Registra un participante a un evento.
    
    **Parámetros:**
    - **event_id**: ID del evento al que se quiere registrar
    - **participant_id**: ID del participante que se registra
    
    **Validaciones:**
    - El evento debe existir
    - El participante debe existir
    - No puede haber duplicados (un participante solo puede registrarse una vez por evento)
    - Debe haber capacidad disponible en el evento
    
    **Retorna:**
    - Asistencia creada con su ID y fecha de registro
    
    **Errores:**
    - 400: Capacidad del evento excedida
    - 404: Evento o participante no encontrado
    - 409: El participante ya está registrado en este evento
    """
    try:
        service = AttendanceService(db)
        return service.register_attendance(attendance)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancela una asistencia (elimina el registro de un participante de un evento).
    
    **Parámetros:**
    - **attendance_id**: ID de la asistencia a cancelar
    
    **Errores:**
    - 404: Asistencia no encontrada
    """
    try:
        service = AttendanceService(db)
        service.cancel_attendance(attendance_id)
        return None
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/event/{event_id}", response_model=List[AttendanceDetail])
def get_event_attendances(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los participantes registrados en un evento específico.
    
    **Parámetros:**
    - **event_id**: ID del evento
    
    **Retorna:**
    - Lista detallada de participantes con:
      - ID de asistencia
      - Información del evento (ID y nombre)
      - Información del participante (ID, nombre y email)
      - Fecha de registro
    
    **Nota:**
    - Este endpoint usa caché para mejorar el rendimiento
    
    **Errores:**
    - 404: Evento no encontrado
    """
    try:
        service = AttendanceService(db)
        return service.get_event_attendances(event_id)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/participant/{participant_id}", response_model=List[AttendanceDetail])
def get_participant_attendances(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los eventos en los que está registrado un participante.
    
    **Parámetros:**
    - **participant_id**: ID del participante
    
    **Retorna:**
    - Lista detallada de eventos con:
      - ID de asistencia
      - Información del evento (ID y nombre)
      - Información del participante (ID, nombre y email)
      - Fecha de registro
    
    **Nota:**
    - Este endpoint usa caché para mejorar el rendimiento
    
    **Errores:**
    - 404: Participante no encontrado
    """
    try:
        service = AttendanceService(db)
        return service.get_participant_attendances(participant_id)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")