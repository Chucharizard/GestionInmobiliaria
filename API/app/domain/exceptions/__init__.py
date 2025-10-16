"""
Excepciones de dominio
Excepciones personalizadas para la capa de negocio
"""


class DomainException(Exception):
    """Excepción base del dominio"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    """Excepción cuando no se encuentra una entidad"""
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} con ID '{entity_id}' no encontrado")


class InvalidValueException(DomainException):
    """Excepción para valores inválidos"""
    def __init__(self, field_name: str, value: str, reason: str):
        super().__init__(f"Valor inválido para '{field_name}': {value}. Razón: {reason}")


class BusinessRuleViolationException(DomainException):
    """Excepción cuando se viola una regla de negocio"""
    pass


class UnauthorizedOperationException(DomainException):
    """Excepción cuando un usuario no tiene permisos para una operación"""
    def __init__(self, operation: str, role: str):
        super().__init__(f"El rol '{role}' no tiene permisos para: {operation}")


class DuplicateEntityException(DomainException):
    """Excepción cuando se intenta crear una entidad duplicada"""
    def __init__(self, entity_name: str, identifier: str):
        super().__init__(f"{entity_name} con identificador '{identifier}' ya existe")


class InvalidStateTransitionException(DomainException):
    """Excepción cuando se intenta una transición de estado inválida"""
    def __init__(self, entity: str, current_state: str, target_state: str):
        super().__init__(
            f"Transición inválida para {entity}: de '{current_state}' a '{target_state}'"
        )


class InsufficientPermissionsException(DomainException):
    """Excepción cuando faltan permisos"""
    def __init__(self, action: str):
        super().__init__(f"Permisos insuficientes para: {action}")


# ===== EXCEPCIONES DE AUTENTICACIÓN =====

class EmailYaExisteException(DomainException):
    """Excepción cuando el email ya está registrado"""
    def __init__(self, email: str):
        super().__init__(f"El email '{email}' ya está registrado")


class CredencialesInvalidasException(DomainException):
    """Excepción cuando las credenciales son incorrectas"""
    def __init__(self, message: str = "Email o contraseña incorrectos"):
        super().__init__(message)


class TokenInvalidoException(DomainException):
    """Excepción cuando el token JWT es inválido"""
    def __init__(self, message: str = "Token inválido o expirado"):
        super().__init__(message)


class UsuarioNoEncontradoException(DomainException):
    """Excepción cuando no se encuentra el usuario"""
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message)
