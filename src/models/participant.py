from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database.connection import Base


class Participant(Base):
    """
    Modelo de Participante

    Representa una persona que puede registrarse en eventos.
    """

    __tablename__ = "participants"

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    attendances = relationship(
        "Attendance", back_populates="participant", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Participant(id={self.id}, name='{self.name}', email='{self.email}')>"
