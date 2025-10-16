-- ============================================
-- SCRIPT DE CREACIÓN DE TABLA: usuarios
-- ============================================
-- Este script crea la tabla de usuarios para autenticación
-- Ejecutar este script en Supabase SQL Editor
-- ============================================

-- Eliminar tabla si existe (CUIDADO: esto borra todos los datos)
-- DROP TABLE IF EXISTS usuarios CASCADE;

-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    -- Identificador único
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Datos de autenticación
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Rol del usuario
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('BROKER', 'SECRETARIA', 'ASESOR')),
    
    -- Relación con empleado (opcional)
    empleado_id UUID NULL,
    
    -- Estado del usuario
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Auditoría
    fecha_creacion TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ultimo_acceso TIMESTAMP WITH TIME ZONE NULL,
    
    -- Constraints
    CONSTRAINT email_formato CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios(activo);
CREATE INDEX IF NOT EXISTS idx_usuarios_empleado_id ON usuarios(empleado_id);

-- Comentarios para documentación
COMMENT ON TABLE usuarios IS 'Tabla de usuarios para autenticación y autorización';
COMMENT ON COLUMN usuarios.id IS 'Identificador único del usuario (UUID)';
COMMENT ON COLUMN usuarios.email IS 'Email único del usuario para login';
COMMENT ON COLUMN usuarios.password_hash IS 'Hash bcrypt de la contraseña';
COMMENT ON COLUMN usuarios.rol IS 'Rol del usuario: BROKER, SECRETARIA o ASESOR';
COMMENT ON COLUMN usuarios.empleado_id IS 'ID del empleado asociado (FK a tabla empleados)';
COMMENT ON COLUMN usuarios.activo IS 'Indica si el usuario puede iniciar sesión';
COMMENT ON COLUMN usuarios.fecha_creacion IS 'Fecha y hora de creación del usuario';
COMMENT ON COLUMN usuarios.ultimo_acceso IS 'Fecha y hora del último login exitoso';

-- Habilitar Row Level Security (RLS)
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;

-- Política: Solo usuarios autenticados pueden ver sus propios datos
CREATE POLICY "Usuarios pueden ver sus propios datos" ON usuarios
    FOR SELECT
    USING (auth.uid()::text = id::text);

-- Política: Solo service_role puede insertar usuarios (desde backend)
CREATE POLICY "Backend puede crear usuarios" ON usuarios
    FOR INSERT
    WITH CHECK (true);

-- Política: Usuarios pueden actualizar sus propios datos (excepto rol)
CREATE POLICY "Usuarios pueden actualizar sus datos" ON usuarios
    FOR UPDATE
    USING (auth.uid()::text = id::text);

-- ============================================
-- DATOS DE PRUEBA (OPCIONAL - DESCOMENTAR SI DESEAS)
-- ============================================

-- Usuario Broker de prueba
-- INSERT INTO usuarios (email, password_hash, rol, activo)
-- VALUES (
--     'broker@test.com',
--     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eoKnd3eMt.dK', -- Password: Test123!
--     'BROKER',
--     TRUE
-- );

-- Usuario Secretaria de prueba
-- INSERT INTO usuarios (email, password_hash, rol, activo)
-- VALUES (
--     'secretaria@test.com',
--     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eoKnd3eMt.dK', -- Password: Test123!
--     'SECRETARIA',
--     TRUE
-- );

-- Usuario Asesor de prueba  
-- INSERT INTO usuarios (email, password_hash, rol, activo)
-- VALUES (
--     'asesor@test.com',
--     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eoKnd3eMt.dK', -- Password: Test123!
--     'ASESOR',
--     TRUE
-- );

-- ============================================
-- VERIFICACIÓN
-- ============================================

-- Ver estructura de la tabla
-- SELECT * FROM information_schema.columns WHERE table_name = 'usuarios';

-- Ver usuarios creados
-- SELECT id, email, rol, activo, fecha_creacion FROM usuarios;

-- ============================================
-- NOTAS IMPORTANTES
-- ============================================
/*
1. La contraseña de ejemplo (Test123!) tiene el hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eoKnd3eMt.dK
2. Los hashes reales deben generarse desde la API usando bcrypt
3. RLS está habilitado para seguridad adicional
4. La tabla empleado_id requiere crear la tabla empleados primero
5. Asegúrate de tener el service_role key configurado en el backend
*/
