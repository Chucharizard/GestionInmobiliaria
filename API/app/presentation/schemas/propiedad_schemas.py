from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date

# ========== Request Schemas ==========

class PropiedadCreateRequest(BaseModel):
    """Schema para crear una nueva propiedad"""
    id_direccion: UUID = Field(..., description="ID de la dirección de la propiedad")
    ci_propietario: str = Field(..., min_length=6, max_length=10, description="Cédula del propietario")
    codigo_publico_propiedad: str = Field(..., min_length=1, max_length=50, description="Código público único")
    titulo_propiedad: str = Field(..., min_length=5, max_length=200, description="Título de la propiedad")
    descripcion_propiedad: Optional[str] = Field(None, max_length=2000, description="Descripción detallada")
    precio_publicado_propiedad: float = Field(..., gt=0, description="Precio de venta/alquiler")
    superficie_propiedad: float = Field(..., gt=0, description="Superficie en m²")
    tipo_operacion_propiedad: str = Field(..., description="Tipo: venta, alquiler, venta/alquiler")
    porcentaje_captacion_propiedad: Optional[float] = Field(None, ge=0, le=100, description="% comisión captación")
    porcentaje_colocacion_propiedad: Optional[float] = Field(None, ge=0, le=100, description="% comisión colocación")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id_direccion": "123e4567-e89b-12d3-a456-426614174000",
            "ci_propietario": "12345678",
            "codigo_publico_propiedad": "PROP-001",
            "titulo_propiedad": "Casa amplia con jardín en zona céntrica",
            "descripcion_propiedad": "Hermosa casa de 3 dormitorios...",
            "precio_publicado_propiedad": 150000.00,
            "superficie_propiedad": 120.5,
            "tipo_operacion_propiedad": "venta",
            "porcentaje_captacion_propiedad": 3.0,
            "porcentaje_colocacion_propiedad": 3.0
        }
    })


class PropiedadUpdateRequest(BaseModel):
    """Schema para actualizar una propiedad existente"""
    titulo_propiedad: Optional[str] = Field(None, min_length=5, max_length=200)
    descripcion_propiedad: Optional[str] = Field(None, max_length=2000)
    precio_publicado_propiedad: Optional[float] = Field(None, gt=0)
    superficie_propiedad: Optional[float] = Field(None, gt=0)
    tipo_operacion_propiedad: Optional[str] = None
    estado_propiedad: Optional[str] = None
    id_usuario_colocador: Optional[UUID] = None
    fecha_publicacion_propiedad: Optional[str] = None  # ISO format
    fecha_cierre_propiedad: Optional[str] = None  # ISO format
    porcentaje_captacion_propiedad: Optional[float] = Field(None, ge=0, le=100)
    porcentaje_colocacion_propiedad: Optional[float] = Field(None, ge=0, le=100)

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "titulo_propiedad": "Casa amplia con jardín - ACTUALIZADO",
            "precio_publicado_propiedad": 145000.00,
            "estado_propiedad": "disponible"
        }
    })


class PropiedadFilterRequest(BaseModel):
    """Schema para filtrar propiedades"""
    tipo_operacion: Optional[str] = Field(None, description="venta, alquiler, venta/alquiler")
    estado: Optional[str] = Field(None, description="disponible, reservada, vendida, alquilada, inactiva")
    precio_min: Optional[float] = Field(None, ge=0)
    precio_max: Optional[float] = Field(None, ge=0)
    superficie_min: Optional[float] = Field(None, ge=0)
    superficie_max: Optional[float] = Field(None, ge=0)
    ci_propietario: Optional[str] = None
    id_usuario_captador: Optional[UUID] = None
    page: int = Field(1, ge=1, description="Número de página")
    page_size: int = Field(10, ge=1, le=100, description="Elementos por página")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "tipo_operacion": "venta",
            "estado": "disponible",
            "precio_min": 100000,
            "precio_max": 200000,
            "page": 1,
            "page_size": 10
        }
    })


# ========== Response Schemas ==========

class PropiedadResponse(BaseModel):
    """Schema para la respuesta de una propiedad"""
    id_propiedad: str
    id_direccion: str
    ci_propietario: str
    codigo_publico_propiedad: str
    titulo_propiedad: str
    descripcion_propiedad: Optional[str]
    precio_publicado_propiedad: float
    superficie_propiedad: float
    tipo_operacion_propiedad: str
    estado_propiedad: str
    id_usuario_captador: Optional[str]
    id_usuario_colocador: Optional[str]
    fecha_captacion_propiedad: Optional[str]
    fecha_publicacion_propiedad: Optional[str]
    fecha_cierre_propiedad: Optional[str]
    porcentaje_captacion_propiedad: Optional[float]
    porcentaje_colocacion_propiedad: Optional[float]

    model_config = ConfigDict(from_attributes=True)


class PropiedadListResponse(BaseModel):
    """Schema para la lista paginada de propiedades"""
    items: list[PropiedadResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [],
            "total": 50,
            "page": 1,
            "page_size": 10,
            "total_pages": 5
        }
    })


class PropiedadCreateResponse(BaseModel):
    """Schema para la respuesta al crear una propiedad"""
    message: str
    propiedad: PropiedadResponse

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "message": "Propiedad creada exitosamente",
            "propiedad": {}
        }
    })
