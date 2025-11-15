"""
Pruebas unitarias para AttendanceService

Estas pruebas verifican las reglas de negocio de asistencias.
"""
import pytest
from src.services.attendance_service import AttendanceService
from src.schemas.attendance import AttendanceCreate
from src.exceptions.custom_exceptions import (
    NotFoundException,
    CapacityExceededException,
    DuplicateRegistrationException
)
from src.models import Attendance


@pytest.mark.unit
class TestAttendanceService:
    """Pruebas para el servicio de asistencias"""
    
    def test_register_attendance_success(self, db, create_event, create_participant):
        """Prueba registrar una asistencia correctamente"""
        # Arrange
        service = AttendanceService(db)
        attendance_data = AttendanceCreate(
            event_id=create_event.id,
            participant_id=create_participant.id
        )
        
        # Act
        attendance = service.register_attendance(attendance_data)
        
        # Assert
        assert attendance.id is not None
        assert attendance.event_id == create_event.id
        assert attendance.participant_id == create_participant.id
        assert attendance.registered_at is not None
    
    def test_register_attendance_event_not_found(self, db, create_participant):
        """Prueba registrar asistencia con evento inexistente"""
        # Arrange
        service = AttendanceService(db)
        attendance_data = AttendanceCreate(
            event_id=999,
            participant_id=create_participant.id
        )
        
        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            service.register_attendance(attendance_data)
        
        assert "Evento" in str(exc_info.value.message)
    
    def test_register_attendance_participant_not_found(self, db, create_event):
        """Prueba registrar asistencia con participante inexistente"""
        # Arrange
        service = AttendanceService(db)
        attendance_data = AttendanceCreate(
            event_id=create_event.id,
            participant_id=999
        )
        
        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            service.register_attendance(attendance_data)
        
        assert "Participante" in str(exc_info.value.message)
    
    def test_register_attendance_duplicate(self, db, create_attendance):
        """Prueba registrar asistencia duplicada"""
        # Arrange
        service = AttendanceService(db)
        attendance_data = AttendanceCreate(
            event_id=create_attendance.event_id,
            participant_id=create_attendance.participant_id
        )
        
        # Act & Assert
        with pytest.raises(DuplicateRegistrationException) as exc_info:
            service.register_attendance(attendance_data)
        
        assert "ya está registrado" in str(exc_info.value.message)
    
    def test_register_attendance_capacity_exceeded(self, db, create_event, create_multiple_participants):
        """Prueba registrar asistencia cuando el evento está lleno"""
        # Arrange
        service = AttendanceService(db)
        
        # Crear evento con capacidad de 2
        create_event.capacity = 2
        db.commit()
        
        # Registrar 2 participantes (llenar evento)
        for i in range(2):
            attendance = Attendance(
                event_id=create_event.id,
                participant_id=create_multiple_participants[i].id
            )
            db.add(attendance)
        db.commit()
        
        # Intentar registrar un tercero
        attendance_data = AttendanceCreate(
            event_id=create_event.id,
            participant_id=create_multiple_participants[2].id
        )
        
        # Act & Assert
        with pytest.raises(CapacityExceededException) as exc_info:
            service.register_attendance(attendance_data)
        
        assert "capacidad máxima" in str(exc_info.value.message)
    
    def test_cancel_attendance(self, db, create_attendance):
        """Prueba cancelar una asistencia"""
        # Arrange
        service = AttendanceService(db)
        attendance_id = create_attendance.id
        
        # Act
        result = service.cancel_attendance(attendance_id)
        
        # Assert
        assert result is True
        assert db.query(Attendance).filter(Attendance.id == attendance_id).first() is None
    
    def test_cancel_attendance_not_found(self, db):
        """Prueba cancelar asistencia inexistente"""
        # Arrange
        service = AttendanceService(db)
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            service.cancel_attendance(999)
    
    def test_get_event_attendances(self, db, create_attendance):
        """Prueba obtener participantes de un evento"""
        # Arrange
        service = AttendanceService(db)
        
        # Act
        attendances = service.get_event_attendances(create_attendance.event_id)
        
        # Assert
        assert len(attendances) == 1
        assert attendances[0].event_id == create_attendance.event_id
        assert attendances[0].participant_name is not None
    
    def test_get_participant_attendances(self, db, create_attendance):
        """Prueba obtener eventos de un participante"""
        # Arrange
        service = AttendanceService(db)
        
        # Act
        attendances = service.get_participant_attendances(create_attendance.participant_id)
        
        # Assert
        assert len(attendances) == 1
        assert attendances[0].participant_id == create_attendance.participant_id
        assert attendances[0].event_name is not None