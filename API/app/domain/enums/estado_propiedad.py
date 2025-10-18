from enum import Enum

class EstadoPropiedad(str, Enum):
    """Enum para los estados de una propiedad"""
    DISPONIBLE = "disponible"
    RESERVADA = "reservada"
    VENDIDA = "vendida"
    ALQUILADA = "alquilada"
    INACTIVA = "inactiva"
