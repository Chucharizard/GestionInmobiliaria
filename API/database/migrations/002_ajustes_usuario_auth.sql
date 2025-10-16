-- ============================================
-- AJUSTES A LA TABLA USUARIO PARA AUTENTICACIÓN
-- ============================================
-- Ejecutar este script en Supabase SQL Editor
-- ============================================

-- 1. Agregar columna de email (si no existe)
ALTER TABLE Usuario 
ADD COLUMN IF NOT EXISTS correo_electronico_usuario VARCHAR(120) UNIQUE;

-- 2. Agregar columna de último acceso (si no existe)
ALTER TABLE Usuario 
ADD COLUMN IF NOT EXISTS ultimo_acceso_usuario TIMESTAMP;

-- 3. Crear índice para búsqueda por email
CREATE INDEX IF NOT EXISTS idx_usuario_email 
ON Usuario(correo_electronico_usuario);

-- 4. Comentarios para documentación
COMMENT ON COLUMN Usuario.correo_electronico_usuario IS 'Email único del usuario para login';
COMMENT ON COLUMN Usuario.ultimo_acceso_usuario IS 'Fecha y hora del último login exitoso';

-- ============================================
-- VERIFICACIÓN (Opcional - para ver la estructura)
-- ============================================

-- Ver estructura actualizada de la tabla
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'usuario'
ORDER BY ordinal_position;

-- ============================================
-- NOTAS IMPORTANTES
-- ============================================
/*
1. El campo `correo_electronico_usuario` se usará para login
2. El campo `contrasenia_usuario` ya existe y almacenará el hash bcrypt
3. El campo `id_rol` se mapeará a los roles: 1=BROKER, 2=SECRETARIA, 3=ASESOR
4. Necesitarás insertar los roles en la tabla Rol primero
*/
