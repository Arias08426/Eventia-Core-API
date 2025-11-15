"""
Configuración compartida para todas las pruebas
"""
import os
import sys

# Agregar el directorio raíz al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Agregar src al path ANTES de cualquier import
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from datetime import datetime, timedelta  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

# AHORA sí importar (después de agregar al path)
from src.database.connection import Base, get_db  # noqa: E402
from src.main import app  # noqa: E402
from src.models.attendance import Attendance  # noqa: E402
from src.models.event import Event  # noqa: E402
from src.models.participant import Participant  # noqa: E402

# Usar DATABASE_URL del environment, si no está disponible usar SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)

# Para SQLite en desarrollo local
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Para MySQL en CI/CD
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Sesión de base de datos para pruebas"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Cliente de pruebas de FastAPI"""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_event_data():
    """Datos de ejemplo para evento"""
    return {
        "name": "Conferencia Tech 2024",
        "description": "Una conferencia sobre tecnología",
        "location": "Centro de Convenciones",
        "date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "capacity": 100,
    }


@pytest.fixture
def sample_participant_data():
    """Datos de ejemplo para participante"""
    return {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "+573001234567",
    }


@pytest.fixture
def create_event(db, sample_event_data):
    """Crea un evento en la BD"""
    event = Event(
        name=sample_event_data["name"],
        description=sample_event_data["description"],
        location=sample_event_data["location"],
        date=datetime.fromisoformat(sample_event_data["date"]),
        capacity=sample_event_data["capacity"],
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@pytest.fixture
def create_participant(db, sample_participant_data):
    """Crea un participante en la BD"""
    participant = Participant(
        name=sample_participant_data["name"],
        email=sample_participant_data["email"],
        phone=sample_participant_data["phone"],
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


@pytest.fixture
def create_attendance(db, create_event, create_participant):
    """Crea una asistencia en la BD"""
    attendance = Attendance(
        event_id=create_event.id, participant_id=create_participant.id
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


@pytest.fixture
def create_multiple_events(db):
    """Crea múltiples eventos"""
    events = []
    for i in range(5):
        event = Event(
            name=f"Evento {i+1}",
            description=f"Descripción del evento {i+1}",
            location=f"Ubicación {i+1}",
            date=datetime.utcnow() + timedelta(days=i + 1),
            capacity=50 + (i * 10),
        )
        db.add(event)
        events.append(event)
    db.commit()
    for event in events:
        db.refresh(event)
    return events


@pytest.fixture
def create_multiple_participants(db):
    """Crea múltiples participantes"""
    participants = []
    for i in range(5):
        participant = Participant(
            name=f"Participante {i+1}",
            email=f"participante{i+1}@example.com",
            phone=f"+5730012345{i}",
        )
        db.add(participant)
        participants.append(participant)
    db.commit()
    for participant in participants:
        db.refresh(participant)
    return participants
