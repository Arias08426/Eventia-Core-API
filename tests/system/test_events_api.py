"""
Pruebas end-to-end para endpoints de eventos

Estas pruebas verifican el flujo completo desde HTTP hasta BD.
"""
import pytest
from datetime import datetime, timedelta


@pytest.mark.system
class TestEventsAPI:
    """Pruebas E2E para API de eventos"""
    
    def test_create_event_success(self, client, sample_event_data):
        """Prueba crear evento via API"""
        # Act
        response = client.post("/events/", json=sample_event_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_event_data["name"]
        assert data["id"] is not None
        assert "created_at" in data
    
    def test_create_event_invalid_date(self, client, sample_event_data):
        """Prueba crear evento con fecha pasada"""
        # Arrange
        sample_event_data["date"] = (datetime.utcnow() - timedelta(days=1)).isoformat()
        
        # Act
        response = client.post("/events/", json=sample_event_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_get_all_events(self, client, create_multiple_events):
        """Prueba listar todos los eventos"""
        # Act
        response = client.get("/events/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert all("id" in event for event in data)
    
    def test_get_event_by_id(self, client, create_event):
        """Prueba obtener evento específico"""
        # Act
        response = client.get(f"/events/{create_event.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == create_event.id
        assert data["name"] == create_event.name
    
    def test_get_event_not_found(self, client):
        """Prueba obtener evento inexistente"""
        # Act
        response = client.get("/events/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data or "error" in data
    
    def test_update_event(self, client, create_event):
        """Prueba actualizar evento"""
        # Arrange
        update_data = {
            "name": "Evento Actualizado",
            "capacity": 200
        }
        
        # Act
        response = client.put(f"/events/{create_event.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Evento Actualizado"
        assert data["capacity"] == 200
    
    def test_delete_event(self, client, create_event):
        """Prueba eliminar evento"""
        # Act
        response = client.delete(f"/events/{create_event.id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verificar que ya no existe
        get_response = client.get(f"/events/{create_event.id}")
        assert get_response.status_code == 404
    
    def test_get_event_statistics(self, client, create_event):
        """Prueba obtener estadísticas de evento"""
        # Act
        response = client.get(f"/events/{create_event.id}/statistics")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["event_id"] == create_event.id
        assert data["total_capacity"] == create_event.capacity
        assert data["registered_participants"] == 0
        assert data["occupation_percentage"] == 0.0
    
    def test_pagination(self, client, create_multiple_events):
        """Prueba paginación de eventos"""
        # Act
        response = client.get("/events/?skip=0&limit=2")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2