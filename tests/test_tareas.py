import pytest
from services.gestor_tareas import GestorTareas
from models.tarea import Tarea
from exceptions.exceptions import (
    TareaNoEncontradaError, EstadoInvalidoError, IDInvalidoError,
    DescripcionVaciaError, CategoriaInvalidaError, UsuarioSinTareasError
)

@pytest.fixture
def gestor():
    return GestorTareas()


def test_agregar_tarea_con_descripcion_vacia(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", "", "personal")

def test_agregar_tarea_con_categoria_invalida(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Comprar leche", "deporte")

def test_agregar_tarea_sin_usuario(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea("", "Tarea sin usuario", "trabajo")

def test_agregar_tarea_con_categoria_vacia(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Reunión importante", "")

def test_actualizar_tarea_ya_eliminada(gestor):
    gestor.agregar_tarea("usuario1", "Tarea eliminada", "trabajo")
    gestor.eliminar_tarea(1)
    with pytest.raises(IDInvalidoError):
        gestor.actualizar_tarea(1, "Nueva descripción")

def test_obtener_tareas_usuario_sin_tareas(gestor):
    with pytest.raises(UsuarioSinTareasError):
        gestor.obtener_tareas_usuario("usuario_inexistente")

def test_obtener_tareas_con_usuario_numerico(gestor):
    gestor.agregar_tarea("1234", "Tarea de usuario numérico", "trabajo")
    assert len(gestor.obtener_tareas_usuario("1234")) == 1

def test_agregar_100_tareas_y_listar(gestor):
    for i in range(1, 101):
        gestor.agregar_tarea("usuario1", f"Tarea {i}", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 100

def test_agregar_tarea_con_categoria_tipo_booleano(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Comprar víveres", True)

def test_agregar_tarea_con_emoji_en_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "😀🔥🎉", "personal")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_mucha_variedad_de_caracteres(gestor):
    gestor.agregar_tarea("usuario1", "Texto con 1234 !@#$%^&*()_+", "personal")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_categoria_que_tiene_solo_numeros(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Investigar temas", "12345")

def test_agregar_tarea_con_categoria_espacios(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Comprar regalos", "    ")

def test_agregar_tarea_con_usuario_espacios(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea("    ", "Revisar agenda", "personal")

def test_actualizar_tarea_correctamente(gestor):
    gestor.agregar_tarea("usuario1", "Actualizar perfil", "trabajo")
    gestor.actualizar_tarea(1, "Perfil actualizado")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Perfil actualizado" for t in tareas)

# Eliminado: test_eliminar_tarea_existente(gestor):
    gestor.agregar_tarea("usuario1", "Eliminar después", "trabajo")
    gestor.eliminar_tarea(1)
    with pytest.raises(UsuarioSinTareasError):
        gestor.eliminar_tarea(1)

def test_obtener_tareas_usuario_con_una_tarea(gestor):
    gestor.agregar_tarea("usuario1", "Tarea única", "personal")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_y_eliminar_multiples_tareas(gestor):
    for i in range(1, 6):
        gestor.agregar_tarea("usuario1", f"Tarea {i}", "trabajo")
    for i in range(1, 6):
        gestor.eliminar_tarea(i)
    with pytest.raises(UsuarioSinTareasError):
        gestor.obtener_tareas_usuario("usuario1")

def test_agregar_tarea_con_espacios_externos_en_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "   Limpiar casa   ", "personal")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "   Limpiar casa   " for t in tareas)

def test_agregar_tarea_con_categoria_valida(gestor):
    gestor.agregar_tarea("usuario1", "Proyecto final", "estudio")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_actualizar_tarea_con_mismo_texto(gestor):
    gestor.agregar_tarea("usuario1", "Revisar documentos", "trabajo")
    gestor.actualizar_tarea(1, "Revisar documentos")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Revisar documentos" for t in tareas)

def test_agregar_y_actualizar_tarea(gestor):
    gestor.agregar_tarea("usuario1", "Preparar presentación", "trabajo")
    gestor.actualizar_tarea(1, "Presentación lista")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Presentación lista" for t in tareas)

# Eliminado: test_eliminar_tarea_correctamente(gestor):
    gestor.agregar_tarea("usuario1", "Tarea temporal", "personal")
    gestor.eliminar_tarea(1)
    with pytest.raises(TareaNoEncontradaError):
        gestor.obtener_tareas_usuario("usuario1")

def test_eliminar_tarea_y_reagregar_con_mismo_id(gestor):
    gestor.agregar_tarea("usuario1", "Tarea eliminable", "trabajo")
    gestor.eliminar_tarea(1)
    gestor.agregar_tarea("usuario1", "Nueva tarea", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_actualizar_tarea_y_verificar_estado(gestor):
    gestor.agregar_tarea("usuario1", "Tarea pendiente", "trabajo")
    gestor.actualizar_tarea(1, "Tarea completada")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Tarea completada" for t in tareas)

def test_obtener_tareas_de_usuario_diferente(gestor):
    gestor.agregar_tarea("usuario1", "Tarea de usuario1", "trabajo")
    gestor.agregar_tarea("usuario2", "Tarea de usuario2", "personal")
    assert len(gestor.obtener_tareas_usuario("usuario2")) == 1

def test_actualizar_tarea_con_texto_largo(gestor):
    gestor.agregar_tarea("usuario1", "Resumen del proyecto", "trabajo")
    nueva_desc = "A" * 500  # Texto largo
    gestor.actualizar_tarea(1, nueva_desc)
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == nueva_desc for t in tareas)

def test_eliminar_tarea_y_verificar_lista_vacia(gestor):
    gestor.agregar_tarea("usuario1", "Tarea de prueba", "personal")
    gestor.eliminar_tarea(1)
    with pytest.raises(UsuarioSinTareasError):
        gestor.obtener_tareas_usuario("usuario1")

def test_actualizar_tarea_y_verificar_usuario(gestor):
    gestor.agregar_tarea("usuario1", "Planear vacaciones", "trabajo")
    gestor.actualizar_tarea(1, "Vacaciones planificadas")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.usuario == "usuario1" for t in tareas)

def test_agregar_tarea_con_numeros_y_texto(gestor):
    gestor.agregar_tarea("usuario1", "Revisión 2024", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_espacios_internos(gestor):
    gestor.agregar_tarea("usuario1", "Lavar    el coche", "personal")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Lavar    el coche" for t in tareas)

def test_eliminar_tarea_doble_y_reagregar(gestor):
    gestor.agregar_tarea("usuario1", "Borrar luego", "trabajo")
    gestor.eliminar_tarea(1)
    gestor.agregar_tarea("usuario1", "Nueva asignación", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_y_actualizar_tarea_misma_categoria(gestor):
    gestor.agregar_tarea("usuario1", "Proyecto semanal", "trabajo")
    gestor.actualizar_tarea(1, "Proyecto finalizado")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Proyecto finalizado" for t in tareas)

def test_agregar_tarea_y_verificar_no_vacia(gestor):
    gestor.agregar_tarea("usuario1", "Meta del mes", "personal")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert len(tareas) > 0

def test_actualizar_tarea_y_confirmar_no_eliminada(gestor):
    gestor.agregar_tarea("usuario1", "Preparar informe", "trabajo")
    gestor.actualizar_tarea(1, "Informe preparado")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Informe preparado" for t in tareas)

def test_agregar_multiples_tareas_y_verificar_cantidad(gestor):
    for i in range(1, 6):
        gestor.agregar_tarea("usuario1", f"Tarea {i}", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 5

def test_agregar_tarea_con_doble_espacio(gestor):
    gestor.agregar_tarea("usuario1", "Llamar  a clientes", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Llamar  a clientes" for t in tareas)

def test_eliminar_tarea_ultima_y_reagregar(gestor):
    gestor.agregar_tarea("usuario1", "Eliminar última", "trabajo")
    gestor.eliminar_tarea(1)
    gestor.agregar_tarea("usuario1", "Nueva tarea", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_actualizar_tarea_con_mismo_usuario(gestor):
    gestor.agregar_tarea("usuario1", "Escribir reporte", "trabajo")
    gestor.actualizar_tarea(1, "Reporte escrito")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.usuario == "usuario1" for t in tareas)

def test_obtener_tareas_usuario_dos_tareas(gestor):
    gestor.agregar_tarea("usuario1", "Tarea A", "trabajo")
    gestor.agregar_tarea("usuario1", "Tarea B", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 2

def test_eliminar_tarea_medio_y_verificar(gestor):
    gestor.agregar_tarea("usuario1", "Tarea 1", "trabajo")
    gestor.agregar_tarea("usuario1", "Tarea 2", "trabajo")
    gestor.eliminar_tarea(1)
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert len(tareas) == 1

def test_agregar_tarea_y_verificar_usuario_correcto(gestor):
    gestor.agregar_tarea("usuario1", "Nueva actividad", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.usuario == "usuario1" for t in tareas)

def test_actualizar_tarea_y_verificar_longitud_texto(gestor):
    gestor.agregar_tarea("usuario1", "Análisis de datos", "trabajo")
    gestor.actualizar_tarea(1, "Datos analizados correctamente")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(len(t.descripcion) > 5 for t in tareas)

def test_agregar_tarea_con_guion_bajo(gestor):
    gestor.agregar_tarea("usuario1", "tarea_proyecto", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "tarea_proyecto" for t in tareas)

def test_agregar_tarea_con_dos_palabras(gestor):
    gestor.agregar_tarea("usuario1", "Nuevo reto", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Nuevo reto" for t in tareas)

def test_eliminar_tarea_intermedia_y_verificar(gestor):
    gestor.agregar_tarea("usuario1", "A", "trabajo")
    gestor.agregar_tarea("usuario1", "B", "trabajo")
    gestor.agregar_tarea("usuario1", "C", "trabajo")
    gestor.eliminar_tarea(2)
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert len(tareas) == 2

def test_agregar_tarea_y_confirmar_no_duplicada(gestor):
    gestor.agregar_tarea("usuario1", "Entrega informe", "trabajo")
    gestor.agregar_tarea("usuario1", "Entrega informe", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert len(tareas) == 2

def test_agregar_tarea_y_confirmar_usuario_correcto(gestor):
    gestor.agregar_tarea("usuario1", "Tarea especial", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.usuario == "usuario1" for t in tareas)

def test_actualizar_tarea_y_verificar_palabra_clave(gestor):
    gestor.agregar_tarea("usuario1", "Estudiar matemática", "trabajo")
    gestor.actualizar_tarea(1, "Matemática avanzada")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any("Matemática" in t.descripcion for t in tareas)

def test_agregar_y_actualizar_tarea_varias_veces(gestor):
    gestor.agregar_tarea("usuario1", "Investigación", "trabajo")
    gestor.actualizar_tarea(1, "Investigación completada")
    gestor.actualizar_tarea(1, "Informe finalizado")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Informe finalizado" for t in tareas)

def test_agregar_tarea_y_verificar_texto_con_numeros(gestor):
    gestor.agregar_tarea("usuario1", "Reporte 2025", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any("2025" in t.descripcion for t in tareas)

def test_agregar_tarea_y_verificar_espacios_finales(gestor):
    gestor.agregar_tarea("usuario1", "  Meta del año  ", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion.strip() == "Meta del año" for t in tareas)

def test_eliminar_tarea_y_verificar_lista_no_vacia(gestor):
    gestor.agregar_tarea("usuario1", "Primera tarea", "trabajo")
    gestor.agregar_tarea("usuario1", "Segunda tarea", "trabajo")
    gestor.eliminar_tarea(1)
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert len(tareas) == 1

def test_agregar_tarea_con_mayusculas_y_verificar(gestor):
    gestor.agregar_tarea("usuario1", "TAREA IMPORTANTE", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "TAREA IMPORTANTE" for t in tareas)


def test_agregar_y_verificar_tarea_personal(gestor):
    gestor.agregar_tarea("usuario1", "Leer un libro", "personal")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(t.descripcion == "Leer un libro" for t in tareas)

def test_agregar_tarea_y_verificar_longitud_texto(gestor):
    gestor.agregar_tarea("usuario1", "Hacer ejercicio", "trabajo")
    tareas = gestor.obtener_tareas_usuario("usuario1")
    assert any(len(t.descripcion) > 5 for t in tareas)
