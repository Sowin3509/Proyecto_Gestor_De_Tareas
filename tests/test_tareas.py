import pytest
from services.gestor_tareas import GestorTareas
from models.tarea import Tarea

@pytest.fixture
def gestor():
    return GestorTareas()

# 1-10: Pruebas para agregar tareas
def test_agregar_tarea(gestor):
    tarea = Tarea(None, "usuario1", "Comprar pan", "Personal")
    gestor.agregar_tarea(tarea)
    tareas = gestor.obtener_tareas("usuario1")
    assert any(t[2] == "Comprar pan" for t in tareas)

# Más pruebas para agregar tareas con diferentes datos
@pytest.mark.parametrize("descripcion, categoria", [
    ("Hacer ejercicio", "Salud"),
    ("Leer un libro", "Educación"),
    ("Pagar facturas", "Finanzas"),
    ("Cita con el doctor", "Salud"),
    ("Revisión del coche", "Mantenimiento"),
    ("Organizar archivos", "Trabajo"),
    ("Llamar a mamá", "Personal"),
    ("Comprar regalos", "Compras"),
    ("Planear vacaciones", "Ocio"),
])
def test_agregar_varias_tareas(gestor, descripcion, categoria):
    tarea = Tarea(None, "usuario2", descripcion, categoria)
    gestor.agregar_tarea(tarea)
    tareas = gestor.obtener_tareas("usuario2")
    assert any(t[2] == descripcion for t in tareas)

# 11-20: Pruebas para obtener tareas
def test_obtener_tareas_usuario_vacio(gestor):
    tareas = gestor.obtener_tareas("usuario_inexistente")
    assert len(tareas) == 0

def test_obtener_tareas_usuario_existente(gestor):
    tarea = Tarea(None, "usuario3", "Hacer café", "Cocina")
    gestor.agregar_tarea(tarea)
    tareas = gestor.obtener_tareas("usuario3")
    assert len(tareas) > 0

# 21-30: Pruebas para actualizar tareas
def test_actualizar_tarea(gestor):
    gestor.agregar_tarea(Tarea(None, "usuario4", "Estudiar Python", "Educación"))
    tareas = gestor.obtener_tareas("usuario4")
    tarea_id = tareas[0][0]
    gestor.actualizar_tarea(tarea_id, "Completada")
    tareas_actualizadas = gestor.obtener_tareas("usuario4")
    assert any(t[4] == "Completada" for t in tareas_actualizadas)

# 31-40: Pruebas para eliminar tareas
def test_eliminar_tarea(gestor):
    gestor.agregar_tarea(Tarea(None, "usuario5", "Sacar la basura", "Casa"))
    tareas = gestor.obtener_tareas("usuario5")
    tarea_id = tareas[0][0]
    gestor.eliminar_tarea(tarea_id)
    tareas_actualizadas = gestor.obtener_tareas("usuario5")
    assert not any(t[0] == tarea_id for t in tareas_actualizadas)

# 41-54: Casos extremos y de error
def test_agregar_tarea_sin_descripcion(gestor):
    tarea = Tarea(None, "usuario6", "", "Personal")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)

@pytest.mark.parametrize("estado", ["Finalizada", "Pendiente", "Cancelada", "No válida"])
def test_actualizar_tarea_estados(gestor, estado):
    gestor.agregar_tarea(Tarea(None, "usuario7", "Revisión de cuentas", "Finanzas"))
    tareas = gestor.obtener_tareas("usuario7")
    tarea_id = tareas[0][0]
    gestor.actualizar_tarea(tarea_id, estado)
    tareas_actualizadas = gestor.obtener_tareas("usuario7")
    assert any(t[4] == estado for t in tareas_actualizadas)
