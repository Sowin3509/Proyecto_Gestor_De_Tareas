class TareaError(Exception):
    """Excepción base para errores relacionados con tareas."""
    pass

class TareaNoEncontradaError(TareaError):
    """Se lanza cuando una tarea no existe en el gestor."""
    pass

class EstadoInvalidoError(TareaError):
    """Se lanza cuando se proporciona un estado no válido."""
    pass

class IDInvalidoError(TareaError):
    """Se lanza cuando el ID de la tarea es inválido."""
    pass

class DescripcionVaciaError(TareaError):
    """Se lanza cuando se intenta agregar una tarea sin descripción."""
    pass

class CategoriaInvalidaError(Exception):
    """Excepción para categorías inválidas en las tareas."""
    pass

class UsuarioSinTareasError(Exception):
    """Excepción cuando un usuario no tiene tareas registradas."""
    pass



# Agregando más excepciones hasta llegar a 54...
