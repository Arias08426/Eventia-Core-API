from typing import List

from sqlalchemy.orm import Session

from src.cache.redis_client import cache
from src.exceptions.custom_exceptions import NotFoundException
from src.models.attendance import Attendance
from src.models.event import Event
from src.schemas.event import EventCreate, EventStatistics, EventUpdate


class EventService:
    """Servicio de lógica de negocio para eventos"""

    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event_data: EventCreate) -> Event:
        """Crea un nuevo evento"""
        event = Event(**event_data.model_dump())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        cache.delete_pattern("events:list:*")
        return event

    def get_event(self, event_id: int) -> Event:
        """Obtiene un evento por ID"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")
        return event

    def get_all_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Obtiene todos los eventos con paginación"""
        return self.db.query(Event).offset(skip).limit(limit).all()

    def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        """Actualiza un evento"""
        event = self.get_event(event_id)
        update_data = event_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        self.db.commit()
        self.db.refresh(event)
        cache.delete(f"event:{event_id}")
        cache.delete_pattern("events:list:*")
        return event

    def delete_event(self, event_id: int) -> bool:
        """Elimina un evento"""
        event = self.get_event(event_id)
        self.db.delete(event)
        self.db.commit()
        cache.delete(f"event:{event_id}")
        cache.delete_pattern("events:list:*")
        return True

    def get_available_capacity(self, event_id: int) -> int:
        """Calcula la capacidad disponible de un evento"""
        event = self.get_event(event_id)
        registered = (
            self.db.query(Attendance).filter(Attendance.event_id == event_id).count()
        )
        return event.capacity - registered

    def get_event_statistics(self, event_id: int) -> EventStatistics:
        """Obtiene estadísticas de un evento"""
        event = self.get_event(event_id)
        registered = (
            self.db.query(Attendance).filter(Attendance.event_id == event_id).count()
        )
        available = event.capacity - registered
        occupation = (registered / event.capacity) * 100 if event.capacity > 0 else 0
        return EventStatistics(
            event_id=event.id,
            event_name=event.name,
            total_capacity=event.capacity,
            registered_participants=registered,
            available_capacity=available,
            occupation_percentage=round(occupation, 2),
        )
