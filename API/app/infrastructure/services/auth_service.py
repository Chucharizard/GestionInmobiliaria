"""
Servicio de Autenticación
Maneja hashing de contraseñas y generación de tokens JWT
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.infrastructure.config.settings import settings


class AuthService:
    """Servicio para manejar autenticación y tokens JWT"""
    
    def __init__(self):
        # Configuración de bcrypt para hashing de passwords
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """
        Hashea una contraseña usando bcrypt
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash almacenado
            
        Returns:
            True si coinciden, False si no
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(
        self, 
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Crea un token JWT de acceso
        
        Args:
            data: Datos a codificar en el token (user_id, email, rol)
            expires_delta: Tiempo de expiración personalizado
            
        Returns:
            Token JWT codificado
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        
        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key, 
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    def create_refresh_token(
        self, 
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Crea un token JWT de refresh
        
        Args:
            data: Datos a codificar en el token (user_id)
            expires_delta: Tiempo de expiración personalizado
            
        Returns:
            Token JWT de refresh codificado
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.refresh_token_expire_days
            )
        
        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key, 
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decodifica y valida un token JWT
        
        Args:
            token: Token JWT a decodificar
            
        Returns:
            Payload del token si es válido, None si es inválido
        """
        try:
            payload = jwt.decode(
                token, 
                settings.secret_key, 
                algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None
    
    def create_tokens(self, user_id: str, email: str, rol: str) -> dict:
        """
        Crea un par de tokens (access + refresh) para un usuario
        
        Args:
            user_id: ID del usuario
            email: Email del usuario
            rol: Rol del usuario (BROKER, SECRETARIA, ASESOR)
            
        Returns:
            Dict con access_token, refresh_token y token_type
        """
        # Datos que irán en el token de acceso
        access_token_data = {
            "sub": user_id,
            "email": email,
            "rol": rol
        }
        
        # Datos que irán en el token de refresh (solo ID)
        refresh_token_data = {
            "sub": user_id
        }
        
        access_token = self.create_access_token(access_token_data)
        refresh_token = self.create_refresh_token(refresh_token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


# Instancia singleton del servicio
auth_service = AuthService()
