"""
Controller para endpoints de Eventos
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.exceptions.custom_exceptions import EventiaException
from src.schemas.event import EventCreate, EventResponse, EventStatistics, EventUpdate
from src.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Crea un nuevo evento."""
    service = EventService(db)
    return service.create_event(event)


@router.get("/", response_model=List[EventResponse])
def get_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene todos los eventos con paginación."""
    service = EventService(db)
    events = service.get_all_events(skip, limit)
    for event in events:
        event.available_capacity = service.get_available_capacity(event.id)
    return events


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Obtiene un evento específico por su ID."""
    service = EventService(db)
    event = service.get_event(event_id)
    event.available_capacity = service.get_available_capacity(event_id)
    return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    """Actualiza un evento existente."""
    service = EventService(db)
    updated_event = service.update_event(event_id, event)
    updated_event.available_capacity = service.get_available_capacity(event_id)
    return updated_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Elimina un evento."""
    service = EventService(db)
    service.delete_event(event_id)


@router.get("/{event_id}/statistics", response_model=EventStatistics)
def get_event_statistics(event_id: int, db: Session = Depends(get_db)):
    """
    Obtiene estadísticas detalladas de un evento.

    **Parámetros:**
    - **event_id**: ID del evento

    **Retorna:**
    - Capacidad total
    - Participantes registrados
    - Capacidad disponible
    - Porcentaje de ocupación

    **Nota:**
    - Este endpoint usa caché para mejorar el rendimiento

    **Errores:**
    - 404: Evento no encontrado
    """
    try:
        service = EventService(db)
        return service.get_event_statistics(event_id)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
