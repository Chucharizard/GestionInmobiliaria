"""
Entidad Usuario - Representa las credenciales y permisos de un empleado
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from app.domain.enums import RolEnum
from app.domain.value_objects import CI
from app.domain.exceptions import UnauthorizedOperationException


@dataclass
class Usuario:
    """
    Usuario del sistema - asociado a un empleado
    Maneja autenticacion y autorizacion
    """
    id_usuario: UUID
    ci_empleado: CI
    id_rol: int
    rol: RolEnum
    nombre_usuario: str
    contrasenia_hash: bytes
    fecha_creacion: datetime
    es_activo: bool = True
    
    @staticmethod
    def crear_nuevo(
        ci_empleado: CI,
        id_rol: int,
        rol: RolEnum,
        nombre_usuario: str,
        contrasenia_hash: bytes
    ) -> 'Usuario':
        """Factory method para crear un nuevo usuario"""
        return Usuario(
            id_usuario=uuid4(),
            ci_empleado=ci_empleado,
            id_rol=id_rol,
            rol=rol,
            nombre_usuario=nombre_usuario,
            contrasenia_hash=contrasenia_hash,
            fecha_creacion=datetime.utcnow(),
            es_activo=True
        )
    
    def es_broker(self) -> bool:
        """Verifica si el usuario es un Broker"""
        return self.rol == RolEnum.BROKER
    
    def es_secretaria(self) -> bool:
        """Verifica si el usuario es Secretaria"""
        return self.rol == RolEnum.SECRETARIA
    
    def es_asesor(self) -> bool:
        """Verifica si el usuario es Asesor"""
        return self.rol == RolEnum.ASESOR
    
    def puede_gestionar_empleados(self) -> bool:
        """Solo el Broker puede gestionar empleados"""
        return self.es_broker()
    
    def puede_gestionar_propiedades(self) -> bool:
        """Broker y Secretaria pueden gestionar propiedades"""
        return self.es_broker() or self.es_secretaria()
    
    def puede_gestionar_clientes(self) -> bool:
        """Broker y Secretaria pueden gestionar clientes"""
        return self.es_broker() or self.es_secretaria()
    
    def puede_ver_reportes(self) -> bool:
        """Broker y Secretaria pueden ver todos los reportes"""
        return self.es_broker() or self.es_secretaria()
    
    def validar_permiso(self, operacion: str) -> None:
        """Valida si tiene permiso para una operacion"""
        permisos = {
            "gestionar_empleados": self.puede_gestionar_empleados(),
            "gestionar_propiedades": self.puede_gestionar_propiedades(),
            "gestionar_clientes": self.puede_gestionar_clientes(),
            "ver_reportes": self.puede_ver_reportes()
        }
        
        if operacion in permisos and not permisos[operacion]:
            raise UnauthorizedOperationException(operacion, self.rol.value)
    
    def activar(self) -> None:
        """Activa el usuario"""
        self.es_activo = True
    
    def desactivar(self) -> None:
        """Desactiva el usuario"""
        self.es_activo = False
    
    def __str__(self) -> str:
        return f"{self.nombre_usuario} ({self.rol.value})"
