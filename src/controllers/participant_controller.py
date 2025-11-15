"""
Controller para endpoints de Participantes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.services.participant_service import ParticipantService
from src.schemas.participant import ParticipantCreate, ParticipantUpdate, ParticipantResponse
from src.exceptions.custom_exceptions import EventiaException

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.post("/", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED)
def create_participant(
    participant: ParticipantCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo participante.
    
    **Parámetros:**
    - **name**: Nombre completo del participante
    - **email**: Email único del participante
    - **phone**: Número de teléfono del participante
    
    **Retorna:**
    - Participante creado con su ID
    
    **Errores:**
    - 409: Email ya registrado
    """
    try:
        service = ParticipantService(db)
        return service.create_participant(participant)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=List[ParticipantResponse])
def get_all_participants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los participantes con paginación.
    
    **Parámetros:**
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros a retornar (default: 100, máx: 100)
    
    **Retorna:**
    - Lista de participantes registrados
    """
    try:
        service = ParticipantService(db)
        return service.get_all_participants(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{participant_id}", response_model=ParticipantResponse)
def get_participant(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un participante específico por su ID.
    
    **Parámetros:**
    - **participant_id**: ID del participante
    
    **Retorna:**
    - Datos del participante
    
    **Errores:**
    - 404: Participante no encontrado
    """
    try:
        service = ParticipantService(db)
        return service.get_participant(participant_id)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{participant_id}", response_model=ParticipantResponse)
def update_participant(
    participant_id: int,
    participant: ParticipantUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un participante existente.
    
    **Parámetros:**
    - **participant_id**: ID del participante
    - Solo se actualizan los campos proporcionados
    
    **Retorna:**
    - Participante actualizado
    
    **Errores:**
    - 404: Participante no encontrado
    - 409: Email ya está en uso
    """
    try:
        service = ParticipantService(db)
        return service.update_participant(participant_id, participant)
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un participante.
    
    **Parámetros:**
    - **participant_id**: ID del participante
    
    **Nota:** 
    - También cancela todas sus asistencias a eventos
    
    **Errores:**
    - 404: Participante no encontrado
    """
    try:
        service = ParticipantService(db)
        service.delete_participant(participant_id)
        return None
    except EventiaException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
