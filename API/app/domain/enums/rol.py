"""
Enum: Rol de Usuario
Define los diferentes roles que puede tener un usuario en el sistema
"""

from enum import Enum


class Rol(str, Enum):
    """
    Roles disponibles en el sistema de gestión inmobiliaria
    
    - BROKER: Acceso total al sistema, puede gestionar empleados y configuración
    - SECRETARIA: Acceso a operaciones administrativas y de gestión
    - ASESOR: Acceso limitado a propiedades y clientes asignados
    """
    
    BROKER = "BROKER"
    SECRETARIA = "SECRETARIA"
    ASESOR = "ASESOR"
    
    @property
    def descripcion(self) -> str:
        """Retorna una descripción del rol"""
        descripciones = {
            Rol.BROKER: "Administrador total del sistema",
            Rol.SECRETARIA: "Gestión administrativa y operativa",
            Rol.ASESOR: "Asesor comercial de propiedades"
        }
        return descripciones[self]
    
    @property
    def permisos_nivel(self) -> int:
        """
        Retorna el nivel de permisos (mayor número = más permisos)
        Útil para comparaciones
        """
        niveles = {
            Rol.BROKER: 3,
            Rol.SECRETARIA: 2,
            Rol.ASESOR: 1
        }
        return niveles[self]
    
    def puede_gestionar(self, otro_rol: "Rol") -> bool:
        """
        Verifica si este rol puede gestionar a otro rol
        
        Args:
            otro_rol: El rol a comparar
            
        Returns:
            True si puede gestionar, False si no
        """
        return self.permisos_nivel > otro_rol.permisos_nivel
    
    @classmethod
    def from_string(cls, valor: str) -> "Rol":
        """
        Crea un Rol desde un string
        
        Args:
            valor: String con el nombre del rol
            
        Returns:
            Instancia de Rol
            
        Raises:
            ValueError: Si el string no corresponde a ningún rol
        """
        try:
            return cls(valor.upper())
        except ValueError:
            roles_validos = [r.value for r in cls]
            raise ValueError(
                f"Rol inválido: '{valor}'. Roles válidos: {', '.join(roles_validos)}"
            )
