"""
Pruebas end-to-end para endpoints de asistencias
"""
import pytest

from src.models import Attendance


@pytest.mark.system
class TestAttendanceAPI:
    """Pruebas E2E para API de asistencias"""

    def test_register_attendance_success(
        self, client, create_event, create_participant
    ):
        """Prueba registrar asistencia via API"""
        # Arrange
        attendance_data = {
            "event_id": create_event.id,
            "participant_id": create_participant.id,
        }

        # Act
        response = client.post("/attendances/", json=attendance_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["event_id"] == create_event.id
        assert data["participant_id"] == create_participant.id
        assert "registered_at" in data

    def test_register_attendance_event_not_found(self, client, create_participant):
        """Prueba registrar con evento inexistente"""
        # Arrange
        attendance_data = {"event_id": 999, "participant_id": create_participant.id}

        # Act
        response = client.post("/attendances/", json=attendance_data)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data or "message" in data

    def test_register_attendance_duplicate(self, client, create_attendance):
        """Prueba registrar asistencia duplicada"""
        # Arrange
        attendance_data = {
            "event_id": create_attendance.event_id,
            "participant_id": create_attendance.participant_id,
        }

        # Act
        response = client.post("/attendances/", json=attendance_data)

        # Assert
        assert response.status_code == 409
        data = response.json()
        assert "detail" in data or "error" in data

    def test_register_attendance_capacity_exceeded(
        self, client, db, create_event, create_multiple_participants
    ):
        """Prueba registrar cuando evento está lleno"""
        # Arrange - Crear evento con capacidad 2
        create_event.capacity = 2
        db.commit()

        # Registrar 2 participantes
        for i in range(2):
            attendance = Attendance(
                event_id=create_event.id,
                participant_id=create_multiple_participants[i].id,
            )
            db.add(attendance)
        db.commit()

        # Intentar registrar un tercero
        attendance_data = {
            "event_id": create_event.id,
            "participant_id": create_multiple_participants[2].id,
        }

        # Act
        response = client.post("/attendances/", json=attendance_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data or "error" in data

    def test_cancel_attendance(self, client, create_attendance):
        """Prueba cancelar asistencia"""
        # Act
        response = client.delete(f"/attendances/{create_attendance.id}")

        # Assert
        assert response.status_code == 204

    def test_get_event_attendances(self, client, create_attendance):
        """Prueba obtener participantes de un evento"""
        # Act
        response = client.get(f"/attendances/event/{create_attendance.event_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["event_id"] == create_attendance.event_id
        assert "participant_name" in data[0]
        assert "participant_email" in data[0]

    def test_get_participant_attendances(self, client, create_attendance):
        """Prueba obtener eventos de un participante"""
        # Act
        response = client.get(
            f"/attendances/participant/{create_attendance.participant_id}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["participant_id"] == create_attendance.participant_id
        assert "event_name" in data[0]

    def test_complete_flow(self, client, sample_event_data, sample_participant_data):
        """Prueba flujo completo: crear evento, participante y registrar"""
        # 1. Crear evento
        event_response = client.post("/events/", json=sample_event_data)
        assert event_response.status_code == 201
        event_id = event_response.json()["id"]

        # 2. Crear participante
        participant_response = client.post(
            "/participants/", json=sample_participant_data
        )
        assert participant_response.status_code == 201
        participant_id = participant_response.json()["id"]

        # 3. Registrar asistencia
        attendance_data = {"event_id": event_id, "participant_id": participant_id}
        attendance_response = client.post("/attendances/", json=attendance_data)
        assert attendance_response.status_code == 201

        # 4. Verificar estadísticas
        stats_response = client.get(f"/events/{event_id}/statistics")
        assert stats_response.status_code == 200
        stats = stats_response.json()
        assert stats["registered_participants"] == 1
        assert stats["available_capacity"] == sample_event_data["capacity"] - 1
