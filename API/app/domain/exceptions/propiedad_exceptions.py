class PropiedadNoEncontradaException(Exception):
    """Excepción cuando no se encuentra una propiedad"""
    pass

class PropiedadYaExisteException(Exception):
    """Excepción cuando una propiedad ya existe"""
    pass

class CodigoPublicoDuplicadoException(Exception):
    """Excepción cuando el código público ya está en uso"""
    pass
