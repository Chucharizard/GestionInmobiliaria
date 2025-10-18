from typing import Dict, Any, List
from uuid import UUID, uuid4
from datetime import datetime
from app.infrastructure.repositories.propiedad_repository import PropiedadRepository
from app.domain.exceptions.propiedad_exceptions import PropiedadNoEncontradaException, CodigoPublicoDuplicadoException


class CrearPropiedadUseCase:
    """Caso de uso para crear una nueva propiedad"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(self, propiedad_data: Dict[str, Any], id_usuario_captador: str) -> Dict[str, Any]:
        """
        Crea una nueva propiedad
        
        Args:
            propiedad_data: Datos de la propiedad
            id_usuario_captador: ID del usuario que capta la propiedad
            
        Returns:
            Propiedad creada
            
        Raises:
            CodigoPublicoDuplicadoException: Si el código público ya existe
        """
        # Generar ID
        propiedad_data["id_propiedad"] = str(uuid4())
        propiedad_data["id_usuario_captador"] = id_usuario_captador
        propiedad_data["estado_propiedad"] = "disponible"
        propiedad_data["fecha_captacion_propiedad"] = datetime.utcnow().date().isoformat()
        
        return await self.repository.create(propiedad_data)


class ObtenerPropiedadUseCase:
    """Caso de uso para obtener una propiedad por ID"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(self, id_propiedad: str) -> Dict[str, Any]:
        """
        Obtiene una propiedad por su ID
        
        Args:
            id_propiedad: UUID de la propiedad
            
        Returns:
            Propiedad encontrada
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        propiedad = await self.repository.find_by_id(id_propiedad)
        
        if not propiedad:
            raise PropiedadNoEncontradaException(f"Propiedad con ID {id_propiedad} no encontrada")
        
        return propiedad


class ListarPropiedadesUseCase:
    """Caso de uso para listar propiedades con filtros y paginación"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(
        self,
        filters: Dict[str, Any],
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Lista propiedades con filtros y paginación
        
        Args:
            filters: Diccionario con filtros
            page: Número de página
            page_size: Elementos por página
            
        Returns:
            Diccionario con items, total, page, page_size, total_pages
        """
        propiedades, total = await self.repository.find_all(filters, page, page_size)
        
        total_pages = (total + page_size - 1) // page_size  # Redondeo hacia arriba
        
        return {
            "items": propiedades,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class ActualizarPropiedadUseCase:
    """Caso de uso para actualizar una propiedad"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(self, id_propiedad: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una propiedad
        
        Args:
            id_propiedad: UUID de la propiedad
            update_data: Datos a actualizar
            
        Returns:
            Propiedad actualizada
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        return await self.repository.update(id_propiedad, update_data)


class EliminarPropiedadUseCase:
    """Caso de uso para eliminar (soft delete) una propiedad"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(self, id_propiedad: str) -> bool:
        """
        Elimina una propiedad (soft delete cambiando estado a 'inactiva')
        
        Args:
            id_propiedad: UUID de la propiedad
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        return await self.repository.delete(id_propiedad)


class BuscarPropiedadPorCodigoUseCase:
    """Caso de uso para buscar propiedad por código público"""
    
    def __init__(self, repository: PropiedadRepository):
        self.repository = repository
    
    async def execute(self, codigo_publico: str) -> Dict[str, Any]:
        """
        Busca una propiedad por su código público
        
        Args:
            codigo_publico: Código público de la propiedad
            
        Returns:
            Propiedad encontrada
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        propiedad = await self.repository.find_by_codigo_publico(codigo_publico)
        
        if not propiedad:
            raise PropiedadNoEncontradaException(f"Propiedad con código '{codigo_publico}' no encontrada")
        
        return propiedad
