"""
Configuracion de la aplicacion
Maneja variables de entorno y settings generales
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Configuracion general de la aplicacion"""
    
    # App Config
    app_name: str = Field(default="Sistema de Gestion Inmobiliaria", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="production", env="ENVIRONMENT")
    
    # Server Config
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Supabase Config
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")
    supabase_service_role_key: str = Field(..., env="SUPABASE_SERVICE_ROLE_KEY")
    
    # JWT Config
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Config
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    
    # Storage Config
    storage_bucket_propiedades: str = Field(default="propiedades", env="STORAGE_BUCKET_PROPIEDADES")
    storage_bucket_documentos: str = Field(default="documentos", env="STORAGE_BUCKET_DOCUMENTOS")
    
    # File Upload Limits
    max_file_size_mb: int = Field(default=10, env="MAX_FILE_SIZE_MB")
    allowed_image_extensions: List[str] = Field(
        default=["jpg", "jpeg", "png", "webp"],
        env="ALLOWED_IMAGE_EXTENSIONS"
    )
    allowed_document_extensions: List[str] = Field(
        default=["pdf"],
        env="ALLOWED_DOCUMENT_EXTENSIONS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Permitir conversion de strings con comas a listas
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name in ['cors_origins', 'allowed_image_extensions', 'allowed_document_extensions']:
                return [item.strip() for item in raw_val.split(',')]
            return raw_val


# Instancia global de settings
settings = Settings()
