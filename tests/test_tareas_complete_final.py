import pytest
from services.gestor_tareas import GestorTareas
from models.tarea import Tarea
from exceptions.custom_exceptions import (
    TareaNoEncontradaError, EstadoInvalidoError, IDInvalidoError,
    DescripcionVaciaError, CategoriaInvalidaError, UsuarioSinTareasError
)

@pytest.fixture
def gestor():
    return GestorTareas()

# --- Pruebas de agregar tarea ---
def test_agregar_tarea_con_descripcion_vacia(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", "", "personal")

def test_agregar_tarea_con_categoria_invalida(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Comprar leche", "deporte")

def test_agregar_tarea_con_id_negativo(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.agregar_tarea("usuario1", "Hacer ejercicio", "trabajo", id_tarea=-5)

def test_agregar_tarea_con_categoria_vacia(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Preparar presentación", "")

def test_agregar_tarea_sin_usuario(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea("", "Revisar correos", "trabajo")

def test_agregar_tarea_con_texto_extremadamente_largo(gestor):
    descripcion_larga = "A" * 1001  # Supongamos que hay un límite de 1000 caracteres
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", descripcion_larga, "personal")

# --- Pruebas de actualizar tarea ---
def test_actualizar_tarea_con_id_inexistente(gestor):
    with pytest.raises(TareaNoEncontradaError):
        gestor.actualizar_tarea(999, "Completada")

def test_actualizar_tarea_sin_nueva_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "Organizar escritorio", "personal")
    with pytest.raises(DescripcionVaciaError):
        gestor.actualizar_tarea(1, "")

def test_actualizar_estado_tarea_invalido(gestor):
    gestor.agregar_tarea("usuario1", "Leer un libro", "personal")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "Pendiente de aprobación")

def test_actualizar_tarea_con_id_negativo(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.actualizar_tarea(-1, "Completada")

# --- Pruebas de eliminar tarea ---
def test_eliminar_tarea_no_existente(gestor):
    with pytest.raises(TareaNoEncontradaError):
        gestor.eliminar_tarea(1000)

def test_eliminar_tarea_con_id_negativo(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea(-10)

def test_eliminar_tarea_con_caracteres_especiales(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("!@#$%")

# --- Pruebas de obtener tareas ---
def test_obtener_tareas_usuario_sin_tareas(gestor):
    with pytest.raises(UsuarioSinTareasError):
        gestor.obtener_tareas_usuario("usuario_inexistente")

def test_obtener_tareas_con_usuario_vacio(gestor):
    with pytest.raises(ValueError):
        gestor.obtener_tareas_usuario("")

# --- Casos extremos y seguridad ---
def test_agregar_tarea_muchos_caracteres(gestor):
    descripcion = "A" * 5000  # Prueba con texto excesivo
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", descripcion, "trabajo")

def test_actualizar_tarea_a_muchos_estados_invalidos(gestor):
    gestor.agregar_tarea("usuario1", "Revisar correos", "personal")
    for estado in ["Aprobado", "Rechazado", "Cancelado", "Borrador"]:
        with pytest.raises(EstadoInvalidoError):
            gestor.actualizar_tarea(1, estado)

def test_eliminar_tarea_mas_de_una_vez(gestor):
    gestor.agregar_tarea("usuario1", "Tarea temporal", "trabajo")
    gestor.eliminar_tarea(1)
    with pytest.raises(TareaNoEncontradaError):
        gestor.eliminar_tarea(1)

def test_listar_tareas_multiples_usuarios(gestor):
    gestor.agregar_tarea("usuario1", "Tarea A", "personal")
    gestor.agregar_tarea("usuario2", "Tarea B", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1
    assert len(gestor.obtener_tareas_usuario("usuario2")) == 1

def test_obtener_tareas_usuario_con_numeros(gestor):
    gestor.agregar_tarea("12345", "Tarea numérica", "trabajo")
    assert len(gestor.obtener_tareas_usuario("12345")) == 1

# Más pruebas hasta completar 54...


# --- Más pruebas de agregar tarea ---
def test_agregar_tarea_con_espacios_en_descripcion(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", "    ", "personal")

def test_agregar_tarea_con_numeros_en_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "123456", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_simbolos_en_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "@@@###$$$", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_usuario_nulo(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea(None, "Descripción válida", "personal")

# --- Más pruebas de actualizar tarea ---
def test_actualizar_tarea_con_estado_vacio(gestor):
    gestor.agregar_tarea("usuario1", "Leer un libro", "personal")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "")

def test_actualizar_tarea_con_estado_numerico(gestor):
    gestor.agregar_tarea("usuario1", "Ordenar archivos", "personal")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "123")

def test_actualizar_tarea_con_usuario_inexistente(gestor):
    with pytest.raises(TareaNoEncontradaError):
        gestor.actualizar_tarea(999, "Completada")

def test_actualizar_tarea_con_multiples_espacios(gestor):
    gestor.agregar_tarea("usuario1", "Dormir temprano", "salud")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "    ")

# --- Más pruebas de eliminar tarea ---
def test_eliminar_tarea_dos_veces(gestor):
    gestor.agregar_tarea("usuario1", "Ejercicio matutino", "salud")
    gestor.eliminar_tarea(1)
    with pytest.raises(TareaNoEncontradaError):
        gestor.eliminar_tarea(1)

def test_eliminar_tarea_con_id_texto(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("texto_id")

def test_eliminar_tarea_con_espacios(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("   ")

def test_eliminar_tarea_con_caracteres_especiales_extremos(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("&&**$$!!")

# --- Más pruebas de obtener tareas ---
def test_obtener_tareas_usuario_con_espacios(gestor):
    with pytest.raises(ValueError):
        gestor.obtener_tareas_usuario("    ")

def test_obtener_tareas_usuario_con_numeros(gestor):
    gestor.agregar_tarea("78910", "Tarea de prueba", "trabajo")
    assert len(gestor.obtener_tareas_usuario("78910")) == 1

def test_obtener_tareas_usuario_inexistente(gestor):
    with pytest.raises(UsuarioSinTareasError):
        gestor.obtener_tareas_usuario("no_existe")

# --- Casos extremos adicionales ---
def test_agregar_100_tareas_y_listar(gestor):
    for i in range(1, 101):
        gestor.agregar_tarea("usuario1", f"Tarea {i}", "trabajo")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 100

def test_intentar_actualizar_tarea_eliminada(gestor):
    gestor.agregar_tarea("usuario1", "Tarea a eliminar", "trabajo")
    gestor.eliminar_tarea(1)
    with pytest.raises(TareaNoEncontradaError):
        gestor.actualizar_tarea(1, "Nueva descripción")

def test_crear_tarea_con_categoria_extremadamente_larga(gestor):
    categoria_larga = "A" * 1000
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Descripción válida", categoria_larga)

def test_intentar_eliminar_tarea_con_id_extremadamente_largo(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("1" * 500)

def test_actualizar_tarea_con_estado_caracteres_especiales(gestor):
    gestor.agregar_tarea("usuario1", "Jugar videojuegos", "ocio")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "!@#$%^")

def test_obtener_tareas_con_usuario_numérico(gestor):
    gestor.agregar_tarea("1234", "Tarea de usuario numérico", "trabajo")
    assert len(gestor.obtener_tareas_usuario("1234")) == 1


# --- Últimos 13 tests para completar los 54 ---

def test_agregar_tarea_con_emoji_en_descripcion(gestor):
    gestor.agregar_tarea("usuario1", "😀🔥🎉", "ocio")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_agregar_tarea_con_mucha_variedad_de_caracteres(gestor):
    gestor.agregar_tarea("usuario1", "Texto con 1234 !@#$%^&*()_+", "personal")
    assert len(gestor.obtener_tareas_usuario("usuario1")) == 1

def test_actualizar_tarea_con_estado_vacio_y_espacios(gestor):
    gestor.agregar_tarea("usuario1", "Leer un libro", "personal")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "   ")

def test_eliminar_tarea_con_cadena_larga_de_texto(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea("x" * 500)

def test_actualizar_tarea_con_estado_que_contiene_numeros(gestor):
    gestor.agregar_tarea("usuario1", "Hacer deporte", "salud")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "Estado123")

def test_agregar_tarea_con_titulo_extremadamente_largo(gestor):
    descripcion_larga = "Tarea " + "A" * 2000  # Más de 2000 caracteres
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("usuario1", descripcion_larga, "trabajo")

def test_actualizar_tarea_con_estado_tipo_lista(gestor):
    gestor.agregar_tarea("usuario1", "Meditar", "salud")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, ["Completado"])

def test_eliminar_tarea_con_estado_booleano(gestor):
    with pytest.raises(IDInvalidoError):
        gestor.eliminar_tarea(True)

def test_obtener_tareas_con_usuario_tipo_lista(gestor):
    with pytest.raises(ValueError):
        gestor.obtener_tareas_usuario(["usuario1"])

def test_agregar_tarea_con_categoria_que_tiene_solo_numeros(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Investigar temas", "12345")

def test_actualizar_tarea_con_estado_con_espacios_y_mayúsculas(gestor):
    gestor.agregar_tarea("usuario1", "Estudiar", "personal")
    with pytest.raises(EstadoInvalidoError):
        gestor.actualizar_tarea(1, "     COMPLETADO     ")

def test_agregar_tarea_con_categoria_tipo_booleano(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("usuario1", "Comprar víveres", True)

def test_obtener_tareas_con_usuario_tipo_numero(gestor):
    with pytest.raises(ValueError):
        gestor.obtener_tareas_usuario(12345)
