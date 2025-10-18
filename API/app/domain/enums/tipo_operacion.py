from enum import Enum

class TipoOperacion(str, Enum):
    """Enum para los tipos de operación inmobiliaria"""
    VENTA = "venta"
    ALQUILER = "alquiler"
    VENTA_ALQUILER = "venta/alquiler"
