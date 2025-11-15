"""
Pruebas unitarias para EventService

Estas pruebas verifican la lógica de negocio de eventos.
"""
import pytest
from datetime import datetime, timedelta
from src.services.event_service import EventService
from src.schemas.event import EventCreate, EventUpdate
from src.exceptions.custom_exceptions import NotFoundException


@pytest.mark.unit
class TestEventService:
    """Pruebas para el servicio de eventos"""
    
    def test_create_event(self, db, sample_event_data):
        """Prueba crear un evento correctamente"""
        # Arrange
        service = EventService(db)
        event_data = EventCreate(**sample_event_data)
        
        # Act
        event = service.create_event(event_data)
        
        # Assert
        assert event.id is not None
        assert event.name == sample_event_data["name"]
        assert event.capacity == sample_event_data["capacity"]
        assert event.created_at is not None
    
    def test_get_event_success(self, db, create_event):
        """Prueba obtener un evento existente"""
        # Arrange
        service = EventService(db)
        
        # Act
        event = service.get_event(create_event.id)
        
        # Assert
        assert event.id == create_event.id
        assert event.name == create_event.name
    
    def test_get_event_not_found(self, db):
        """Prueba obtener un evento que no existe"""
        # Arrange
        service = EventService(db)
        
        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            service.get_event(999)
        
        assert "no encontrado" in str(exc_info.value.message)
    
    def test_get_all_events(self, db, create_multiple_events):
        """Prueba listar todos los eventos"""
        # Arrange
        service = EventService(db)
        
        # Act
        events = service.get_all_events()
        
        # Assert
        assert len(events) == 5
        assert all(event.id is not None for event in events)
    
    def test_get_all_events_pagination(self, db, create_multiple_events):
        """Prueba paginación de eventos"""
        # Arrange
        service = EventService(db)
        
        # Act
        events_page1 = service.get_all_events(skip=0, limit=2)
        events_page2 = service.get_all_events(skip=2, limit=2)
        
        # Assert
        assert len(events_page1) == 2
        assert len(events_page2) == 2
        assert events_page1[0].id != events_page2[0].id
    
    def test_update_event(self, db, create_event):
        """Prueba actualizar un evento"""
        # Arrange
        service = EventService(db)
        update_data = EventUpdate(name="Evento Actualizado", capacity=150)
        
        # Act
        updated_event = service.update_event(create_event.id, update_data)
        
        # Assert
        assert updated_event.name == "Evento Actualizado"
        assert updated_event.capacity == 150
        assert updated_event.location == create_event.location  # No cambió
    
    def test_delete_event(self, db, create_event):
        """Prueba eliminar un evento"""
        # Arrange
        service = EventService(db)
        event_id = create_event.id
        
        # Act
        result = service.delete_event(event_id)
        
        # Assert
        assert result is True
        with pytest.raises(NotFoundException):
            service.get_event(event_id)
    
    def test_get_available_capacity(self, db, create_event):
        """Prueba calcular capacidad disponible"""
        # Arrange
        service = EventService(db)
        
        # Act
        available = service.get_available_capacity(create_event.id)
        
        # Assert
        assert available == create_event.capacity
    
    def test_get_event_statistics(self, db, create_event):
        """Prueba obtener estadísticas de un evento"""
        # Arrange
        service = EventService(db)
        
        # Act
        stats = service.get_event_statistics(create_event.id)
        
        # Assert
        assert stats.event_id == create_event.id
        assert stats.total_capacity == create_event.capacity
        assert stats.registered_participants == 0
        assert stats.available_capacity == create_event.capacity
        assert stats.occupation_percentage == 0.0