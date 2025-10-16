"""
Cliente de Supabase
Configuracion y conexion con la base de datos
"""

from supabase import create_client, Client
from app.infrastructure.config.settings import settings


class SupabaseClient:
    """Cliente singleton para Supabase"""
    
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Obtiene la instancia del cliente de Supabase"""
        if cls._instance is None:
            cls._instance = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._instance
    
    @classmethod
    def get_admin_client(cls) -> Client:
        """Obtiene una instancia con privilegios de servicio (admin)"""
        return create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )


# Funcion helper para obtener el cliente
def get_supabase() -> Client:
    """Dependency para FastAPI - retorna el cliente de Supabase"""
    return SupabaseClient.get_client()


def get_supabase_admin() -> Client:
    """Dependency para FastAPI - retorna el cliente admin de Supabase"""
    return SupabaseClient.get_admin_client()
