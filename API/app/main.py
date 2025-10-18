"""
Sistema de Gestion Inmobiliaria - API REST
Punto de entrada de la aplicacion FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.infrastructure.config.settings import settings
from app.presentation.routers import auth, propiedad

# Crear la aplicacion FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API REST para gestion integral de inmobiliaria con autenticacion por roles",
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Endpoint raiz para verificar que la API esta funcionando"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "environment": settings.environment
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para health check"""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler global para excepciones no controladas"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred"
        }
    )


# Eventos de startup y shutdown
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicacion"""
    print(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    print(f"📊 Entorno: {settings.environment}")
    print(f"🔧 Debug: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al detener la aplicacion"""
    print(f"👋 Deteniendo {settings.app_name}")


# Incluir routers
app.include_router(auth.router)
app.include_router(propiedad.router)
# Próximamente:
# app.include_router(empleados.router, prefix="/api/v1", tags=["Empleados"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
