"""
Entidad Propiedad - Representa una propiedad inmobiliaria
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from app.domain.value_objects import CI, Dinero, Porcentaje
from app.domain.enums import TipoOperacionEnum, EstadoPropiedadEnum
from app.domain.exceptions import BusinessRuleViolationException, InvalidStateTransitionException


@dataclass
class Propiedad:
    """
    Propiedad inmobiliaria para venta o alquiler
    """
    id_propiedad: UUID
    id_direccion: UUID
    ci_propietario: CI
    codigo_publico: str
    titulo: str
    descripcion: str
    precio_publicado: Dinero
    superficie: float  # en metros cuadrados
    tipo_operacion: TipoOperacionEnum
    estado: EstadoPropiedadEnum
    id_usuario_captador: UUID
    id_usuario_colocador: Optional[UUID]
    fecha_captacion: date
    fecha_publicacion: Optional[date]
    fecha_cierre: Optional[date]
    porcentaje_captacion: Porcentaje
    porcentaje_colocacion: Porcentaje
    
    @staticmethod
    def crear_nueva(
        id_direccion: UUID,
        ci_propietario: CI,
        codigo_publico: str,
        titulo: str,
        descripcion: str,
        precio_publicado: Dinero,
        superficie: float,
        tipo_operacion: TipoOperacionEnum,
        id_usuario_captador: UUID,
        porcentaje_captacion: Porcentaje,
        porcentaje_colocacion: Porcentaje
    ) -> 'Propiedad':
        """Factory method para crear una nueva propiedad"""
        if superficie <= 0:
            raise BusinessRuleViolationException("La superficie debe ser mayor a 0")
        
        return Propiedad(
            id_propiedad=uuid4(),
            id_direccion=id_direccion,
            ci_propietario=ci_propietario,
            codigo_publico=codigo_publico,
            titulo=titulo,
            descripcion=descripcion,
            precio_publicado=precio_publicado,
            superficie=superficie,
            tipo_operacion=tipo_operacion,
            estado=EstadoPropiedadEnum.DISPONIBLE,
            id_usuario_captador=id_usuario_captador,
            id_usuario_colocador=None,
            fecha_captacion=date.today(),
            fecha_publicacion=None,
            fecha_cierre=None,
            porcentaje_captacion=porcentaje_captacion,
            porcentaje_colocacion=porcentaje_colocacion
        )
    
    def publicar(self) -> None:
        """Publica la propiedad para que sea visible"""
        if self.estado != EstadoPropiedadEnum.DISPONIBLE:
            raise InvalidStateTransitionException(
                "Propiedad", 
                self.estado.value, 
                "Publicada"
            )
        self.fecha_publicacion = date.today()
    
    def marcar_en_proceso(self) -> None:
        """Marca la propiedad como en proceso de negociacion"""
        if self.estado not in [EstadoPropiedadEnum.DISPONIBLE]:
            raise InvalidStateTransitionException(
                "Propiedad",
                self.estado.value,
                EstadoPropiedadEnum.EN_PROCESO.value
            )
        self.estado = EstadoPropiedadEnum.EN_PROCESO
    
    def reservar(self) -> None:
        """Reserva la propiedad"""
        if self.estado not in [EstadoPropiedadEnum.DISPONIBLE, EstadoPropiedadEnum.EN_PROCESO]:
            raise InvalidStateTransitionException(
                "Propiedad",
                self.estado.value,
                EstadoPropiedadEnum.RESERVADA.value
            )
        self.estado = EstadoPropiedadEnum.RESERVADA
    
    def cerrar_operacion(self, id_usuario_colocador: UUID, precio_cierre: Optional[Dinero] = None) -> None:
        """Cierra la operacion (venta o alquiler)"""
        if self.estado == EstadoPropiedadEnum.VENDIDA or self.estado == EstadoPropiedadEnum.ALQUILADA:
            raise BusinessRuleViolationException("La propiedad ya fue cerrada")
        
        self.id_usuario_colocador = id_usuario_colocador
        self.fecha_cierre = date.today()
        
        # Actualizar precio si se nego diferente
        if precio_cierre:
            self.precio_publicado = precio_cierre
        
        # Cambiar estado segun tipo de operacion
        if self.tipo_operacion == TipoOperacionEnum.VENTA:
            self.estado = EstadoPropiedadEnum.VENDIDA
        elif self.tipo_operacion == TipoOperacionEnum.ALQUILER:
            self.estado = EstadoPropiedadEnum.ALQUILADA
    
    def desactivar(self) -> None:
        """Desactiva la propiedad"""
        if self.estado in [EstadoPropiedadEnum.VENDIDA, EstadoPropiedadEnum.ALQUILADA]:
            raise BusinessRuleViolationException("No se puede desactivar una propiedad cerrada")
        self.estado = EstadoPropiedadEnum.INACTIVA
    
    def reactivar(self) -> None:
        """Reactiva la propiedad"""
        if self.estado == EstadoPropiedadEnum.INACTIVA:
            self.estado = EstadoPropiedadEnum.DISPONIBLE
    
    def actualizar_precio(self, nuevo_precio: Dinero) -> None:
        """Actualiza el precio de la propiedad"""
        if self.estado in [EstadoPropiedadEnum.VENDIDA, EstadoPropiedadEnum.ALQUILADA]:
            raise BusinessRuleViolationException("No se puede cambiar el precio de una propiedad cerrada")
        self.precio_publicado = nuevo_precio
    
    def calcular_comision_captacion(self, precio_final: Optional[Dinero] = None) -> Dinero:
        """Calcula la comision del captador"""
        precio_base = precio_final if precio_final else self.precio_publicado
        monto_comision = self.porcentaje_captacion.aplicar_a(precio_base.monto)
        return Dinero(monto_comision, precio_base.moneda)
    
    def calcular_comision_colocacion(self, precio_final: Optional[Dinero] = None) -> Dinero:
        """Calcula la comision del colocador"""
        precio_base = precio_final if precio_final else self.precio_publicado
        monto_comision = self.porcentaje_colocacion.aplicar_a(precio_base.monto)
        return Dinero(monto_comision, precio_base.moneda)
    
    def esta_publicada(self) -> bool:
        """Verifica si la propiedad esta publicada"""
        return self.fecha_publicacion is not None
    
    def esta_cerrada(self) -> bool:
        """Verifica si la operacion fue cerrada"""
        return self.estado in [EstadoPropiedadEnum.VENDIDA, EstadoPropiedadEnum.ALQUILADA]
    
    def dias_en_mercado(self) -> int:
        """Calcula los dias que la propiedad lleva en el mercado"""
        if not self.fecha_publicacion:
            return 0
        
        fecha_final = self.fecha_cierre if self.fecha_cierre else date.today()
        return (fecha_final - self.fecha_publicacion).days
    
    def __str__(self) -> str:
        return f"{self.titulo} ({self.codigo_publico}) - {self.estado.value}"
