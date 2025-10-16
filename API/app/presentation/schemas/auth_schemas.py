"""
Schemas de Autenticación
DTOs para requests y responses de autenticación
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ===== REQUEST SCHEMAS =====

class RegisterRequest(BaseModel):
    """Schema para registro de nuevos usuarios"""
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["broker@inmobiliaria.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Contraseña (mínimo 8 caracteres)",
        examples=["Password123!"]
    )
    password_confirm: str = Field(
        ...,
        description="Confirmación de contraseña",
        examples=["Password123!"]
    )
    rol: str = Field(
        ...,
        description="Rol del usuario: BROKER, SECRETARIA, ASESOR",
        examples=["ASESOR"]
    )
    empleado_id: Optional[str] = Field(
        None,
        description="ID del empleado asociado (opcional)"
    )
    
    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v, info):
        """Valida que las contraseñas coincidan"""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Las contraseñas no coinciden")
        return v
    
    @field_validator("rol")
    @classmethod
    def validate_rol(cls, v):
        """Valida que el rol sea válido"""
        valid_roles = ["BROKER", "SECRETARIA", "ASESOR"]
        if v.upper() not in valid_roles:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(valid_roles)}")
        return v.upper()
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """Valida que la contraseña sea segura"""
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe contener al menos una minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v


class LoginRequest(BaseModel):
    """Schema para login de usuarios"""
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["broker@inmobiliaria.com"]
    )
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        examples=["Password123!"]
    )


class RefreshTokenRequest(BaseModel):
    """Schema para refrescar token"""
    
    refresh_token: str = Field(
        ...,
        description="Refresh token válido"
    )


# ===== RESPONSE SCHEMAS =====

class TokenResponse(BaseModel):
    """Schema para respuesta con tokens"""
    
    access_token: str = Field(
        ...,
        description="Token de acceso JWT"
    )
    refresh_token: str = Field(
        ...,
        description="Token de refresco JWT"
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo de token"
    )
    expires_in: int = Field(
        ...,
        description="Tiempo de expiración en segundos"
    )


class UserResponse(BaseModel):
    """Schema para respuesta con datos del usuario"""
    
    id: str = Field(
        ...,
        description="ID del usuario"
    )
    email: str = Field(
        ...,
        description="Email del usuario"
    )
    rol: str = Field(
        ...,
        description="Rol del usuario"
    )
    empleado_id: Optional[str] = Field(
        None,
        description="ID del empleado asociado"
    )
    activo: bool = Field(
        ...,
        description="Estado del usuario"
    )
    fecha_creacion: datetime = Field(
        ...,
        description="Fecha de creación"
    )
    ultimo_acceso: Optional[datetime] = Field(
        None,
        description="Fecha del último acceso"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "broker@inmobiliaria.com",
                "rol": "BROKER",
                "empleado_id": None,
                "activo": True,
                "fecha_creacion": "2024-01-15T10:30:00",
                "ultimo_acceso": "2024-01-20T14:45:00"
            }
        }


class LoginResponse(BaseModel):
    """Schema para respuesta completa de login"""
    
    user: UserResponse = Field(
        ...,
        description="Datos del usuario"
    )
    tokens: TokenResponse = Field(
        ...,
        description="Tokens de autenticación"
    )
    message: str = Field(
        default="Login exitoso",
        description="Mensaje de respuesta"
    )


class RegisterResponse(BaseModel):
    """Schema para respuesta de registro"""
    
    user: UserResponse = Field(
        ...,
        description="Datos del usuario creado"
    )
    message: str = Field(
        default="Usuario registrado exitosamente",
        description="Mensaje de respuesta"
    )
