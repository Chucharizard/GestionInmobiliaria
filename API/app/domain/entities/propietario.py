"""
Entidad Propietario - Representa al dueno de una propiedad
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from app.domain.value_objects import CI, Email, Telefono, NombreCompleto


@dataclass
class Propietario:
    """
    Propietario de una o mas propiedades
    """
    ci_propietario: CI
    nombre_completo: NombreCompleto
    fecha_nacimiento: date
    telefono: Telefono
    correo_electronico: Optional[Email]
    es_activo: bool = True
    
    def calcular_edad(self) -> int:
        """Calcula la edad del propietario"""
        from datetime import datetime
        hoy = datetime.now().date()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def es_mayor_de_edad(self) -> bool:
        """Verifica si el propietario es mayor de edad"""
        return self.calcular_edad() >= 18
    
    def activar(self) -> None:
        """Activa el propietario"""
        self.es_activo = True
    
    def desactivar(self) -> None:
        """Desactiva el propietario"""
        self.es_activo = False
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} (CI: {self.ci_propietario})"
