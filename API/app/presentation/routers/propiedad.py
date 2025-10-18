from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from app.presentation.schemas.propiedad_schemas import (
    PropiedadCreateRequest,
    PropiedadUpdateRequest,
    PropiedadFilterRequest,
    PropiedadResponse,
    PropiedadListResponse,
    PropiedadCreateResponse
)
from app.application.use_cases.propiedad_use_cases import (
    CrearPropiedadUseCase,
    ObtenerPropiedadUseCase,
    ListarPropiedadesUseCase,
    ActualizarPropiedadUseCase,
    EliminarPropiedadUseCase,
    BuscarPropiedadPorCodigoUseCase
)
from app.infrastructure.repositories.propiedad_repository import PropiedadRepository
from app.presentation.routers.auth import get_current_user
from app.domain.exceptions.propiedad_exceptions import (
    PropiedadNoEncontradaException,
    CodigoPublicoDuplicadoException
)

router = APIRouter(prefix="/api/v1/propiedades", tags=["Propiedades"])

# Dependencias

def get_propiedad_repository():
    return PropiedadRepository()


# ========== Endpoints ==========

@router.post(
    "",
    response_model=PropiedadCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva propiedad",
    description="Crea una nueva propiedad inmobiliaria. Requiere autenticación."
)
async def crear_propiedad(
    request: PropiedadCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Crea una nueva propiedad inmobiliaria
    
    - **id_direccion**: UUID de la dirección asociada
    - **ci_propietario**: Cédula del propietario
    - **codigo_publico_propiedad**: Código único público
    - **titulo_propiedad**: Título descriptivo
    - **precio_publicado_propiedad**: Precio de venta/alquiler
    - **superficie_propiedad**: Superficie en m²
    - **tipo_operacion_propiedad**: venta, alquiler, venta/alquiler
    """
    try:
        use_case = CrearPropiedadUseCase(repository)
        
        propiedad_data = request.model_dump()
        id_usuario_captador = current_user["id_usuario"]
        
        propiedad = await use_case.execute(propiedad_data, id_usuario_captador)
        
        return PropiedadCreateResponse(
            message="Propiedad creada exitosamente",
            propiedad=PropiedadResponse(**propiedad)
        )
        
    except CodigoPublicoDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear propiedad: {str(e)}"
        )


@router.get(
    "",
    response_model=PropiedadListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar propiedades",
    description="Lista propiedades con filtros y paginación"
)
async def listar_propiedades(
    tipo_operacion: str | None = None,
    estado: str | None = None,
    precio_min: float | None = None,
    precio_max: float | None = None,
    superficie_min: float | None = None,
    superficie_max: float | None = None,
    ci_propietario: str | None = None,
    id_usuario_captador: str | None = None,
    page: int = 1,
    page_size: int = 10,
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Lista propiedades con filtros opcionales y paginación
    
    **Filtros disponibles:**
    - **tipo_operacion**: venta, alquiler, venta/alquiler
    - **estado**: disponible, reservada, vendida, alquilada, inactiva
    - **precio_min/max**: Rango de precios
    - **superficie_min/max**: Rango de superficie en m²
    - **ci_propietario**: Cédula del propietario
    - **id_usuario_captador**: UUID del usuario captador
    - **page**: Número de página (default: 1)
    - **page_size**: Elementos por página (default: 10, max: 100)
    """
    try:
        use_case = ListarPropiedadesUseCase(repository)
        
        filters = {
            "tipo_operacion": tipo_operacion,
            "estado": estado,
            "precio_min": precio_min,
            "precio_max": precio_max,
            "superficie_min": superficie_min,
            "superficie_max": superficie_max,
            "ci_propietario": ci_propietario,
            "id_usuario_captador": id_usuario_captador
        }
        
        # Remover filtros vacíos
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Validar paginación
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
        
        result = await use_case.execute(filters, page, page_size)
        
        return PropiedadListResponse(
            items=[PropiedadResponse(**p) for p in result["items"]],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar propiedades: {str(e)}"
        )


@router.get(
    "/{id_propiedad}",
    response_model=PropiedadResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener propiedad por ID",
    description="Obtiene los detalles de una propiedad específica"
)
async def obtener_propiedad(
    id_propiedad: str,
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Obtiene una propiedad por su ID
    
    - **id_propiedad**: UUID de la propiedad
    """
    try:
        use_case = ObtenerPropiedadUseCase(repository)
        propiedad = await use_case.execute(id_propiedad)
        
        return PropiedadResponse(**propiedad)
        
    except PropiedadNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener propiedad: {str(e)}"
        )


@router.get(
    "/codigo/{codigo_publico}",
    response_model=PropiedadResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar propiedad por código público",
    description="Busca una propiedad por su código público único"
)
async def buscar_por_codigo(
    codigo_publico: str,
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Busca una propiedad por su código público
    
    - **codigo_publico**: Código público único de la propiedad (ej: PROP-001)
    """
    try:
        use_case = BuscarPropiedadPorCodigoUseCase(repository)
        propiedad = await use_case.execute(codigo_publico)
        
        return PropiedadResponse(**propiedad)
        
    except PropiedadNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar propiedad: {str(e)}"
        )


@router.put(
    "/{id_propiedad}",
    response_model=PropiedadResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar propiedad",
    description="Actualiza los datos de una propiedad. Requiere autenticación."
)
async def actualizar_propiedad(
    id_propiedad: str,
    request: PropiedadUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Actualiza una propiedad existente
    
    - **id_propiedad**: UUID de la propiedad
    - Todos los campos son opcionales, solo se actualizan los enviados
    """
    try:
        use_case = ActualizarPropiedadUseCase(repository)
        
        # Filtrar campos no enviados
        update_data = request.model_dump(exclude_unset=True)
        
        propiedad = await use_case.execute(id_propiedad, update_data)
        
        return PropiedadResponse(**propiedad)
        
    except PropiedadNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar propiedad: {str(e)}"
        )


@router.delete(
    "/{id_propiedad}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar propiedad",
    description="Elimina una propiedad (soft delete). Requiere autenticación."
)
async def eliminar_propiedad(
    id_propiedad: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    repository: PropiedadRepository = Depends(get_propiedad_repository)
):
    """
    Elimina una propiedad (cambia estado a 'inactiva')
    
    - **id_propiedad**: UUID de la propiedad
    """
    try:
        use_case = EliminarPropiedadUseCase(repository)
        await use_case.execute(id_propiedad)
        
        return None
        
    except PropiedadNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar propiedad: {str(e)}"
        )
