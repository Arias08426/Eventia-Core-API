from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database.connection import Base


class Event(Base):
    """Modelo de Evento"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(300), nullable=False)
    date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con asistencias
    attendances = relationship(
        "Attendance", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', date={self.date})>"
