"""
Servicio para la lógica de negocio de Participantes
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.cache.redis_client import cache
from src.exceptions.custom_exceptions import AlreadyExistsException, NotFoundException
from src.models.participant import Participant
from src.schemas.participant import ParticipantCreate, ParticipantUpdate


class ParticipantService:
    """
    Servicio que contiene toda la lógica de negocio relacionada con participantes.

    Responsabilidades:
    - CRUD de participantes
    - Validación de emails únicos
    - Gestión de caché
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db

    def create_participant(self, participant_data: ParticipantCreate) -> Participant:
        """
        Crea un nuevo participante.

        Regla de negocio: El email debe ser único en el sistema.

        Args:
            participant_data: Datos del participante a crear

        Returns:
            Participante creado

        Raises:
            AlreadyExistsException: Si el email ya está registrado
        """
        # Verificar si el email ya existe
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

        # Invalidar caché de listado
        cache.delete_pattern("participants:list:*")

        return participant

    def get_participant(self, participant_id: int) -> Participant:
        """
        Obtiene un participante por su ID.

        Args:
            participant_id: ID del participante

        Returns:
            Participante encontrado

        Raises:
            NotFoundException: Si el participante no existe
        """
        # Intentar obtener del caché
        cache_key = f"participant:{participant_id}"
        cached = cache.get(cache_key)

        if cached:
            participant = (
                self.db.query(Participant)
                .filter(Participant.id == participant_id)
                .first()
            )
            if participant:
                return participant

        # Buscar en BD
        participant = (
            self.db.query(Participant).filter(Participant.id == participant_id).first()
        )

        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )

        # Guardar en caché
        cache.set(
            cache_key,
            {
                "id": participant.id,
                "name": participant.name,
                "email": participant.email,
            },
        )

        return participant

    def get_participant_by_email(self, email: str) -> Optional[Participant]:
        """
        Obtiene un participante por su email.

        Args:
            email: Email del participante

        Returns:
            Participante si existe, None en caso contrario
        """
        return self.db.query(Participant).filter(Participant.email == email).first()

    def get_all_participants(
        self, skip: int = 0, limit: int = 100
    ) -> List[Participant]:
        """
        Obtiene todos los participantes con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar

        Returns:
            Lista de participantes
        """
        cache_key = f"participants:list:{skip}:{limit}"

        # Intentar obtener del caché
        cached_list = cache.get(cache_key)
        if cached_list:
            participant_ids = cached_list.get("ids", [])
            if participant_ids:
                return (
                    self.db.query(Participant)
                    .filter(Participant.id.in_(participant_ids))
                    .all()
                )

        # Consultar BD
        participants = self.db.query(Participant).offset(skip).limit(limit).all()

        # Guardar IDs en caché
        if participants:
            cache.set(cache_key, {"ids": [p.id for p in participants]})

        return participants

    def update_participant(
        self, participant_id: int, participant_data: ParticipantUpdate
    ) -> Participant:
        """
        Actualiza un participante existente.

        Regla de negocio: Si se actualiza el email, debe seguir siendo único.

        Args:
            participant_id: ID del participante
            participant_data: Datos a actualizar

        Returns:
            Participante actualizado

        Raises:
            NotFoundException: Si el participante no existe
            AlreadyExistsException: Si el nuevo email ya está registrado
        """
        participant = self.get_participant(participant_id)

        # Si se está actualizando el email, verificar que no exista
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

        # Actualizar campos
        for key, value in update_data.items():
            setattr(participant, key, value)

        self.db.commit()
        self.db.refresh(participant)

        # Invalidar caché
        cache.delete(f"participant:{participant_id}")
        cache.delete_pattern("participants:list:*")

        return participant

    def delete_participant(self, participant_id: int) -> bool:
        """
        Elimina un participante.

        Nota: También elimina todas sus asistencias (cascade).

        Args:
            participant_id: ID del participante

        Returns:
            True si se eliminó correctamente

        Raises:
            NotFoundException: Si el participante no existe
        """
        participant = self.get_participant(participant_id)
        self.db.delete(participant)
        self.db.commit()

        # Invalidar caché
        cache.delete(f"participant:{participant_id}")
        cache.delete_pattern("participants:list:*")

        return True
