"""
Repositorio de Usuarios
Maneja la persistencia de usuarios en Supabase
"""

from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from app.domain.enums.rol import Rol
from app.infrastructure.database.supabase_client import SupabaseClient


class UserRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def __init__(self):
        self.supabase = SupabaseClient.get_admin_client()
        self.table = "usuario"  # Nombre correcto de la tabla en tu BD
    
    async def create(
        self, 
        email: str, 
        password_hash: str, 
        rol: Rol,
        empleado_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea un nuevo usuario en la base de datos
        
        Args:
            email: Email del usuario
            password_hash: Hash de la contraseña
            rol: Rol del usuario
            empleado_id: ID del empleado asociado (opcional)
            
        Returns:
            Diccionario con datos del usuario creado
            
        Raises:
            Exception: Si hay error al crear el usuario
        """
        try:
            # Mapear a los nombres de columnas de tu BD
            data = {
                "correo_electronico_usuario": email,
                "contrasenia_usuario": password_hash,  # Enviar como string, Supabase lo convertirá a BYTEA
                "id_rol": self._map_rol_to_id(rol),
                "nombre_usuario": email.split('@')[0],  # Usar parte del email como username
                "es_activo_usuario": True,
                "fecha_creacion_usuario": datetime.utcnow().isoformat(),
                "ultimo_acceso_usuario": None
            }
            
            # Solo agregar ci_empleado si se proporciona
            if empleado_id:
                data["ci_empleado"] = empleado_id
            
            # Insertar el usuario
            response = self.supabase.table(self.table).insert(data).execute()
            
            if not response.data:
                raise Exception("Error al crear usuario")
            
            # Obtener solo el ID del usuario recién creado
            user_id = response.data[0].get("id_usuario")
            
            # Construir respuesta manualmente sin consultar de nuevo la BD
            # Esto evita problemas con bytes de la contraseña
            created_user = {
                "id": str(user_id),
                "email": email,
                "rol": rol.value,
                "empleado_id": empleado_id,
                "activo": True,
                "fecha_creacion": data["fecha_creacion_usuario"],
                "ultimo_acceso": None
            }
            
            return created_user
            
        except Exception as e:
            raise Exception(f"Error al crear usuario: {str(e)}")
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un usuario por su email (sin incluir contraseña)
        
        Args:
            email: Email a buscar
            
        Returns:
            Diccionario con datos del usuario si existe, None si no
        """
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("correo_electronico_usuario", email)\
                .execute()
            
            if not response.data:
                return None
            
            return self._map_from_db(response.data[0])
            
        except Exception as e:
            print(f"Error al buscar usuario por email: {str(e)}")
            return None
    
    async def find_by_email_with_password(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un usuario por su email INCLUYENDO la contraseña (solo para autenticación)
        
        Args:
            email: Email a buscar
            
        Returns:
            Diccionario con datos del usuario Y password_hash si existe, None si no
        """
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("correo_electronico_usuario", email)\
                .execute()
            
            if not response.data:
                return None
            
            user_data = response.data[0]
            
            # Convertir password desde el formato que viene de Supabase
            password = user_data.get("contrasenia_usuario")
            
            if password:
                # Si viene como string con formato \x (hex escape), decodificar desde hex
                if isinstance(password, str) and password.startswith('\\x'):
                    try:
                        # Remover el prefijo \x y decodificar desde hex
                        hex_string = password.replace('\\x', '')
                        password_bytes = bytes.fromhex(hex_string)
                        password = password_bytes.decode('utf-8')
                    except Exception as e:
                        print(f"Error decodificando password desde hex: {e}")
                        password = None
                elif isinstance(password, bytes):
                    password = password.decode('utf-8')
                elif isinstance(password, memoryview):
                    password = bytes(password).decode('utf-8')
            
            # Usar _map_from_db y agregar el password_hash manualmente
            mapped_data = self._map_from_db(user_data)
            mapped_data["password_hash"] = password
            
            return mapped_data
            
        except Exception as e:
            print(f"Error al buscar usuario por email con contraseña: {str(e)}")
            return None
    
    async def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un usuario por su ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con datos del usuario si existe, None si no
        """
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("id_usuario", user_id)\
                .execute()
            
            if not response.data:
                return None
            
            # Convertir contrasenia_usuario a string antes de mapear
            user_data = response.data[0]
            if "contrasenia_usuario" in user_data and isinstance(user_data["contrasenia_usuario"], bytes):
                user_data["contrasenia_usuario"] = user_data["contrasenia_usuario"].decode('utf-8')
            
            return self._map_from_db(user_data)
            
        except Exception as e:
            print(f"Error al buscar usuario por ID: {str(e)}")
            return None
    
    async def update_last_login(self, user_id: str) -> bool:
        """
        Actualiza la fecha del último acceso del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si se actualizó correctamente
        """
        try:
            response = self.supabase.table(self.table)\
                .update({"ultimo_acceso_usuario": datetime.utcnow().isoformat()})\
                .eq("id_usuario", user_id)\
                .execute()
            
            return bool(response.data)
            
        except Exception as e:
            print(f"Error al actualizar último acceso: {str(e)}")
            return False
    
    async def exists_by_email(self, email: str) -> bool:
        """
        Verifica si ya existe un usuario con ese email
        
        Args:
            email: Email a verificar
            
        Returns:
            True si existe, False si no
        """
        user = await self.find_by_email(email)
        return user is not None
    
    async def update_password(self, user_id: str, password_hash: str) -> bool:
        """
        Actualiza la contraseña de un usuario
        
        Args:
            user_id: ID del usuario
            password_hash: Nuevo hash de contraseña
            
        Returns:
            True si se actualizó correctamente
        """
        try:
            response = self.supabase.table(self.table)\
                .update({"contrasenia_usuario": password_hash.encode('utf-8')})\
                .eq("id_usuario", user_id)\
                .execute()
            
            return bool(response.data)
            
        except Exception as e:
            print(f"Error al actualizar contraseña: {str(e)}")
            return False
    
    def _map_rol_to_id(self, rol: Rol) -> int:
        """
        Mapea un rol del dominio (enum) a su ID en la base de datos
        
        Args:
            rol: Enum del rol
            
        Returns:
            ID del rol en la base de datos
        """
        mapping = {
            "BROKER": 1,
            "SECRETARIA": 2,
            "ASESOR": 3
        }
        return mapping[rol.value]
    
    def _map_id_to_rol(self, id_rol: int) -> str:
        """
        Mapea un ID de rol de la base de datos al nombre del rol del dominio
        
        Args:
            id_rol: ID del rol en la base de datos
            
        Returns:
            Nombre del rol como string
        """
        mapping = {
            1: "BROKER",
            2: "SECRETARIA",
            3: "ASESOR"
        }
        return mapping.get(id_rol, "ASESOR")
    
    def _map_from_db(self, data: dict) -> dict:
        """
        Mapea los nombres de columnas de la base de datos a los nombres del dominio
        
        Args:
            data: Diccionario con datos de la base de datos
            
        Returns:
            Diccionario con nombres de campos del dominio (SIN password_hash)
        """
        # Convertir fechas a string ISO format si son datetime
        fecha_creacion = data.get("fecha_creacion_usuario")
        if fecha_creacion and not isinstance(fecha_creacion, str):
            fecha_creacion = fecha_creacion.isoformat() if hasattr(fecha_creacion, 'isoformat') else str(fecha_creacion)
        
        ultimo_acceso = data.get("ultimo_acceso_usuario")
        if ultimo_acceso and not isinstance(ultimo_acceso, str):
            ultimo_acceso = ultimo_acceso.isoformat() if hasattr(ultimo_acceso, 'isoformat') else str(ultimo_acceso)
        
        # NO incluir password_hash en la respuesta para evitar problemas de serialización
        return {
            "id": str(data["id_usuario"]),
            "email": data.get("correo_electronico_usuario"),
            "rol": self._map_id_to_rol(data["id_rol"]),
            "empleado_id": data.get("ci_empleado"),
            "activo": data.get("es_activo_usuario", True),
            "fecha_creacion": fecha_creacion,
            "ultimo_acceso": ultimo_acceso
        }
    


# Instancia singleton del repositorio
user_repository = UserRepository()
