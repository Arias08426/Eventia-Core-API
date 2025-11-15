"""
Pruebas end-to-end para endpoints de participantes
"""
import pytest


@pytest.mark.system
class TestParticipantsAPI:
    """Pruebas E2E para API de participantes"""
    
    def test_create_participant_success(self, client, sample_participant_data):
        """Prueba crear participante via API"""
        # Act
        response = client.post("/participants/", json=sample_participant_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_participant_data["name"]
        assert data["email"] == sample_participant_data["email"]
        assert data["id"] is not None
    
    def test_create_participant_duplicate_email(self, client, create_participant):
        """Prueba crear participante con email duplicado"""
        # Arrange
        duplicate_data = {
            "name": "Otro Nombre",
            "email": create_participant.email,
            "phone": "+573009999999"
        }
        
        # Act
        response = client.post("/participants/", json=duplicate_data)
        
        # Assert
        assert response.status_code == 409
        data = response.json()
        assert "detail" in data or "error" in data
    
    def test_create_participant_invalid_email(self, client):
        """Prueba crear participante con email inválido"""
        # Arrange
        invalid_data = {
            "name": "Test User",
            "email": "invalid-email",
            "phone": "+573001234567"
        }
        
        # Act
        response = client.post("/participants/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_get_all_participants(self, client, create_multiple_participants):
        """Prueba listar todos los participantes"""
        # Act
        response = client.get("/participants/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
    
    def test_get_participant_by_id(self, client, create_participant):
        """Prueba obtener participante específico"""
        # Act
        response = client.get(f"/participants/{create_participant.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == create_participant.id
        assert data["email"] == create_participant.email
    
    def test_get_participant_not_found(self, client):
        """Prueba obtener participante inexistente"""
        # Act
        response = client.get("/participants/999")
        
        # Assert
        assert response.status_code == 404
    
    def test_update_participant(self, client, create_participant):
        """Prueba actualizar participante"""
        # Arrange
        update_data = {
            "name": "Nombre Actualizado",
            "phone": "+573009876543"
        }
        
        # Act
        response = client.put(f"/participants/{create_participant.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Nombre Actualizado"
        assert data["phone"] == "+573009876543"
        assert data["email"] == create_participant.email  # No cambió
    
    def test_delete_participant(self, client, create_participant):
        """Prueba eliminar participante"""
        # Act
        response = client.delete(f"/participants/{create_participant.id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verificar que ya no existe
        get_response = client.get(f"/participants/{create_participant.id}")
        assert get_response.status_code == 404