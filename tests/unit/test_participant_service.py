"""
Pruebas unitarias para ParticipantService

Estas pruebas verifican la lógica de negocio de participantes.
"""
import pytest
from src.services.participant_service import ParticipantService
from src.schemas.participant import ParticipantCreate, ParticipantUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


@pytest.mark.unit
class TestParticipantService:
    """Pruebas para el servicio de participantes"""
    
    def test_create_participant(self, db, sample_participant_data):
        """Prueba crear un participante correctamente"""
        # Arrange
        service = ParticipantService(db)
        participant_data = ParticipantCreate(**sample_participant_data)
        
        # Act
        participant = service.create_participant(participant_data)
        
        # Assert
        assert participant.id is not None
        assert participant.name == sample_participant_data["name"]
        assert participant.email == sample_participant_data["email"]
        assert participant.created_at is not None
    
    def test_create_participant_duplicate_email(self, db, create_participant):
        """Prueba crear participante con email duplicado"""
        # Arrange
        service = ParticipantService(db)
        duplicate_data = ParticipantCreate(
            name="Otro Nombre",
            email=create_participant.email,  # Email duplicado
            phone="+573009999999"
        )
        
        # Act & Assert
        with pytest.raises(AlreadyExistsException) as exc_info:
            service.create_participant(duplicate_data)
        
        assert "ya está registrado" in str(exc_info.value.message)
    
    def test_get_participant_success(self, db, create_participant):
        """Prueba obtener un participante existente"""
        # Arrange
        service = ParticipantService(db)
        
        # Act
        participant = service.get_participant(create_participant.id)
        
        # Assert
        assert participant.id == create_participant.id
        assert participant.email == create_participant.email
    
    def test_get_participant_not_found(self, db):
        """Prueba obtener un participante que no existe"""
        # Arrange
        service = ParticipantService(db)
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            service.get_participant(999)
    
    def test_get_participant_by_email(self, db, create_participant):
        """Prueba buscar participante por email"""
        # Arrange
        service = ParticipantService(db)
        
        # Act
        participant = service.get_participant_by_email(create_participant.email)
        
        # Assert
        assert participant is not None
        assert participant.id == create_participant.id
    
    def test_get_all_participants(self, db, create_multiple_participants):
        """Prueba listar todos los participantes"""
        # Arrange
        service = ParticipantService(db)
        
        # Act
        participants = service.get_all_participants()
        
        # Assert
        assert len(participants) == 5
    
    def test_update_participant(self, db, create_participant):
        """Prueba actualizar un participante"""
        # Arrange
        service = ParticipantService(db)
        update_data = ParticipantUpdate(name="Nombre Actualizado")
        
        # Act
        updated = service.update_participant(create_participant.id, update_data)
        
        # Assert
        assert updated.name == "Nombre Actualizado"
        assert updated.email == create_participant.email  # No cambió
    
    def test_update_participant_email_duplicate(self, db, create_multiple_participants):
        """Prueba actualizar email a uno que ya existe"""
        # Arrange
        service = ParticipantService(db)
        participant1 = create_multiple_participants[0]
        participant2 = create_multiple_participants[1]
        
        update_data = ParticipantUpdate(email=participant2.email)
        
        # Act & Assert
        with pytest.raises(AlreadyExistsException):
            service.update_participant(participant1.id, update_data)
    
    def test_delete_participant(self, db, create_participant):
        """Prueba eliminar un participante"""
        # Arrange
        service = ParticipantService(db)
        participant_id = create_participant.id
        
        # Act
        result = service.delete_participant(participant_id)
        
        # Assert
        assert result is True
        with pytest.raises(NotFoundException):
            service.get_participant(participant_id)