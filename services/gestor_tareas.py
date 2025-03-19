
from exceptions.custom_exceptions import (
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
