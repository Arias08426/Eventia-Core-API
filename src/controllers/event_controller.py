"""
Controller para endpoints de Eventos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.services.event_service import EventService
from src.schemas.event import EventCreate, EventUpdate, EventResponse, EventStatistics
from src.exceptions.custom_exceptions import EventiaException

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo evento.
    
    **Parámetros:**
    - **name**: Nombre del evento (mínimo 3 caracteres)
    - **description**: Descripción opcional del evento
    - **location**: Ubicación del evento
    - **date**: Fecha y hora del evento (debe ser futura)
    - **capacity**: Capacidad máxima de participantes
    
    **Retorna:**
    - Evento creado con su ID y fechas de creación
    """
    try:
        service = EventService(db)
        return service.create_event(event)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=List[EventResponse])
def get_all_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los eventos con paginación.
    
    **Parámetros:**
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros a retornar (default: 100, máx: 100)
    
    **Retorna:**
    - Lista de eventos con capacidad disponible
    """
    try:
        service = EventService(db)
        events = service.get_all_events(skip, limit)
        
        # Agregar capacidad disponible a cada evento
        for event in events:
            event.available_capacity = service.get_available_capacity(event.id)
        
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un evento específico por su ID.
    
    **Parámetros:**
    - **event_id**: ID del evento
    
    **Retorna:**
    - Evento con capacidad disponible
    
    **Errores:**
    - 404: Evento no encontrado
    """
    try:
        service = EventService(db)
        event = service.get_event(event_id)
        event.available_capacity = service.get_available_capacity(event_id)
        return event
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un evento existente.
    
    **Parámetros:**
    - **event_id**: ID del evento
    - Solo se actualizan los campos proporcionados
    
    **Retorna:**
    - Evento actualizado
    
    **Errores:**
    - 404: Evento no encontrado
    - 422: Error de validación
    """
    try:
        service = EventService(db)
        updated_event = service.update_event(event_id, event)
        updated_event.available_capacity = service.get_available_capacity(event_id)
        return updated_event
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un evento.
    
    **Parámetros:**
    - **event_id**: ID del evento
    
    **Nota:** 
    - También elimina todas las asistencias asociadas
    
    **Errores:**
    - 404: Evento no encontrado
    """
    try:
        service = EventService(db)
        service.delete_event(event_id)
        return None
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{event_id}/statistics", response_model=EventStatistics)
def get_event_statistics(
    event_id: int,
    db: Session = Depends(get_db)
):
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