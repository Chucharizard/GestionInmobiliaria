"""
Casos de Uso de Autenticación
Lógica de negocio para autenticación y gestión de usuarios
"""

from typing import Optional
from datetime import datetime

from app.domain.enums.rol import Rol
from app.domain.exceptions import (
    EmailYaExisteException,
    CredencialesInvalidasException,
    TokenInvalidoException,
    UsuarioNoEncontradoException
)
from app.infrastructure.services.auth_service import auth_service
from app.infrastructure.repositories.user_repository import user_repository
from app.infrastructure.config.settings import settings


class RegisterUserUseCase:
    """Caso de uso para registrar un nuevo usuario"""
    
    async def execute(
        self, 
        email: str, 
        password: str, 
        rol: str,
        empleado_id: Optional[str] = None
    ) -> dict:
        """
        Registra un nuevo usuario en el sistema
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            rol: Rol del usuario (BROKER, SECRETARIA, ASESOR)
            empleado_id: ID del empleado asociado (opcional)
            
        Returns:
            Diccionario con datos del usuario creado
            
        Raises:
            EmailYaExisteException: Si el email ya está registrado
        """
        # Verificar si el email ya existe
        if await user_repository.exists_by_email(email):
            raise EmailYaExisteException(email)
        
        # Hashear la contraseña
        password_hash = auth_service.hash_password(password)
        
        # Crear el usuario
        usuario = await user_repository.create(
            email=email,
            password_hash=password_hash,
            rol=Rol(rol),
            empleado_id=empleado_id
        )
        
        return {
            "id": usuario["id"],
            "email": usuario["email"],
            "rol": usuario["rol"],
            "empleado_id": usuario.get("empleado_id"),
            "activo": usuario["activo"],
            "fecha_creacion": usuario["fecha_creacion"],
            "ultimo_acceso": usuario.get("ultimo_acceso")
        }


class LoginUseCase:
    """Caso de uso para iniciar sesión"""
    
    async def execute(self, email: str, password: str) -> dict:
        """
        Autentica a un usuario y genera tokens
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Diccionario con datos del usuario y tokens
            
        Raises:
            CredencialesInvalidasException: Si las credenciales son incorrectas
        """
        # Buscar usuario por email (CON contraseña para verificación)
        usuario = await user_repository.find_by_email_with_password(email)
        
        if not usuario:
            raise CredencialesInvalidasException()
        
        # Verificar contraseña
        if not auth_service.verify_password(password, usuario["password_hash"]):
            raise CredencialesInvalidasException()
        
        # Verificar que el usuario esté activo
        if not usuario["activo"]:
            raise CredencialesInvalidasException("Usuario inactivo")
        
        # Actualizar último acceso
        await user_repository.update_last_login(usuario["id"])
        
        # Generar tokens
        tokens = auth_service.create_tokens(
            user_id=usuario["id"],
            email=usuario["email"],
            rol=usuario["rol"]
        )
        
        return {
            "user": {
                "id": usuario["id"],
                "email": usuario["email"],
                "rol": usuario["rol"],
                "empleado_id": usuario.get("empleado_id"),
                "activo": usuario["activo"],
                "fecha_creacion": usuario["fecha_creacion"],
                "ultimo_acceso": datetime.utcnow()
            },
            "tokens": {
                **tokens,
                "expires_in": settings.access_token_expire_minutes * 60
            }
        }


class RefreshTokenUseCase:
    """Caso de uso para refrescar token de acceso"""
    
    async def execute(self, refresh_token: str) -> dict:
        """
        Genera un nuevo access token usando un refresh token válido
        
        Args:
            refresh_token: Refresh token JWT
            
        Returns:
            Diccionario con nuevos tokens
            
        Raises:
            TokenInvalidoException: Si el refresh token es inválido
        """
        # Decodificar y validar el token
        payload = auth_service.decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise TokenInvalidoException()
        
        # Obtener el usuario
        user_id = payload.get("sub")
        if not user_id:
            raise TokenInvalidoException()
        
        usuario = await user_repository.find_by_id(user_id)
        
        if not usuario:
            raise UsuarioNoEncontradoException()
        
        if not usuario["activo"]:
            raise TokenInvalidoException("Usuario inactivo")
        
        # Generar nuevos tokens
        tokens = auth_service.create_tokens(
            user_id=usuario["id"],
            email=usuario["email"],
            rol=usuario["rol"]
        )
        
        return {
            **tokens,
            "expires_in": settings.access_token_expire_minutes * 60
        }


class GetCurrentUserUseCase:
    """Caso de uso para obtener el usuario actual desde un token"""
    
    async def execute(self, token: str) -> dict:
        """
        Obtiene los datos del usuario actual desde un access token
        
        Args:
            token: Access token JWT
            
        Returns:
            Diccionario con datos del usuario
            
        Raises:
            TokenInvalidoException: Si el token es inválido
            UsuarioNoEncontradoException: Si el usuario no existe
        """
        # Decodificar y validar el token
        payload = auth_service.decode_token(token)
        
        if not payload or payload.get("type") != "access":
            raise TokenInvalidoException()
        
        # Obtener el usuario
        user_id = payload.get("sub")
        if not user_id:
            raise TokenInvalidoException()
        
        usuario = await user_repository.find_by_id(user_id)
        
        if not usuario:
            raise UsuarioNoEncontradoException()
        
        if not usuario["activo"]:
            raise TokenInvalidoException("Usuario inactivo")
        
        return {
            "id": usuario["id"],
            "email": usuario["email"],
            "rol": usuario["rol"],
            "empleado_id": usuario.get("empleado_id"),
            "activo": usuario["activo"],
            "fecha_creacion": usuario["fecha_creacion"],
            "ultimo_acceso": usuario.get("ultimo_acceso")
        }


# Instancias de los casos de uso
register_user_use_case = RegisterUserUseCase()
login_use_case = LoginUseCase()
refresh_token_use_case = RefreshTokenUseCase()
get_current_user_use_case = GetCurrentUserUseCase()
