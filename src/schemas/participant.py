"""
Schemas Pydantic para Participantes
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


class ParticipantBase(BaseModel):
    """
    Schema base para participantes con campos comunes.
    """
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=200, 
        description="Nombre completo del participante"
    )
    email: EmailStr = Field(
        ..., 
        description="Email único del participante"
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20, 
        description="Teléfono del participante (opcional)"
    )
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """
        Valida el formato del número de teléfono.
        
        Acepta:
        - Números con 10-15 dígitos
        - Puede incluir espacios, guiones y +
        
        Ejemplos válidos:
        - +573001234567
        - 300-123-4567
        - 300 123 4567
        - 3001234567
        
        Args:
            v: Teléfono a validar
            
        Returns:
            Teléfono validado o None
            
        Raises:
            ValueError: Si el formato es inválido
        """
        if v:
            # Remover espacios y guiones para validar
            clean_phone = re.sub(r'[\s\-]', '', v)
            # Validar que solo tenga dígitos y opcionalmente +
            if not re.match(r'^\+?[0-9]{10,15}$', clean_phone):
                raise ValueError(
                    'Formato de teléfono inválido. '
                    'Debe contener entre 10 y 15 dígitos'
                )
        return v


class ParticipantCreate(ParticipantBase):
    """
    Schema para crear un nuevo participante.
    
    Hereda todos los campos de ParticipantBase.
    """
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "phone": "+573001234567"
            }
        }


class ParticipantUpdate(BaseModel):
    """
    Schema para actualizar un participante existente.
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    name: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=200,
        description="Nombre completo del participante"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email único del participante"
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20,
        description="Teléfono del participante"
    )
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """
        Valida el formato del número de teléfono.
        
        Args:
            v: Teléfono a validar
            
        Returns:
            Teléfono validado o None
            
        Raises:
            ValueError: Si el formato es inválido
        """
        if v:
            clean_phone = re.sub(r'[\s\-]', '', v)
            if not re.match(r'^\+?[0-9]{10,15}$', clean_phone):
                raise ValueError(
                    'Formato de teléfono inválido. '
                    'Debe contener entre 10 y 15 dígitos'
                )
        return v
    
    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez García",
                "phone": "+573009876543"
            }
        }


class ParticipantResponse(ParticipantBase):
    """
    Schema de respuesta para participantes.
    
    Incluye campos adicionales como ID y fechas de auditoría.
    """
    id: int = Field(..., description="ID único del participante")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    
    class Config:
        """Configuración de Pydantic"""
        from_attributes = True  # Permite crear desde objetos ORM
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "phone": "+573001234567",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }