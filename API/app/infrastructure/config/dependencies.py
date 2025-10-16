"""
Dependency Injection
Configuracion de dependencias para FastAPI
"""

from typing import Generator
from supabase import Client
from app.infrastructure.database.supabase_client import get_supabase, get_supabase_admin
from app.infrastructure.config.settings import settings


def get_db() -> Generator[Client, None, None]:
    """
    Dependency que proporciona una instancia del cliente de Supabase
    """
    client = get_supabase()
    try:
        yield client
    finally:
        # Cleanup si es necesario
        pass


def get_admin_db() -> Generator[Client, None, None]:
    """
    Dependency que proporciona una instancia admin del cliente de Supabase
    Solo para operaciones que requieren privilegios elevados
    """ 
    client = get_supabase_admin()
    try:
        yield client
    finally:
        pass


def get_settings():
    """
    Dependency que proporciona acceso a la configuracion
    """
    return settings
