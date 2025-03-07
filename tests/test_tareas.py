import pytest
from services.gestor_tareas import GestorTareas
from models.tarea import Tarea
from services.gestor_tareas import GestorTareas, Tarea

# 54 pruebas con fallos intencionales
@pytest.fixture

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

def test_agregar_tarea_con_texto_muy_largo_27(gestor):
    texto_largo = "A" * 1001  # Más de 1000 caracteres
    tarea = Tarea(8, "usuario1", texto_largo, "Personal")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # No debe permitir descripciones muy largas

def test_eliminar_tarea_ya_eliminada_28(gestor):
    gestor.eliminar_tarea(1)  # Eliminar tarea con ID 1
    with pytest.raises(KeyError):
        gestor.eliminar_tarea(1)  # Intentar eliminarla de nuevo

def test_agregar_tarea_con_estado_no_valido_29(gestor):
    tarea = Tarea(9, "usuario2", "Leer un libro", "Educación")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea, estado="En progreso")  # Estado no definido

def test_obtener_tareas_usuario_inexistente_30(gestor):
    with pytest.raises(KeyError):
        gestor.obtener_tareas_usuario("usuario_no_existente")  # Usuario no registrado

def test_actualizar_tarea_con_estado_vacio_31(gestor):
    with pytest.raises(ValueError):
        gestor.actualizar_tarea(2, estado="")  # Estado no puede estar vacío

def test_agregar_tarea_con_id_negativo_32(gestor):
    tarea = Tarea(-1, "usuario3", "Comprar frutas", "Compras")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # No debe permitir IDs negativos

def test_actualizar_tarea_con_categoria_invalida_33(gestor):
    with pytest.raises(ValueError):
        gestor.actualizar_tarea(3, categoria="Entretenimiento")  # Categoría inexistente

def test_eliminar_tarea_con_id_no_numerico_34(gestor):
    with pytest.raises(TypeError):
        gestor.eliminar_tarea("dos")  # ID de tarea debe ser un número

def test_agregar_tarea_con_usuario_vacio_35(gestor):
    tarea = Tarea(10, "", "Llamar al banco", "Finanzas")
    with pytest.raises(ValueError):
        gestor.agregar_tarea(tarea)  # Usuario no puede estar vacío

def test_obtener_tareas_cuando_no_hay_tareas_36(gestor):
    gestor.limpiar_almacen()  # Vacía la lista de tareas
    assert gestor.obtener_todas_las_tareas() == []  # Debe devolver una lista vacía

def test_agregar_tarea_con_texto_extremadamente_largo_42(gestor):
    texto_largo = "A" * 1001  # Suponiendo que el límite es 1000 caracteres
    with pytest.raises(ValueError):
        gestor.agregar_tarea(Tarea(13, "usuario6", texto_largo, "Personal"))

def test_eliminar_tarea_con_id_negativo_43(gestor):
    with pytest.raises(ValueError):
        gestor.eliminar_tarea(-5)  # No debería permitir IDs negativos

def test_actualizar_tarea_de_otro_usuario_44(gestor):
    with pytest.raises(PermissionError):
        gestor.actualizar_tarea(3, texto="Nuevo texto", usuario="usuario_diferente")

def test_obtener_tareas_con_categoria_invalida_45(gestor):
    with pytest.raises(ValueError):
        gestor.obtener_tareas_categoria("Categoría inexistente")

def test_listar_tareas_ordenadas_por_fecha_invalida_46(gestor):
    with pytest.raises(ValueError):
        gestor.listar_tareas_ordenadas(criterio="fecha_inexistente")

def test_agregar_tarea_sin_usuario_47(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea(Tarea(14, None, "Hacer ejercicio", "Salud"))

def test_eliminar_tarea_no_existente_48(gestor):
    with pytest.raises(KeyError):
        gestor.eliminar_tarea(9999)  # Suponiendo que la tarea con ID 9999 no existe

def test_actualizar_tarea_con_usuario_vacio_49(gestor):
    with pytest.raises(ValueError):
        gestor.actualizar_tarea(3, texto="Nuevo texto", usuario="")

def test_obtener_tareas_por_usuario_inexistente_50(gestor):
    with pytest.raises(KeyError):
        gestor.obtener_tareas_usuario("usuario_inexistente")

def test_agregar_tarea_con_id_repetido_51(gestor):
    gestor.agregar_tarea(Tarea(15, "usuario7", "Ir al médico", "Salud"))
    with pytest.raises(ValueError):
        gestor.agregar_tarea(Tarea(15, "usuario8", "Leer un libro", "Educación"))  # ID duplicado

def test_actualizar_tarea_con_id_inexistente_52(gestor):
    with pytest.raises(KeyError):
        gestor.actualizar_tarea(999, texto="Texto nuevo")  # ID inexistente

def test_eliminar_tarea_con_caracteres_especiales_53(gestor):
    with pytest.raises(TypeError):
        gestor.eliminar_tarea("!@#$%^")  # ID con caracteres no válidos

def test_agregar_tarea_con_categoria_demasiado_larga_54(gestor):
    categoria_larga = "A" * 256  # Suponiendo que el límite es 255 caracteres
    with pytest.raises(ValueError):
        gestor.agregar_tarea(Tarea(16, "usuario9", "Revisar informes", categoria_larga))
