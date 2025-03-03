import pytest
from models.tarea import Tarea
from services.gestor_tareas import GestorTareas

@pytest.fixture
def gestor():
    """Crea una instancia de GestorTareas para las pruebas."""
    return GestorTareas()

def test_agregar_tarea(gestor):
    """Prueba la creación de una tarea."""
    tarea = Tarea(None, "usuario1", "Hacer la compra", "Personal")
    gestor.agregar_tarea(tarea)
    tareas = gestor.obtener_tareas("usuario1")
    assert len(tareas) > 0

def test_actualizar_tarea(gestor):
    """Prueba la actualización del estado de una tarea."""
    tarea = Tarea(None, "usuario1", "Hacer ejercicio", "Salud")
    gestor.agregar_tarea(tarea)
    id_tarea = gestor.obtener_tareas("usuario1")[-1][0]  # Obtener la última tarea agregada
    gestor.actualizar_tarea(id_tarea, "Completada")
    tareas = gestor.obtener_tareas("usuario1")
    estados = [t[4] for t in tareas]
    assert "Completada" in estados

def test_eliminar_tarea(gestor):
    """Prueba la eliminación de una tarea."""
    tarea = Tarea(None, "usuario1", "Leer un libro", "Ocio")
    gestor.agregar_tarea(tarea)
    id_tarea = gestor.obtener_tareas("usuario1")[-1][0]  # Obtener la última tarea agregada
    gestor.eliminar_tarea(id_tarea)
    tareas = gestor.obtener_tareas("usuario1")
    ids_tareas = [t[0] for t in tareas]
    assert id_tarea not in ids_tareas
