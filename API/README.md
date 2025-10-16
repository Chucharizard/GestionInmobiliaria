# 🏢 Sistema de Gestión Inmobiliaria - API

API REST desarrollada con **FastAPI** siguiendo **Clean Architecture** para la gestión integral de una inmobiliaria.

## 📋 Stack Tecnológico

- **Backend**: FastAPI 0.115.0+ con Python 3.11
- **Base de Datos**: Supabase (PostgreSQL managed)
- **Arquitectura**: Clean Architecture (Domain, Application, Infrastructure, Presentation)
- **Autenticación**: JWT (JSON Web Tokens)
- **Documentación**: OpenAPI (Swagger) automática

## 🏗️ Arquitectura del Proyecto

```
API/
├── app/
│   ├── domain/              # 🟢 Capa de Dominio (lógica de negocio pura)
│   │   ├── entities/        # Entidades del negocio
│   │   ├── value_objects/   # Objetos de valor inmutables
│   │   ├── enums/           # Enumeraciones
│   │   └── exceptions/      # Excepciones de dominio
│   │
│   ├── application/         # 🔵 Capa de Aplicación (casos de uso)
│   │   ├── use_cases/       # Lógica de casos de uso
│   │   ├── dtos/            # Data Transfer Objects
│   │   └── interfaces/      # Contratos/Interfaces
│   │
│   ├── infrastructure/      # 🟡 Capa de Infraestructura
│   │   ├── database/        # Conexión y modelos de BD
│   │   ├── repositories/    # Implementaciones concretas
│   │   ├── services/        # Servicios externos (Supabase)
│   │   └── config/          # Configuración y settings
│   │
│   ├── presentation/        # 🔴 Capa de Presentación (API REST)
│   │   ├── api/v1/          # Endpoints versión 1
│   │   ├── schemas/         # Schemas Pydantic (request/response)
│   │   └── middleware/      # Middlewares (auth, CORS, etc.)
│   │
│   └── shared/              # 🟣 Código compartido
│       └── utils/           # Utilidades generales
│
├── tests/                   # Tests unitarios e integración
├── .env.example             # Variables de entorno de ejemplo
├── requirements.txt         # Dependencias Python
└── main.py                  # Punto de entrada de la aplicación
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd GestionInmobiliaria/API
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales de Supabase
```

### 5. Ejecutar la aplicación

```bash
# Modo desarrollo (con auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

La API estará disponible en: `http://localhost:8000`

##  Documentación API

Una vez iniciada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 👥 Roles de Usuario

El sistema maneja 3 roles con diferentes niveles de acceso:

1. **Bróker** (Admin)
   - Gestión completa de empleados
   - Acceso total al sistema
   - Asignación de roles

2. **Secretaria**
   - Gestión de clientes, propietarios y propiedades
   - Administración de visitas y operaciones
   - Generación de reportes

3. **Asesor Inmobiliario**
   - Consulta de propiedades asignadas
   - Gestión de visitas propias
   - Registro de resultados de visitas
   - Consulta de rendimiento personal

## 🔑 Módulos Principales

### Autenticación
- Login/Logout
- Refresh Token
- Gestión de sesiones

### Empleados
- CRUD de empleados (solo Bróker)
- Asignación de roles
- Consulta de información personal

### Propiedades
- CRUD de propiedades
- Gestión de imágenes (portada, orden)
- Documentos PDF (exclusividad, contratos)
- Configuración de comisiones

### Clientes
- CRUD de clientes
- Preferencias y presupuesto
- Historial de interacciones

### Visitas
- Agenda de visitas
- Asignación rotativa de asesores
- Reprogramación y cancelación
- Registro de resultados

### Operaciones
- Registro de cierres (venta/alquiler)
- Cálculo automático de comisiones
- Gestión de pagos

### Reportes
- Visitas por propiedad
- Rendimiento por asesor
- Ganancias por empleado
- Filtros por fecha y tipo

##  Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/unit/
pytest tests/integration/
```

##  Dependencias Principales

- **fastapi**: Framework web moderno y rápido
- **uvicorn**: Servidor ASGI
- **pydantic**: Validación de datos
- **supabase**: Cliente para Supabase (PostgreSQL)
- **python-jose**: JWT para autenticación
- **passlib**: Hashing de contraseñas
- **python-multipart**: Manejo de archivos

##  Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Autenticación JWT
- ✅ Autorización basada en roles (RBAC)
- ✅ Validación de datos con Pydantic
- ✅ CORS configurado
- ✅ Rate limiting (recomendado para producción)

##  Equipo de Desarrollo

- **Product Owner**: Ignacio Adrian Layme Delgado
- **Scrum Master**: Nicolas Arturo Vargas Silva
- **Developers**: Jesus Wilfredo Arancibia Alfaro, Ignacio Adrian Layme Delgado, Nicolas Arturo Vargas Silva

##  Licencia

Este proyecto es de uso académico para el curso de Ingeniería de Software.

---

