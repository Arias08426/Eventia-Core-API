from typing import List

from sqlalchemy.orm import Session

from src.cache.redis_client import cache
from src.exceptions.custom_exceptions import AlreadyExistsException, NotFoundException
from src.models.participant import Participant
from src.schemas.participant import ParticipantCreate, ParticipantUpdate


class ParticipantService:
    """Servicio de lógica de negocio para participantes"""

    def __init__(self, db: Session):
        self.db = db

    def create_participant(self, participant_data: ParticipantCreate) -> Participant:
        """Crea un nuevo participante"""
        existing = (
            self.db.query(Participant)
            .filter(Participant.email == participant_data.email)
            .first()
        )
        if existing:
            raise AlreadyExistsException(
                f"El email {participant_data.email} ya está registrado"
            )
        participant = Participant(**participant_data.model_dump())
        self.db.add(participant)
        self.db.commit()
        self.db.refresh(participant)
        cache.delete_pattern("participants:list:*")
        return participant

    def get_participant(self, participant_id: int) -> Participant:
        """Obtiene un participante por su ID"""
        participant = (
            self.db.query(Participant).filter(Participant.id == participant_id).first()
        )
        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )
        return participant

    def get_participant_by_email(self, email: str):
        """Obtiene un participante por su email"""
        return self.db.query(Participant).filter(Participant.email == email).first()

    def get_all_participants(
        self, skip: int = 0, limit: int = 100
    ) -> list[Participant]:
        """Obtiene todos los participantes con paginación"""
        return self.db.query(Participant).offset(skip).limit(limit).all()

    def update_participant(
        self, participant_id: int, participant_data: ParticipantUpdate
    ) -> Participant:
        """Actualiza un participante existente"""
        participant = self.get_participant(participant_id)
        update_data = participant_data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"] != participant.email:
            existing = (
                self.db.query(Participant)
                .filter(Participant.email == update_data["email"])
                .first()
            )
            if existing:
                raise AlreadyExistsException(
                    f"El email {update_data['email']} ya está registrado"
                )
        for key, value in update_data.items():
            setattr(participant, key, value)
        self.db.commit()
        self.db.refresh(participant)
        cache.delete(f"participant:{participant_id}")
        cache.delete_pattern("participants:list:*")
        return participant

    def delete_participant(self, participant_id: int) -> bool:
        """Elimina un participante"""
        participant = self.get_participant(participant_id)
        self.db.delete(participant)
        self.db.commit()
        cache.delete(f"participant:{participant_id}")
        cache.delete_pattern("participants:list:*")
        return True
