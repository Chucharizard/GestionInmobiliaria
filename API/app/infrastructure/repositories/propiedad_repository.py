from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.infrastructure.database.supabase_client import get_supabase
from app.domain.exceptions.propiedad_exceptions import PropiedadNoEncontradaException, CodigoPublicoDuplicadoException


class PropiedadRepository:
    """Repository para gestionar propiedades en Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "propiedad"
    
    async def create(self, propiedad_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva propiedad
        
        Args:
            propiedad_data: Diccionario con los datos de la propiedad
            
        Returns:
            Diccionario con la propiedad creada
            
        Raises:
            CodigoPublicoDuplicadoException: Si el código público ya existe
        """
        try:
            # Verificar si el código público ya existe
            existing = self.supabase.table(self.table_name)\
                .select("id_propiedad")\
                .eq("codigo_publico_propiedad", propiedad_data["codigo_publico_propiedad"])\
                .execute()
            
            if existing.data:
                raise CodigoPublicoDuplicadoException(
                    f"El código público '{propiedad_data['codigo_publico_propiedad']}' ya está en uso"
                )
            
            # Establecer valores por defecto
            propiedad_data["estado_propiedad"] = propiedad_data.get("estado_propiedad", "disponible")
            propiedad_data["fecha_captacion_propiedad"] = propiedad_data.get(
                "fecha_captacion_propiedad", 
                datetime.utcnow().date().isoformat()
            )
            
            # Insertar propiedad
            response = self.supabase.table(self.table_name)\
                .insert(propiedad_data)\
                .execute()
            
            if not response.data:
                raise Exception("Error al crear la propiedad")
            
            return self._map_from_db(response.data[0])
            
        except CodigoPublicoDuplicadoException:
            raise
        except Exception as e:
            raise Exception(f"Error al crear propiedad: {str(e)}")
    
    async def find_by_id(self, id_propiedad: str) -> Optional[Dict[str, Any]]:
        """
        Busca una propiedad por ID
        
        Args:
            id_propiedad: UUID de la propiedad
            
        Returns:
            Diccionario con la propiedad o None si no existe
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select("*")\
                .eq("id_propiedad", id_propiedad)\
                .execute()
            
            if not response.data:
                return None
            
            return self._map_from_db(response.data[0])
            
        except Exception as e:
            raise Exception(f"Error al buscar propiedad: {str(e)}")
    
    async def find_all(
        self, 
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Lista propiedades con filtros y paginación
        
        Args:
            filters: Diccionario con filtros opcionales
            page: Número de página (desde 1)
            page_size: Elementos por página
            
        Returns:
            Tupla (lista de propiedades, total de elementos)
        """
        try:
            # Construir query con filtros
            query = self.supabase.table(self.table_name).select("*", count="exact")
            
            if filters:
                if "tipo_operacion" in filters and filters["tipo_operacion"]:
                    query = query.eq("tipo_operacion_propiedad", filters["tipo_operacion"])
                
                if "estado" in filters and filters["estado"]:
                    query = query.eq("estado_propiedad", filters["estado"])
                
                if "precio_min" in filters and filters["precio_min"] is not None:
                    query = query.gte("precio_publicado_propiedad", filters["precio_min"])
                
                if "precio_max" in filters and filters["precio_max"] is not None:
                    query = query.lte("precio_publicado_propiedad", filters["precio_max"])
                
                if "superficie_min" in filters and filters["superficie_min"] is not None:
                    query = query.gte("superficie_propiedad", filters["superficie_min"])
                
                if "superficie_max" in filters and filters["superficie_max"] is not None:
                    query = query.lte("superficie_propiedad", filters["superficie_max"])
                
                if "ci_propietario" in filters and filters["ci_propietario"]:
                    query = query.eq("ci_propietario", filters["ci_propietario"])
                
                if "id_usuario_captador" in filters and filters["id_usuario_captador"]:
                    query = query.eq("id_usuario_captador", str(filters["id_usuario_captador"]))
            
            # Aplicar paginación
            start = (page - 1) * page_size
            end = start + page_size - 1
            
            response = query.range(start, end).execute()
            
            propiedades = [self._map_from_db(p) for p in response.data]
            total = response.count if response.count else 0
            
            return propiedades, total
            
        except Exception as e:
            raise Exception(f"Error al listar propiedades: {str(e)}")
    
    async def update(self, id_propiedad: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una propiedad
        
        Args:
            id_propiedad: UUID de la propiedad
            update_data: Diccionario con los campos a actualizar
            
        Returns:
            Diccionario con la propiedad actualizada
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        try:
            # Verificar que existe
            existing = await self.find_by_id(id_propiedad)
            if not existing:
                raise PropiedadNoEncontradaException(f"Propiedad con ID {id_propiedad} no encontrada")
            
            # Filtrar campos vacíos
            filtered_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not filtered_data:
                return existing
            
            # Actualizar
            response = self.supabase.table(self.table_name)\
                .update(filtered_data)\
                .eq("id_propiedad", id_propiedad)\
                .execute()
            
            if not response.data:
                raise Exception("Error al actualizar la propiedad")
            
            return self._map_from_db(response.data[0])
            
        except PropiedadNoEncontradaException:
            raise
        except Exception as e:
            raise Exception(f"Error al actualizar propiedad: {str(e)}")
    
    async def delete(self, id_propiedad: str) -> bool:
        """
        Elimina (soft delete) una propiedad cambiando su estado a 'inactiva'
        
        Args:
            id_propiedad: UUID de la propiedad
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            PropiedadNoEncontradaException: Si la propiedad no existe
        """
        try:
            # Verificar que existe
            existing = await self.find_by_id(id_propiedad)
            if not existing:
                raise PropiedadNoEncontradaException(f"Propiedad con ID {id_propiedad} no encontrada")
            
            # Soft delete
            response = self.supabase.table(self.table_name)\
                .update({"estado_propiedad": "inactiva"})\
                .eq("id_propiedad", id_propiedad)\
                .execute()
            
            return bool(response.data)
            
        except PropiedadNoEncontradaException:
            raise
        except Exception as e:
            raise Exception(f"Error al eliminar propiedad: {str(e)}")
    
    async def find_by_codigo_publico(self, codigo_publico: str) -> Optional[Dict[str, Any]]:
        """
        Busca una propiedad por su código público
        
        Args:
            codigo_publico: Código público de la propiedad
            
        Returns:
            Diccionario con la propiedad o None si no existe
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select("*")\
                .eq("codigo_publico_propiedad", codigo_publico)\
                .execute()
            
            if not response.data:
                return None
            
            return self._map_from_db(response.data[0])
            
        except Exception as e:
            raise Exception(f"Error al buscar propiedad por código: {str(e)}")
    
    def _map_from_db(self, db_row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapea un registro de la BD a un diccionario con formato de respuesta
        
        Args:
            db_row: Fila de la base de datos
            
        Returns:
            Diccionario con los datos mapeados
        """
        # Convertir UUIDs a strings
        mapped = db_row.copy()
        
        for key in ["id_propiedad", "id_direccion", "id_usuario_captador", "id_usuario_colocador"]:
            if key in mapped and mapped[key] is not None:
                mapped[key] = str(mapped[key])
        
        # Convertir dates a strings ISO
        for key in ["fecha_captacion_propiedad", "fecha_publicacion_propiedad", "fecha_cierre_propiedad"]:
            if key in mapped and mapped[key] is not None:
                if isinstance(mapped[key], str):
                    mapped[key] = mapped[key]
                else:
                    mapped[key] = mapped[key].isoformat()
        
        return mapped
