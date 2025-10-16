"""
Entidad Direccion - Representa la ubicacion geografica de una propiedad
"""

from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Optional
from app.domain.value_objects import Coordenadas


@dataclass
class Direccion:
    """
    Direccion y ubicacion geografica de una propiedad
    """
    id_direccion: UUID
    calle: str
    ciudad: str
    zona: str
    coordenadas: Optional[Coordenadas]
    
    @staticmethod
    def crear_nueva(
        calle: str,
        ciudad: str,
        zona: str,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None
    ) -> 'Direccion':
        """Factory method para crear una nueva direccion"""
        coordenadas = None
        if latitud is not None and longitud is not None:
            coordenadas = Coordenadas(latitud, longitud)
        
        return Direccion(
            id_direccion=uuid4(),
            calle=calle,
            ciudad=ciudad,
            zona=zona,
            coordenadas=coordenadas
        )
    
    def direccion_completa(self) -> str:
        """Retorna la direccion completa como texto"""
        return f"{self.calle}, {self.zona}, {self.ciudad}"
    
    def tiene_coordenadas(self) -> bool:
        """Verifica si la direccion tiene coordenadas GPS"""
        return self.coordenadas is not None
    
    def actualizar_coordenadas(self, latitud: float, longitud: float) -> None:
        """Actualiza las coordenadas GPS"""
        self.coordenadas = Coordenadas(latitud, longitud)
    
    def __str__(self) -> str:
        return self.direccion_completa()
