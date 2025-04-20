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




"""
Módulo de excepciones personalizadas para el sistema de gestión de tareas.

Proporciona clases de excepciones específicas para manejar errores de dominio
en el sistema de gestión de tareas, con información contextual detallada.

Estructura común de las excepciones:
----------------------------------
- Atributos adicionales con contexto del error
- Códigos de error HTTP semánticos
- Mensajes descriptivos con información específica
- Herencia de la clase base Exception

Jerarquía de Excepciones:
-----------------------
1. TareaNoEncontradaError (404)
2. EstadoInvalidoError (400)
3. IDInvalidoError (400)
4. DescripcionVaciaError (422)
5. CategoriaInvalidaError (400)
6. UsuarioSinTareasError (404)

Propósito:
---------
- Proporcionar errores específicos del dominio
- Facilitar el manejo granular de errores
- Incluir metadatos útiles para el diagnóstico
- Mantener consistencia en los errores de la API

Uso típico:
----------
>>> try:
...     gestor.obtener_tarea(999)
... except TareaNoEncontradaError as e:
...     print(f"Error {e.codigo_error}: {e}")

Atributos comunes:
---------------
codigo_error : int
    Código HTTP semántico asociado al error
mensaje : str
    Descripción legible del error

Best Practices:
-------------
- Usar excepciones específicas en lugar de Exception genérica
- Capturar excepciones con el tipo más específico posible
- Proporcionar contexto relevante en el mensaje de error
- Usar códigos HTTP apropiados para cada caso

Ejemplo completo:
--------------
try:
    gestor.agregar_tarea("", "", "invalid")
except (DescripcionVaciaError, CategoriaInvalidaError) as e:
    logger.error(f"{e.__class__.__name__}: {e}")
    raise
"""

class TareaNoEncontradaError(Exception):
    """
    Excepción lanzada cuando no se encuentra una tarea con el ID especificado.

    Atributos:
        tarea_id (int): ID de la tarea no encontrada
        codigo_error (int): 404 (Not Found)
    
    Uso:
        raise TareaNoEncontradaError(123)
    """
    def __init__(self, tarea_id, mensaje="La tarea no fue encontrada"):
        self.tarea_id = tarea_id
        self.codigo_error = 404
        super().__init__(f"{mensaje} (ID: {tarea_id})")


class EstadoInvalidoError(Exception):
    """
    Excepción para estados de tarea no válidos.

    Atributos:
        estado (str): Estado inválido recibido
        codigo_error (int): 400 (Bad Request)
    """
    def __init__(self, estado, mensaje="Estado de tarea inválido"):
        self.estado = estado
        self.codigo_error = 400
        super().__init__(f"{mensaje}: {estado}")


class IDInvalidoError(Exception):
    """
    Excepción para IDs de tarea mal formados o inválidos.

    Atributos:
        id_recibido (any): Valor inválido recibido como ID
        codigo_error (int): 400 (Bad Request)
    """
    def __init__(self, id_recibido, mensaje="ID de tarea inválido"):
        self.id_recibido = id_recibido
        self.codigo_error = 400
        super().__init__(f"{mensaje}: {id_recibido}")


class DescripcionVaciaError(Exception):
    """
    Excepción para descripciones de tarea vacías o nulas.

    Atributos:
        codigo_error (int): 422 (Unprocessable Entity)
    """
    def __init__(self, mensaje="La descripción no puede estar vacía"):
        self.codigo_error = 422
        super().__init__(mensaje)


class CategoriaInvalidaError(Exception):
    """
    Excepción para categorías de tarea no permitidas.

    Atributos:
        categoria (str): Categoría inválida recibida
        codigo_error (int): 400 (Bad Request)
    """
    def __init__(self, categoria, mensaje="Categoría inválida"):
        self.categoria = categoria
        self.codigo_error = 400
        super().__init__(f"{mensaje}: {categoria}")


class UsuarioSinTareasError(Exception):
    """
    Excepción cuando un usuario no tiene tareas asignadas.

    Atributos:
        usuario (str): Nombre del usuario sin tareas
        codigo_error (int): 404 (Not Found)
    """
    def __init__(self, usuario, mensaje="Usuario sin tareas asignadas"):
        self.usuario = usuario
        self.codigo_error = 404
        super().__init__(f"{mensaje}: {usuario}")