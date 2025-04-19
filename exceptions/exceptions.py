class TareaNoEncontradaError(Exception):
    def __init__(self, tarea_id, mensaje="La tarea no fue encontrada."):
        self.tarea_id = tarea_id
        self.codigo_error = 404
        super().__init__(f"{mensaje} (ID: {tarea_id})")

class EstadoInvalidoError(Exception):
    def __init__(self, estado, mensaje="El estado proporcionado no es válido."):
        self.estado = estado
        self.codigo_error = 400
        super().__init__(f"{mensaje} Estado: {estado}")

class IDInvalidoError(Exception):
    def __init__(self, id_recibido, mensaje="El ID proporcionado no es válido."):
        self.id_recibido = id_recibido
        self.codigo_error = 400
        super().__init__(f"{mensaje} ID recibido: {id_recibido}")

class DescripcionVaciaError(Exception):
    def __init__(self, mensaje="La descripción de la tarea no puede estar vacía."):
        self.codigo_error = 422
        super().__init__(mensaje)

class CategoriaInvalidaError(Exception):
    def __init__(self, categoria, mensaje="La categoría proporcionada no es válida."):
        self.categoria = categoria
        self.codigo_error = 400
        super().__init__(f"{mensaje} Categoría: {categoria}")

class UsuarioSinTareasError(Exception):
    def __init__(self, usuario, mensaje="El usuario no tiene tareas asignadas."):
        self.usuario = usuario
        self.codigo_error = 404
        super().__init__(f"{mensaje} Usuario: {usuario}")



"""
Módulo de excepciones personalizadas para el sistema de gestión de tareas.

Cada excepción define atributos como el código de error, el mensaje personalizado
y los datos específicos relacionados con la causa del error.
"""

class TareaNoEncontradaError(Exception):
    """
    Excepción lanzada cuando una tarea con un ID específico no existe.

    Atributos:
        tarea_id (int): ID de la tarea no encontrada.
        codigo_error (int): Código HTTP simulado (404).
    """

    def __init__(self, tarea_id, mensaje="La tarea no fue encontrada."):
        self.tarea_id = tarea_id
        self.codigo_error = 404
        super().__init__(f"{mensaje} (ID: {tarea_id})")


class EstadoInvalidoError(Exception):
    """
    Excepción lanzada cuando se proporciona un estado inválido para una tarea.

    Atributos:
        estado (str): Estado inválido recibido.
        codigo_error (int): Código HTTP simulado (400).
    """

    def __init__(self, estado, mensaje="El estado proporcionado no es válido."):
        self.estado = estado
        self.codigo_error = 400
        super().__init__(f"{mensaje} Estado: {estado}")


class IDInvalidoError(Exception):
    """
    Excepción lanzada cuando se proporciona un ID inválido.

    Atributos:
        id_recibido (int): Valor del ID recibido como inválido.
        codigo_error (int): Código HTTP simulado (400).
    """

    def __init__(self, id_recibido, mensaje="El ID proporcionado no es válido."):
        self.id_recibido = id_recibido
        self.codigo_error = 400
        super().__init__(f"{mensaje} ID recibido: {id_recibido}")


class DescripcionVaciaError(Exception):
    """
    Excepción lanzada cuando la descripción de una tarea está vacía.

    Atributos:
        codigo_error (int): Código HTTP simulado (422).
    """

    def __init__(self, mensaje="La descripción de la tarea no puede estar vacía."):
        self.codigo_error = 422
        super().__init__(mensaje)


class CategoriaInvalidaError(Exception):
    """
    Excepción lanzada cuando la categoría asignada a una tarea no es válida.

    Atributos:
        categoria (str): Categoría recibida como inválida.
        codigo_error (int): Código HTTP simulado (400).
    """

    def __init__(self, categoria, mensaje="La categoría proporcionada no es válida."):
        self.categoria = categoria
        self.codigo_error = 400
        super().__init__(f"{mensaje} Categoría: {categoria}")


class UsuarioSinTareasError(Exception):
    """
    Excepción lanzada cuando un usuario no tiene tareas asignadas.

    Atributos:
        usuario (str): Nombre del usuario sin tareas.
        codigo_error (int): Código HTTP simulado (404).
    """

    def __init__(self, usuario, mensaje="El usuario no tiene tareas asignadas."):
        self.usuario = usuario
        self.codigo_error = 404
        super().__init__(f"{mensaje} Usuario: {usuario}")
