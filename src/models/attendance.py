"""
Modelo de base de datos para Asistencias
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.connection import Base


class Attendance(Base):
    """
    Modelo de Asistencia

    Representa la relación muchos-a-muchos entre Eventos y Participantes.
    Un participante solo puede registrarse una vez por evento.
    """

    __tablename__ = "attendances"

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    event = relationship("Event", back_populates="attendances")
    participant = relationship("Participant", back_populates="attendances")

    # Restricción de unicidad: un participante solo puede registrarse una vez por evento
    __table_args__ = (
        UniqueConstraint("event_id", "participant_id", name="unique_event_participant"),
    )

    def __repr__(self):
        return f"<Attendance(event_id={self.event_id}, participant_id={self.participant_id})>"
