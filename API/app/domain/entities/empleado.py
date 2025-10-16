"""
Entidad Empleado - Representa un empleado de la inmobiliaria
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from app.domain.value_objects import CI, Email, Telefono, NombreCompleto


@dataclass
class Empleado:
    """
    Empleado de la inmobiliaria
    Puede ser Broker, Secretaria o Asesor
    """
    ci_empleado: CI
    nombre_completo: NombreCompleto
    correo_electronico: Email
    fecha_nacimiento: date
    telefono: Telefono
    es_activo: bool = True
    
    def activar(self) -> None:
        """Activa el empleado"""
        self.es_activo = True
    
    def desactivar(self) -> None:
        """Desactiva el empleado"""
        self.es_activo = False
    
    def calcular_edad(self) -> int:
        """Calcula la edad del empleado"""
        from datetime import datetime
        hoy = datetime.now().date()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def es_mayor_de_edad(self) -> bool:
        """Verifica si el empleado es mayor de edad"""
        return self.calcular_edad() >= 18
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} (CI: {self.ci_empleado})"
