"""
Entidad Cliente - Representa un cliente potencial o real
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.domain.value_objects import CI, Email, Telefono, NombreCompleto, Dinero
from app.domain.enums import OrigenClienteEnum


@dataclass
class Cliente:
    """
    Cliente de la inmobiliaria
    Puede ser comprador, inquilino o prospecto
    """
    ci_cliente: CI
    nombre_completo: NombreCompleto
    telefono: Telefono
    correo_electronico: Optional[Email]
    preferencia_zona: Optional[str]
    presupuesto_max: Optional[Dinero]
    origen: OrigenClienteEnum
    fecha_registro: datetime
    id_usuario_registrador: UUID
    es_activo: bool = True
    
    @staticmethod
    def crear_nuevo(
        ci_cliente: CI,
        nombre_completo: NombreCompleto,
        telefono: Telefono,
        id_usuario_registrador: UUID,
        correo_electronico: Optional[Email] = None,
        preferencia_zona: Optional[str] = None,
        presupuesto_max: Optional[Dinero] = None,
        origen: OrigenClienteEnum = OrigenClienteEnum.WEB
    ) -> 'Cliente':
        """Factory method para crear un nuevo cliente"""
        return Cliente(
            ci_cliente=ci_cliente,
            nombre_completo=nombre_completo,
            telefono=telefono,
            correo_electronico=correo_electronico,
            preferencia_zona=preferencia_zona,
            presupuesto_max=presupuesto_max,
            origen=origen,
            fecha_registro=datetime.utcnow(),
            id_usuario_registrador=id_usuario_registrador,
            es_activo=True
        )
    
    def actualizar_presupuesto(self, nuevo_presupuesto: Dinero) -> None:
        """Actualiza el presupuesto maximo del cliente"""
        self.presupuesto_max = nuevo_presupuesto
    
    def actualizar_preferencia_zona(self, nueva_zona: str) -> None:
        """Actualiza la zona de preferencia"""
        self.preferencia_zona = nueva_zona
    
    def puede_pagar(self, monto: Dinero) -> bool:
        """Verifica si el cliente puede pagar un monto dado"""
        if not self.presupuesto_max:
            return True  # Sin limite definido
        return self.presupuesto_max.monto >= monto.monto
    
    def desactivar(self) -> None:
        """Desactiva el cliente"""
        self.es_activo = False
    
    def activar(self) -> None:
        """Activa el cliente"""
        self.es_activo = True
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} (CI: {self.ci_cliente})"
