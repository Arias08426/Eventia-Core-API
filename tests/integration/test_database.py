"""
Pruebas de integración con la base de datos

Verifican que los modelos ORM funcionen correctamente.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from src.models import Event, Participant, Attendance


@pytest.mark.integration
class TestDatabaseIntegration:
    """Pruebas de integración con base de datos"""
    
    def test_event_creation_and_retrieval(self, db):
        """Prueba crear y recuperar un evento"""
        # Arrange & Act
        event = Event(
            name="Test Event",
            description="Test Description",
            location="Test Location",
            date=datetime.utcnow() + timedelta(days=1),
            capacity=50
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Assert
        retrieved = db.query(Event).filter(Event.id == event.id).first()
        assert retrieved is not None
        assert retrieved.name == "Test Event"
        assert retrieved.capacity == 50
    
    def test_participant_email_unique_constraint(self, db):
        """Prueba que el email de participante sea único"""
        # Arrange
        participant1 = Participant(
            name="Participant 1",
            email="test@example.com",
            phone="+573001234567"
        )
        db.add(participant1)
        db.commit()
        
        # Act & Assert
        participant2 = Participant(
            name="Participant 2",
            email="test@example.com",  # Email duplicado
            phone="+573009876543"
        )
        db.add(participant2)
        
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_attendance_unique_constraint(self, db, create_event, create_participant):
        """Prueba que no se pueda registrar dos veces al mismo evento"""
        # Arrange
        attendance1 = Attendance(
            event_id=create_event.id,
            participant_id=create_participant.id
        )
        db.add(attendance1)
        db.commit()
        
        # Act & Assert
        attendance2 = Attendance(
            event_id=create_event.id,
            participant_id=create_participant.id
        )
        db.add(attendance2)
        
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_cascade_delete_event(self, db, create_attendance):
        """Prueba que al eliminar evento se eliminen asistencias"""
        # Arrange
        event_id = create_attendance.event_id
        attendance_id = create_attendance.id
        
        # Act
        event = db.query(Event).filter(Event.id == event_id).first()
        db.delete(event)
        db.commit()
        
        # Assert
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        assert attendance is None
    
    def test_cascade_delete_participant(self, db, create_attendance):
        """Prueba que al eliminar participante se eliminen asistencias"""
        # Arrange
        participant_id = create_attendance.participant_id
        attendance_id = create_attendance.id
        
        # Act
        participant = db.query(Participant).filter(Participant.id == participant_id).first()
        db.delete(participant)
        db.commit()
        
        # Assert
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        assert attendance is None
    
    def test_relationship_event_to_attendances(self, db, create_attendance):
        """Prueba relación de evento a asistencias"""
        # Arrange
        event = db.query(Event).filter(Event.id == create_attendance.event_id).first()
        
        # Act & Assert
        assert len(event.attendances) == 1
        assert event.attendances[0].participant_id == create_attendance.participant_id
    
    def test_relationship_participant_to_attendances(self, db, create_attendance):
        """Prueba relación de participante a asistencias"""
        # Arrange
        participant = db.query(Participant).filter(
            Participant.id == create_attendance.participant_id
        ).first()
        
        # Act & Assert
        assert len(participant.attendances) == 1
        assert participant.attendances[0].event_id == create_attendance.event_id