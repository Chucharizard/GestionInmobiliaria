"""
Value Objects - Objetos de valor inmutables
Representan conceptos del dominio con validacion integrada
"""

import re
from dataclasses import dataclass
from typing import Optional
from app.domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class CI:
    """Carnet de Identidad - Value Object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise InvalidValueException("CI", self.value, "No puede estar vacio")
        
        # Eliminar espacios y guiones
        clean_ci = re.sub(r'[\s-]', '', self.value)
        
        if not clean_ci.isdigit():
            raise InvalidValueException("CI", self.value, "Debe contener solo numeros")
        
        if len(clean_ci) < 6 or len(clean_ci) > 20:
            raise InvalidValueException("CI", self.value, "Debe tener entre 6 y 20 caracteres")
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Email:
    """Email - Value Object con validacion"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise InvalidValueException("Email", self.value, "No puede estar vacio")
        
        # Patron basico de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise InvalidValueException("Email", self.value, "Formato invalido")
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Telefono:
    """Telefono - Value Object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise InvalidValueException("Telefono", self.value, "No puede estar vacio")
        
        # Eliminar espacios, guiones y parentesis
        clean_phone = re.sub(r'[\s\-()]', '', self.value)
        
        if not clean_phone.isdigit():
            raise InvalidValueException("Telefono", self.value, "Debe contener solo numeros")
        
        if len(clean_phone) < 7 or len(clean_phone) > 15:
            raise InvalidValueException("Telefono", self.value, "Debe tener entre 7 y 15 digitos")
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class NombreCompleto:
    """Nombre completo - Value Object"""
    nombres: str
    apellidos: str
    
    def __post_init__(self):
        if not self.nombres or not self.nombres.strip():
            raise InvalidValueException("Nombres", self.nombres, "No pueden estar vacios")
        
        if not self.apellidos or not self.apellidos.strip():
            raise InvalidValueException("Apellidos", self.apellidos, "No pueden estar vacios")
        
        if len(self.nombres) > 120:
            raise InvalidValueException("Nombres", self.nombres, "Maximo 120 caracteres")
        
        if len(self.apellidos) > 120:
            raise InvalidValueException("Apellidos", self.apellidos, "Maximo 120 caracteres")
    
    def nombre_completo(self) -> str:
        """Retorna el nombre completo concatenado"""
        return f"{self.nombres} {self.apellidos}"
    
    def __str__(self) -> str:
        return self.nombre_completo()


@dataclass(frozen=True)
class Dinero:
    """Dinero - Value Object para manejo de montos monetarios"""
    monto: float
    moneda: str = "BOB"  # Bolivianos por defecto
    
    def __post_init__(self):
        if self.monto < 0:
            raise InvalidValueException("Dinero", str(self.monto), "No puede ser negativo")
        
        if self.moneda not in ["BOB", "USD", "EUR"]:
            raise InvalidValueException("Moneda", self.moneda, "Moneda no soportada")
    
    def __str__(self) -> str:
        return f"{self.moneda} {self.monto:,.2f}"
    
    def __add__(self, other: 'Dinero') -> 'Dinero':
        if self.moneda != other.moneda:
            raise InvalidValueException("Moneda", other.moneda, "No se pueden sumar diferentes monedas")
        return Dinero(self.monto + other.monto, self.moneda)
    
    def __sub__(self, other: 'Dinero') -> 'Dinero':
        if self.moneda != other.moneda:
            raise InvalidValueException("Moneda", other.moneda, "No se pueden restar diferentes monedas")
        resultado = self.monto - other.monto
        if resultado < 0:
            raise InvalidValueException("Dinero", str(resultado), "El resultado no puede ser negativo")
        return Dinero(resultado, self.moneda)


@dataclass(frozen=True)
class Porcentaje:
    """Porcentaje - Value Object"""
    valor: float
    
    def __post_init__(self):
        if self.valor < 0 or self.valor > 100:
            raise InvalidValueException("Porcentaje", str(self.valor), "Debe estar entre 0 y 100")
    
    def __str__(self) -> str:
        return f"{self.valor}%"
    
    def aplicar_a(self, monto: float) -> float:
        """Aplica el porcentaje a un monto"""
        return (monto * self.valor) / 100


@dataclass(frozen=True)
class Coordenadas:
    """Coordenadas geograficas - Value Object"""
    latitud: float
    longitud: float
    
    def __post_init__(self):
        if self.latitud < -90 or self.latitud > 90:
            raise InvalidValueException("Latitud", str(self.latitud), "Debe estar entre -90 y 90")
        
        if self.longitud < -180 or self.longitud > 180:
            raise InvalidValueException("Longitud", str(self.longitud), "Debe estar entre -180 y 180")
    
    def __str__(self) -> str:
        return f"({self.latitud}, {self.longitud})"
