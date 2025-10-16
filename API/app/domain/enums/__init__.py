"""
Capa de Dominio - Enumeraciones del sistema
Contiene los enums que representan los estados y tipos del negocio
"""

from enum import Enum
from app.domain.enums.rol import Rol


class RolEnum(str, Enum):
    """Roles de usuario en el sistema"""
    BROKER = "Broker"
    SECRETARIA = "Secretaria"
    ASESOR = "Asesor Inmobiliario"


class TipoOperacionEnum(str, Enum):
    """Tipos de operacion de propiedad"""
    VENTA = "Venta"
    ALQUILER = "Alquiler"
    ANTICRESIS = "Anticresis"


class EstadoPropiedadEnum(str, Enum):
    """Estados de una propiedad"""
    DISPONIBLE = "Disponible"
    EN_PROCESO = "En Proceso"
    RESERVADA = "Reservada"
    VENDIDA = "Vendida"
    ALQUILADA = "Alquilada"
    INACTIVA = "Inactiva"


class EstadoCitaEnum(str, Enum):
    """Estados de una cita o visita"""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"
    REPROGRAMADA = "Reprogramada"


class EstadoContratoEnum(str, Enum):
    """Estados de un contrato"""
    BORRADOR = "Borrador"
    ACTIVO = "Activo"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"


class ModalidadPagoEnum(str, Enum):
    """Modalidades de pago"""
    CONTADO = "Contado"
    CREDITO = "Credito"
    CUOTAS = "Cuotas"
    MIXTO = "Mixto"


class EstadoPagoEnum(str, Enum):
    """Estados de un pago"""
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    VENCIDO = "Vencido"
    PARCIAL = "Parcial"


class TipoDocumentoEnum(str, Enum):
    """Tipos de documento de propiedad"""
    EXCLUSIVIDAD = "Exclusividad"
    CONTRATO_VENTA = "Contrato de Venta"
    CONTRATO_ALQUILER = "Contrato de Alquiler"
    ESCRITURA = "Escritura"
    PLANO = "Plano"
    OTRO = "Otro"


class OrigenClienteEnum(str, Enum):
    """Origen del cliente - como llego"""
    WEB = "Pagina Web"
    WHATSAPP = "WhatsApp"
    REFERIDO = "Referido"
    REDES_SOCIALES = "Redes Sociales"
    LLAMADA = "Llamada Telefonica"
    VISITA_OFICINA = "Visita a Oficina"
    OTRO = "Otro"


class PeriodoDesempenoEnum(str, Enum):
    """Periodos de desempeno"""
    SEMANAL = "Semanal"
    QUINCENAL = "Quincenal"
    MENSUAL = "Mensual"
    TRIMESTRAL = "Trimestral"
    ANUAL = "Anual"
