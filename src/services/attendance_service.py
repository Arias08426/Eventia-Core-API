from typing import List

from sqlalchemy.orm import Session

from src.cache.redis_client import cache
from src.exceptions.custom_exceptions import (
    CapacityExceededException,
    DuplicateRegistrationException,
    NotFoundException,
)
from src.models.attendance import Attendance
from src.models.event import Event
from src.models.participant import Participant
from src.schemas.attendance import AttendanceCreate, AttendanceDetail


class AttendanceService:
    """Servicio de lógica de negocio para asistencias"""

    def __init__(self, db: Session):
        self.db = db

    def register_attendance(self, attendance_data: AttendanceCreate) -> Attendance:
        """Registra un participante a un evento"""
        event_id = attendance_data.event_id
        participant_id = attendance_data.participant_id

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")

        participant = (
            self.db.query(Participant).filter(Participant.id == participant_id).first()
        )
        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )
        existing = (
            self.db.query(Attendance)
            .filter(
                Attendance.event_id == event_id,
                Attendance.participant_id == participant_id,
            )
            .first()
        )
        if existing:
            raise DuplicateRegistrationException(
                f"El participante {participant.name} ya está registrado "
                f"en el evento {event.name}"
            )

        registered_count = (
            self.db.query(Attendance).filter(Attendance.event_id == event_id).count()
        )
        if registered_count >= event.capacity:
            raise CapacityExceededException(
                f"El evento {event.name} ha alcanzado su capacidad máxima "
                f"({event.capacity} participantes)"
            )

        attendance = Attendance(event_id=event_id, participant_id=participant_id)
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        cache.delete(f"event:stats:{event_id}")
        cache.delete(f"event:attendances:{event_id}")
        cache.delete(f"participant:attendances:{participant_id}")
        return attendance

    def cancel_attendance(self, attendance_id: int) -> bool:
        """Cancela una asistencia"""
        attendance = (
            self.db.query(Attendance).filter(Attendance.id == attendance_id).first()
        )
        if not attendance:
            raise NotFoundException(f"Asistencia con ID {attendance_id} no encontrada")

        event_id = attendance.event_id
        participant_id = attendance.participant_id
        self.db.delete(attendance)
        self.db.commit()
        cache.delete(f"event:stats:{event_id}")
        cache.delete(f"event:attendances:{event_id}")
        cache.delete(f"participant:attendances:{participant_id}")
        return True

    def get_event_attendances(self, event_id: int) -> List[AttendanceDetail]:
        """Obtiene todos los participantes registrados en un evento"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")

        attendances = (
            self.db.query(
                Attendance.id,
                Attendance.event_id,
                Event.name.label("event_name"),
                Attendance.participant_id,
                Participant.name.label("participant_name"),
                Participant.email.label("participant_email"),
                Attendance.registered_at,
            )
            .join(Event)
            .join(Participant)
            .filter(Attendance.event_id == event_id)
            .all()
        )

        return [
            AttendanceDetail(
                id=a.id,
                event_id=a.event_id,
                event_name=a.event_name,
                participant_id=a.participant_id,
                participant_name=a.participant_name,
                participant_email=a.participant_email,
                registered_at=a.registered_at,
            )
            for a in attendances
        ]

    def get_participant_attendances(
        self, participant_id: int
    ) -> List[AttendanceDetail]:
        """Obtiene todos los eventos en los que está registrado un participante"""
        participant = (
            self.db.query(Participant).filter(Participant.id == participant_id).first()
        )
        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )

        attendances = (
            self.db.query(
                Attendance.id,
                Attendance.event_id,
                Event.name.label("event_name"),
                Attendance.participant_id,
                Participant.name.label("participant_name"),
                Participant.email.label("participant_email"),
                Attendance.registered_at,
            )
            .join(Event)
            .join(Participant)
            .filter(Attendance.participant_id == participant_id)
            .all()
        )

        return [
            AttendanceDetail(
                id=a.id,
                event_id=a.event_id,
                event_name=a.event_name,
                participant_id=a.participant_id,
                participant_name=a.participant_name,
                participant_email=a.participant_email,
                registered_at=a.registered_at,
            )
            for a in attendances
        ]
