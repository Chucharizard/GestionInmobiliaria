"""
Router de Autenticación
Endpoints para registro, login, refresh y obtener usuario actual
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.presentation.schemas.auth_schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse
)
from app.application.use_cases.auth_use_cases import (
    register_user_use_case,
    login_use_case,
    refresh_token_use_case,
    get_current_user_use_case
)
from app.domain.exceptions import (
    EmailYaExisteException,
    CredencialesInvalidasException,
    TokenInvalidoException,
    UsuarioNoEncontradoException
)


# Configuración del router
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)

# Esquema de seguridad Bearer
security = HTTPBearer()


# ===== DEPENDENCY: Obtener usuario actual =====

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency para obtener el usuario actual desde el token
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        Datos del usuario actual
        
    Raises:
        HTTPException: Si el token es inválido
    """
    try:
        token = credentials.credentials
        user = await get_current_user_use_case.execute(token)
        return user
    except (TokenInvalidoException, UsuarioNoEncontradoException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


# ===== ENDPOINTS =====

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="""
    Registra un nuevo usuario en el sistema.
    
    **Requisitos:**
    - Email único válido
    - Contraseña mínimo 8 caracteres (debe incluir mayúscula, minúscula y número)
    - Rol válido: BROKER, SECRETARIA o ASESOR
    
    **Respuesta:**
    - Usuario creado con ID generado
    - No retorna tokens (debe hacer login después)
    """
)
async def register(request: RegisterRequest):
    """Registra un nuevo usuario"""
    try:
        user_data = await register_user_use_case.execute(
            email=request.email,
            password=request.password,
            rol=request.rol,
            empleado_id=request.empleado_id
        )
        
        return RegisterResponse(
            user=UserResponse(**user_data),
            message="Usuario registrado exitosamente"
        )
        
    except EmailYaExisteException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="""
    Autentica a un usuario y retorna tokens de acceso.
    
    **Proceso:**
    1. Valida credenciales (email + password)
    2. Verifica que el usuario esté activo
    3. Genera par de tokens (access + refresh)
    4. Actualiza fecha de último acceso
    
    **Respuesta:**
    - Datos del usuario
    - Access token (expira en 30 minutos)
    - Refresh token (expira en 7 días)
    """
)
async def login(request: LoginRequest):
    """Inicia sesión y retorna tokens"""
    try:
        result = await login_use_case.execute(
            email=request.email,
            password=request.password
        )
        
        return LoginResponse(
            user=UserResponse(**result["user"]),
            tokens=TokenResponse(**result["tokens"]),
            message="Login exitoso"
        )
        
    except CredencialesInvalidasException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar sesión: {str(e)}"
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refrescar token de acceso",
    description="""
    Genera un nuevo access token usando un refresh token válido.
    
    **Uso:**
    - Cuando el access token expira (401 Unauthorized)
    - Enviar el refresh token en el body
    - Recibirás un nuevo par de tokens
    
    **Nota:** El refresh token también se renueva en cada refresh
    """
)
async def refresh_token(request: RefreshTokenRequest):
    """Refresca el access token"""
    try:
        tokens = await refresh_token_use_case.execute(request.refresh_token)
        return TokenResponse(**tokens)
        
    except (TokenInvalidoException, UsuarioNoEncontradoException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al refrescar token: {str(e)}"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="""
    Retorna los datos del usuario autenticado.
    
    **Autenticación requerida:**
    - Header: `Authorization: Bearer {access_token}`
    
    **Uso:**
    - Verificar información del usuario logueado
    - Validar permisos según rol
    - Obtener ID para otras operaciones
    """
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Obtiene los datos del usuario actual"""
    return UserResponse(**current_user)


@router.get(
    "/check",
    summary="Verificar token",
    description="Endpoint simple para verificar si un token es válido"
)
async def check_token(current_user: dict = Depends(get_current_user)):
    """Verifica si el token es válido"""
    return {
        "valid": True,
        "user_id": current_user["id"],
        "email": current_user["email"],
        "rol": current_user["rol"]
    }
