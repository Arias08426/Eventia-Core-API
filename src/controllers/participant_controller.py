"""
Controller para endpoints de Participantes
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.participant import (
    ParticipantCreate,
    ParticipantResponse,
    ParticipantUpdate,
)
from src.services.participant_service import ParticipantService

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.post(
    "/", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED
)
def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    """Crea un nuevo participante."""
    service = ParticipantService(db)
    return service.create_participant(participant)


@router.get("/", response_model=List[ParticipantResponse])
def get_all_participants(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtiene todos los participantes con paginación."""
    service = ParticipantService(db)
    return service.get_all_participants(skip, limit)


@router.get("/{participant_id}", response_model=ParticipantResponse)
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    """Obtiene un participante específico por su ID."""
    service = ParticipantService(db)
    return service.get_participant(participant_id)


@router.put("/{participant_id}", response_model=ParticipantResponse)
def update_participant(
    participant_id: int, participant: ParticipantUpdate, db: Session = Depends(get_db)
):
    """Actualiza un participante existente."""
    service = ParticipantService(db)
    return service.update_participant(participant_id, participant)


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    """Elimina un participante."""
    service = ParticipantService(db)
    service.delete_participant(participant_id)
