from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.event import Event
from src.models.attendance import Attendance
from src.schemas.event import EventCreate, EventUpdate, EventStatistics
from src.exceptions.custom_exceptions import NotFoundException
from src.cache.redis_client import cache


class EventService:
    """Servicio para manejar la lógica de negocio de eventos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_event(self, event_data: EventCreate) -> Event:
        """Crea un nuevo evento"""
        event = Event(**event_data.model_dump())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        # Invalidar caché de listado de eventos
        cache.delete_pattern("events:list:*")
        
        return event
    
    def get_event(self, event_id: int) -> Event:
        """Obtiene un evento por ID"""
        # Intentar obtener del caché
        cache_key = f"event:{event_id}"
        cached_event = cache.get(cache_key)
        
        if cached_event:
            # Reconstruir objeto Event desde caché
            event = self.db.query(Event).filter(Event.id == event_id).first()
            if event:
                return event
        
        # Si no está en caché, buscar en BD
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")
        
        # Guardar en caché
        cache.set(cache_key, {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "location": event.location,
            "capacity": event.capacity
        })
        
        return event
    
    def get_all_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Obtiene todos los eventos con paginación"""
        cache_key = f"events:list:{skip}:{limit}"
        
        # Intentar obtener del caché
        cached_list = cache.get(cache_key)
        if cached_list:
            # Obtener eventos de BD (caché solo guarda IDs)
            event_ids = cached_list.get("ids", [])
            if event_ids:
                return self.db.query(Event).filter(Event.id.in_(event_ids)).all()
        
        # Consultar BD
        events = self.db.query(Event).offset(skip).limit(limit).all()
        
        # Guardar IDs en caché
        if events:
            cache.set(cache_key, {"ids": [e.id for e in events]})
        
        return events
    
    def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        """Actualiza un evento"""
        event = self.get_event(event_id)
        
        update_data = event_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        
        self.db.commit()
        self.db.refresh(event)
        
        # Invalidar caché
        cache.delete(f"event:{event_id}")
        cache.delete_pattern("events:list:*")
        cache.delete(f"event:stats:{event_id}")
        
        return event
    
    def delete_event(self, event_id: int) -> bool:
        """Elimina un evento"""
        event = self.get_event(event_id)
        self.db.delete(event)
        self.db.commit()
        
        # Invalidar caché
        cache.delete(f"event:{event_id}")
        cache.delete_pattern("events:list:*")
        cache.delete(f"event:stats:{event_id}")
        
        return True
    
    def get_available_capacity(self, event_id: int) -> int:
        """Calcula la capacidad disponible de un evento"""
        event = self.get_event(event_id)
        registered = self.db.query(Attendance).filter(
            Attendance.event_id == event_id
        ).count()
        return event.capacity - registered
    
    def get_event_statistics(self, event_id: int) -> EventStatistics:
        """Obtiene estadísticas de un evento"""
        # Intentar obtener del caché
        cache_key = f"event:stats:{event_id}"
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            return EventStatistics(**cached_stats)
        
        # Calcular estadísticas
        event = self.get_event(event_id)
        registered = self.db.query(Attendance).filter(
            Attendance.event_id == event_id
        ).count()
        
        available = event.capacity - registered
        occupation = (registered / event.capacity) * 100 if event.capacity > 0 else 0
        
        stats = EventStatistics(
            event_id=event.id,
            event_name=event.name,
            total_capacity=event.capacity,
            registered_participants=registered,
            available_capacity=available,
            occupation_percentage=round(occupation, 2)
        )
        
        # Guardar en caché
        cache.set(cache_key, stats.model_dump(), ttl=60)  # 1 minuto
        
        return stats