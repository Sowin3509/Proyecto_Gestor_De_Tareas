import pytest
from services.gestor_tareas import GestorTareas
from models.tarea import Tarea
from services.gestor_tareas import GestorTareas, Tarea

# 54 pruebas con fallos intencionales

def test_agregar_tarea_1():
    gestor = GestorTareas()
    tarea = Tarea("", "usuario6", "", "Personal")
    gestor.agregar_tarea(tarea)
    assert False  # Provoca fallo intencional

def test_contar_tareas_2():
    gestor = GestorTareas()
    assert gestor.obtener_todas_las_tareas() == 57  # Falla intencionalmente

def test_eliminar_tarea_3():
    gestor = GestorTareas()
    assert gestor.eliminar_tarea(1) == True  # Falla intencionalmente

def test_actualizar_estado_4():
    gestor = GestorTareas()
    assert gestor.actualizar_estado(1, "Completado") == True  # Falla

def test_listar_tareas_usuario_5():
    gestor = GestorTareas()
    assert len(gestor.obtener_tareas_usuario("usuario6")) == 5  # Falla

def test_agregar_tarea_sin_descripcion_6(gestor):
    """Debe fallar porque la descripción está vacía"""
    with pytest.raises(ValueError):
        tarea = Tarea(None, "usuario1", "", "Trabajo")
        gestor.agregar_tarea(tarea)

def test_agregar_tarea_con_categoria_invalida_7(gestor):
    """Debe fallar porque la categoría no es válida"""
    with pytest.raises(ValueError):
        tarea = Tarea(None, "usuario1", "Hacer reporte", "Categoría_Falsa")
        gestor.agregar_tarea(tarea)

def test_actualizar_tarea_inexistente_8(gestor):
    """Debe fallar porque la tarea no existe"""
    with pytest.raises(KeyError):
        gestor.actualizar_tarea(999, "Completada")

def test_eliminar_tarea_inexistente_9(gestor):
    """Debe fallar porque la tarea no existe"""
    with pytest.raises(KeyError):
        gestor.eliminar_tarea(999)

def test_obtener_tareas_usuario_sin_tareas_10(gestor):
    """Debe fallar porque el usuario no tiene tareas"""
    tareas = gestor.obtener_tareas("usuario_vacio")
    assert len(tareas) > 0, "El usuario no debería tener tareas registradas"

def test_contar_tareas_en_lista_vacia_11(gestor):
    """Debe fallar porque no hay tareas en la base de datos"""
    tareas = gestor.obtener_tareas("usuario1")
    assert len(tareas) > 0, "No hay tareas registradas"

def test_agregar_tarea_con_usuario_vacio_12(gestor):
    """Debe fallar porque el usuario está vacío"""
    with pytest.raises(ValueError):
        tarea = Tarea(None, "", "Comprar comida", "Hogar")
        gestor.agregar_tarea(tarea)

def test_actualizar_tarea_con_estado_invalido_13(gestor):
    """Debe fallar porque el estado no es válido"""
    tarea = Tarea(None, "usuario2", "Llamar al banco", "Trabajo")
    gestor.agregar_tarea(tarea)
    with pytest.raises(ValueError):
        gestor.actualizar_tarea(1, "Estado_No_Existe")

def test_eliminar_tarea_de_otro_usuario_14(gestor):
    """Debe fallar porque el usuario no tiene permisos para eliminar la tarea"""
    tarea = Tarea(1, "usuario3", "Hacer ejercicio", "Salud")
    gestor.agregar_tarea(tarea)
    with pytest.raises(PermissionError):
        gestor.eliminar_tarea(1)  # Usuario incorrecto intentando eliminar

def test_obtener_tareas_con_usuario_inexistente_15(gestor):
    """Debe fallar porque el usuario no existe"""
    tareas = gestor.obtener_tareas("usuario_inexistente")
    assert len(tareas) > 0, "El usuario no debería tener tareas registradas"

def test_agregar_tarea_con_id_duplicado_16(gestor):
    """Debe fallar porque el ID de la tarea está duplicado"""
    tarea1 = Tarea(1, "usuario4", "Estudiar para el examen", "Estudios")
    tarea2 = Tarea(1, "usuario4", "Leer un libro", "Ocio")  # ID duplicado
    gestor.agregar_tarea(tarea1)
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea2)

@pytest.fixture

def test_actualizar_tarea_con_estado_no_permitido_17(gestor):
    tarea = Tarea(1, "usuario1", "Hacer ejercicio", "Salud")
    gestor.agregar_tarea(tarea)
    with pytest.raises(ValueError):
        gestor.actualizar_tarea(1, estado="Desconocido")

def test_eliminar_tarea_ya_eliminada_18(gestor):
    tarea = Tarea(2, "usuario1", "Leer un libro", "Educación")
    gestor.agregar_tarea(tarea)
    gestor.eliminar_tarea(2)
    with pytest.raises(KeyError):
        gestor.eliminar_tarea(2)  # Se intenta eliminar nuevamente

def test_listar_tareas_usuario_sin_permisos_19(gestor):
    tarea = Tarea(3, "usuario1", "Pagar facturas", "Finanzas")
    gestor.agregar_tarea(tarea)
    with pytest.raises(PermissionError):
        gestor.obtener_tareas_usuario("usuario2")  # Usuario no autorizado

def test_obtener_tareas_por_categoria_inexistente_20(gestor):
    tarea = Tarea(4, "usuario1", "Revisión del coche", "Mantenimiento")
    gestor.agregar_tarea(tarea)
    tareas = gestor.obtener_tareas_categoria("Magia")  # Categoría inexistente
    assert tareas == []  # Debe devolver una lista vacía

def test_agregar_tarea_con_fecha_pasada_21(gestor):
    tarea = Tarea(5, "usuario1", "Planear vacaciones", "Ocio", fecha="2020-01-01")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # Fecha no válida

def test_agregar_tarea_sin_usuario_22(gestor):
    tarea = Tarea(6, None, "Hacer la compra", "Compras")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # No debe permitir usuario None

def test_actualizar_tarea_inexistente_23(gestor):
    with pytest.raises(KeyError):
        gestor.actualizar_tarea(999, estado="Finalizada")  # ID de tarea inexistente

def test_obtener_tareas_usuario_sin_tareas_24(gestor):
    tareas = gestor.obtener_tareas_usuario("usuario3")  # Usuario sin tareas
    assert tareas == []  # Debe devolver lista vacía

def test_eliminar_tarea_con_id_no_numerico_25(gestor):
    with pytest.raises(TypeError):
        gestor.eliminar_tarea("abc")  # ID debe ser numérico

def test_agregar_tarea_con_categoria_vacia_26(gestor):
    tarea = Tarea(7, "usuario2", "Hacer café", "")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # Categoría no puede estar vacía
