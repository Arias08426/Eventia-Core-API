"""
Servicio para la lógica de negocio de Asistencias
"""
from sqlalchemy.orm import Session
from typing import List
from src.models.attendance import Attendance
from src.models.event import Event
from src.models.participant import Participant
from src.schemas.attendance import AttendanceCreate, AttendanceDetail
from src.exceptions.custom_exceptions import (
    NotFoundException, 
    CapacityExceededException, 
    DuplicateRegistrationException
)
from src.cache.redis_client import cache


class AttendanceService:
    """
    Servicio que contiene toda la lógica de negocio relacionada con asistencias.
    
    Responsabilidades:
    - Registrar participantes a eventos
    - Validar capacidad disponible
    - Evitar registros duplicados
    - Cancelar asistencias
    - Consultar asistencias por evento o participante
    - Gestión de caché
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    def register_attendance(self, attendance_data: AttendanceCreate) -> Attendance:
        """
        Registra un participante a un evento.
        
        Reglas de negocio:
        1. El evento debe existir
        2. El participante debe existir
        3. No puede haber registros duplicados
        4. Debe haber capacidad disponible
        
        Args:
            attendance_data: Datos de la asistencia
            
        Returns:
            Asistencia creada
            
        Raises:
            NotFoundException: Si el evento o participante no existe
            DuplicateRegistrationException: Si ya está registrado
            CapacityExceededException: Si no hay capacidad disponible
        """
        event_id = attendance_data.event_id
        participant_id = attendance_data.participant_id
        
        # Validación 1: Verificar que el evento existe
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")
        
        # Validación 2: Verificar que el participante existe
        participant = self.db.query(Participant).filter(
            Participant.id == participant_id
        ).first()
        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )
        
        # Validación 3: Verificar que no esté ya registrado
        existing = self.db.query(Attendance).filter(
            Attendance.event_id == event_id,
            Attendance.participant_id == participant_id
        ).first()
        
        if existing:
            raise DuplicateRegistrationException(
                f"El participante {participant.name} ya está registrado "
                f"en el evento {event.name}"
            )
        
        # Validación 4: Verificar capacidad disponible
        registered_count = self.db.query(Attendance).filter(
            Attendance.event_id == event_id
        ).count()
        
        if registered_count >= event.capacity:
            raise CapacityExceededException(
                f"El evento {event.name} ha alcanzado su capacidad máxima "
                f"({event.capacity} participantes)"
            )
        
        # Crear la asistencia
        attendance = Attendance(
            event_id=event_id,
            participant_id=participant_id
        )
        
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        
        # Invalidar caché relacionado
        cache.delete(f"event:stats:{event_id}")
        cache.delete(f"event:attendances:{event_id}")
        cache.delete(f"participant:attendances:{participant_id}")
        
        return attendance
    
    def cancel_attendance(self, attendance_id: int) -> bool:
        """
        Cancela una asistencia (elimina el registro).
        
        Args:
            attendance_id: ID de la asistencia
            
        Returns:
            True si se canceló correctamente
            
        Raises:
            NotFoundException: Si la asistencia no existe
        """
        attendance = self.db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()
        
        if not attendance:
            raise NotFoundException(
                f"Asistencia con ID {attendance_id} no encontrada"
            )
        
        event_id = attendance.event_id
        participant_id = attendance.participant_id
        
        self.db.delete(attendance)
        self.db.commit()
        
        # Invalidar caché
        cache.delete(f"event:stats:{event_id}")
        cache.delete(f"event:attendances:{event_id}")
        cache.delete(f"participant:attendances:{participant_id}")
        
        return True
    
    def get_event_attendances(self, event_id: int) -> List[AttendanceDetail]:
        """
        Obtiene todos los participantes registrados en un evento.
        
        Args:
            event_id: ID del evento
            
        Returns:
            Lista detallada de participantes
            
        Raises:
            NotFoundException: Si el evento no existe
        """
        # Verificar que el evento existe
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Evento con ID {event_id} no encontrado")
        
        # Intentar obtener del caché
        cache_key = f"event:attendances:{event_id}"
        cached = cache.get(cache_key)
        
        if cached:
            return [AttendanceDetail(**item) for item in cached]
        
        # Consultar BD con JOIN
        attendances = self.db.query(
            Attendance.id,
            Attendance.event_id,
            Event.name.label('event_name'),
            Attendance.participant_id,
            Participant.name.label('participant_name'),
            Participant.email.label('participant_email'),
            Attendance.registered_at
        ).join(Event).join(Participant).filter(
            Attendance.event_id == event_id
        ).all()
        
        # Convertir a lista de AttendanceDetail
        results = [
            AttendanceDetail(
                id=a.id,
                event_id=a.event_id,
                event_name=a.event_name,
                participant_id=a.participant_id,
                participant_name=a.participant_name,
                participant_email=a.participant_email,
                registered_at=a.registered_at
            )
            for a in attendances
        ]
        
        # Guardar en caché por 2 minutos
        if results:
            cache.set(cache_key, [r.model_dump() for r in results], ttl=120)
        
        return results
    
    def get_participant_attendances(self, participant_id: int) -> List[AttendanceDetail]:
        """
        Obtiene todos los eventos en los que está registrado un participante.
        
        Args:
            participant_id: ID del participante
            
        Returns:
            Lista detallada de eventos
            
        Raises:
            NotFoundException: Si el participante no existe
        """
        # Verificar que el participante existe
        participant = self.db.query(Participant).filter(
            Participant.id == participant_id
        ).first()
        if not participant:
            raise NotFoundException(
                f"Participante con ID {participant_id} no encontrado"
            )
        
        # Intentar obtener del caché
        cache_key = f"participant:attendances:{participant_id}"
        cached = cache.get(cache_key)
        
        if cached:
            return [AttendanceDetail(**item) for item in cached]
        
        # Consultar BD con JOIN
        attendances = self.db.query(
            Attendance.id,
            Attendance.event_id,
            Event.name.label('event_name'),
            Attendance.participant_id,
            Participant.name.label('participant_name'),
            Participant.email.label('participant_email'),
            Attendance.registered_at
        ).join(Event).join(Participant).filter(
            Attendance.participant_id == participant_id
        ).all()
        
        # Convertir a lista de AttendanceDetail
        results = [
            AttendanceDetail(
                id=a.id,
                event_id=a.event_id,
                event_name=a.event_name,
                participant_id=a.participant_id,
                participant_name=a.participant_name,
                participant_email=a.participant_email,
                registered_at=a.registered_at
            )
            for a in attendances
        ]
        
        # Guardar en caché por 2 minutos
        if results:
            cache.set(cache_key, [r.model_dump() for r in results], ttl=120)
        
        return results