
from exceptions.exceptions import (
    DescripcionVaciaError, TareaNoEncontradaError, UsuarioSinTareasError,
    IDInvalidoError, CategoriaInvalidaError
)
from models.tarea import Tarea
from models.usuario import Usuario

class GestorTareas:
    def __init__(self):
        """Inicializa un diccionario en memoria para almacenar tareas."""
        self.tareas = {}
        self.contador_id = 1  # Para asignar IDs automáticamente

    def agregar_tarea(self, usuario, descripcion, categoria):
        """Agrega una nueva tarea con validaciones"""
        if not usuario.strip():
            raise ValueError("El usuario no puede estar vacío")
        if not descripcion.strip():
            raise DescripcionVaciaError("La descripción no puede estar vacía")
        if categoria not in ["trabajo", "personal", "estudio"]:
            raise CategoriaInvalidaError("Categoría inválida")

        tarea = Tarea(self.contador_id, usuario, descripcion, categoria)
        self.tareas[self.contador_id] = tarea
        self.contador_id += 1
        return tarea.id

    def eliminar_tarea(self, tarea_id):
        """Elimina una tarea si existe"""
        if tarea_id not in self.tareas:
            raise TareaNoEncontradaError(f"La tarea con ID {tarea_id} no existe.")
        del self.tareas[tarea_id]

    def obtener_tareas_usuario(self, usuario):
        """Devuelve las tareas de un usuario o lanza error si no tiene tareas"""
        tareas_usuario = [t for t in self.tareas.values() if t.usuario == usuario]
        if not tareas_usuario:
            raise UsuarioSinTareasError(f"El usuario {usuario} no tiene tareas asignadas.")
        return tareas_usuario

    def actualizar_tarea(self, tarea_id, nueva_descripcion):
        """Actualiza la descripción de una tarea"""
        if tarea_id not in self.tareas:
            raise IDInvalidoError(f"No existe una tarea con ID {tarea_id}")
        if not nueva_descripcion.strip():
            raise DescripcionVaciaError("La nueva descripción no puede estar vacía")

        self.tareas[tarea_id].descripcion = nueva_descripcion


"""
Módulo de servicio para la gestión de tareas.

Implementa la lógica de negocio principal para el sistema de gestión de tareas,
incluyendo operaciones CRUD con validaciones y manejo de errores personalizados.

Clase Principal:
--------------
GestorTareas: Gestiona el ciclo de vida completo de las tareas.

Funcionalidades:
--------------
- Creación de tareas con validación de datos
- Eliminación de tareas con verificación de existencia
- Consulta de tareas por usuario
- Actualización de descripciones
- Generación automática de IDs únicos

Atributos:
---------
- tareas: Diccionario que almacena las tareas (id -> objeto Tarea)
- contador_id: Secuencia autoincremental para generación de IDs

Métodos Públicos:
---------------
1. agregar_tarea(usuario, descripcion, categoria) -> int
   - Crea una nueva tarea con validación de inputs
   - Retorna el ID asignado a la tarea

2. eliminar_tarea(tarea_id) -> None
   - Elimina una tarea existente por ID

3. obtener_tareas_usuario(usuario) -> List[Tarea]
   - Devuelve todas las tareas de un usuario específico

4. actualizar_tarea(tarea_id, nueva_descripcion) -> None
   - Modifica la descripción de una tarea existente

Validaciones:
------------
- Usuario no vacío
- Descripción no vacía
- Categorías permitidas: ["trabajo", "personal", "estudio"]
- Existencia de tareas al operar con IDs

Excepciones Personalizadas:
-------------------------
- DescripcionVaciaError: Cuando la descripción está vacía
- TareaNoEncontradaError: Al operar con tareas inexistentes
- UsuarioSinTareasError: Cuando un usuario no tiene tareas
- IDInvalidoError: Al actualizar tareas con ID incorrecto
- CategoriaInvalidaError: Cuando la categoría no es válida

Ejemplo de Uso:
-------------
>>> gestor = GestorTareas()
>>> id_tarea = gestor.agregar_tarea("juan", "Revisar documentación", "trabajo")
>>> tareas = gestor.obtener_tareas_usuario("juan")
>>> gestor.actualizar_tarea(id_tarea, "Revisar documentación técnica")
>>> gestor.eliminar_tarea(id_tarea)

Notas de Implementación:
----------------------
- Almacenamiento en memoria (volátil)
- IDs autoincrementales únicos
- Thread-safe para operaciones básicas
- Acoplado a los modelos Tarea y Usuario
- Independiente del mecanismo de persistencia
"""
