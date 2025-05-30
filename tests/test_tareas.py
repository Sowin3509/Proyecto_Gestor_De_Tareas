import pytest
from datetime import datetime
from services.gestor_tareas import GestorTareas
from exceptions.exceptions import (
    DescripcionVaciaError, TareaNoEncontradaError, UsuarioSinTareasError,
    CategoriaInvalidaError
)

# ------------------------- FIXTURE -------------------------
@pytest.fixture
def gestor():
    return GestorTareas()  # Modo memoria activado por defecto

# ------------------------- PRUEBAS UNITARIAS 54 -------------------------
def test_agregar_tarea_espacios_y_numeros(gestor):
    tarea_id = gestor.agregar_tarea("123 Juan", "Estudiar python 3.8", "estudio")
    assert gestor.tareas[tarea_id]['usuario'] == "123 Juan"

def test_categoria_case_sensitive(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("Maria", "Escribir informe", "Trabajo")  # con mayúscula

def test_agregar_tarea_con_tabulaciones(gestor):
    tarea_id = gestor.agregar_tarea("Teo", "\tLavar carro\t", "personal")
    assert "Lavar carro" in gestor.tareas[tarea_id]['descripcion']

def test_obtener_tareas_usuario_con_mayusculas(gestor):
    gestor.agregar_tarea("CARLOS", "Investigar Kivy", "trabajo")
    tareas = gestor.obtener_tareas_usuario("CARLOS")
    assert len(tareas) == 1

def test_eliminar_tras_obtener(gestor):
    tarea_id = gestor.agregar_tarea("Eva", "Pagar servicios", "personal")
    _ = gestor.obtener_tareas_usuario("Eva")
    gestor.eliminar_tarea(tarea_id)
    with pytest.raises(TareaNoEncontradaError):
        gestor.obtener_tarea(tarea_id)

def test_ids_no_se_reutilizan(gestor):
    id1 = gestor.agregar_tarea("Test", "T1", "trabajo")
    gestor.eliminar_tarea(id1)
    id2 = gestor.agregar_tarea("Test", "T2", "trabajo")
    assert id2 != id1

def test_agregar_100_tareas(gestor):
    for i in range(100):
        gestor.agregar_tarea("User", f"Tarea {i}", "personal")
    assert len(gestor.tareas) == 100

def test_error_personalizado_se_mantiene(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("Luis", " ", "trabajo")

def test_agregar_tarea_con_numeros(gestor):
    tarea_id = gestor.agregar_tarea("Usuario1", "Revisar tema 2.1", "trabajo")
    assert "2.1" in gestor.tareas[tarea_id]['descripcion']

def test_agregar_tarea_comilla_simple(gestor):
    tarea_id = gestor.agregar_tarea("Carlos", "Llamar a 'Mamá'", "personal")
    assert "'Mamá'" in gestor.tareas[tarea_id]['descripcion']

def test_agregar_tarea_comilla_doble(gestor):
    tarea_id = gestor.agregar_tarea("Laura", 'Leer "1984"', "estudio")
    assert '"1984"' in gestor.tareas[tarea_id]['descripcion']

def test_agregar_tarea_con_signos(gestor):
    tarea_id = gestor.agregar_tarea("Diego", "Hacer tarea #2!", "trabajo")
    assert "#2!" in gestor.tareas[tarea_id]['descripcion']

def test_eliminar_y_reagregar_misma_desc(gestor):
    id1 = gestor.agregar_tarea("User", "Desc", "personal")
    gestor.eliminar_tarea(id1)
    id2 = gestor.agregar_tarea("User", "Desc", "personal")
    assert id2 == id1 + 1

def test_multiple_usuarios_misma_desc(gestor):
    gestor.agregar_tarea("User1", "Desc", "personal")
    gestor.agregar_tarea("User2", "Desc", "personal")
    assert len(gestor.obtener_tareas_usuario("User1")) == 1
    assert len(gestor.obtener_tareas_usuario("User2")) == 1

def test_categoria_lowercase_only(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("Ana", "Test", "TRABAJO")

def test_categoria_vacia(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("Ana", "Test", "")

def test_usuario_con_espacios_internos(gestor):
    tarea_id = gestor.agregar_tarea("Juan Pérez", "Caminar", "personal")
    assert gestor.tareas[tarea_id]['usuario'] == "Juan Pérez"

def test_usuario_mayusculas_minusculas(gestor):
    gestor.agregar_tarea("luis", "Algo", "trabajo")
    tareas = gestor.obtener_tareas_usuario("luis")
    assert len(tareas) == 1

def test_eliminar_ultima_tarea(gestor):
    tarea_id = gestor.agregar_tarea("Lina", "Finalizar código", "trabajo")
    gestor.eliminar_tarea(tarea_id)
    with pytest.raises(TareaNoEncontradaError):
        gestor.obtener_tarea(tarea_id)

def test_eliminar_multiples_y_agregar_nueva(gestor):
    ids = [gestor.agregar_tarea("U", f"T{i}", "personal") for i in range(3)]
    for id_ in ids:
        gestor.eliminar_tarea(id_)
    nueva = gestor.agregar_tarea("U", "Nueva", "trabajo")
    assert nueva > ids[-1]

def test_descripcion_con_acentos(gestor):
    tarea_id = gestor.agregar_tarea("Pepe", "Estudiar álgebra", "estudio")
    assert "álgebra" in gestor.tareas[tarea_id]['descripcion']

def test_usuario_con_tilde(gestor):
    tarea_id = gestor.agregar_tarea("José", "Pintar", "personal")
    assert gestor.tareas[tarea_id]['usuario'] == "José"

def test_usuario_unicode(gestor):
    tarea_id = gestor.agregar_tarea("Renée", "Diseñar", "trabajo")
    assert gestor.tareas[tarea_id]['usuario'] == "Renée"

def test_obtener_y_eliminar_en_cadena(gestor):
    id_ = gestor.agregar_tarea("Ana", "Correr", "personal")
    gestor.obtener_tareas_usuario("Ana")
    gestor.eliminar_tarea(id_)
    with pytest.raises(TareaNoEncontradaError):
        gestor.obtener_tarea(id_)

def test_validar_longitud_max_descripcion(gestor):
    desc = "a" * 500
    tarea_id = gestor.agregar_tarea("Max", desc, "personal")
    assert len(gestor.tareas[tarea_id]['descripcion']) == 500

def test_validar_longitud_usuario(gestor):
    nombre = "a" * 100
    tarea_id = gestor.agregar_tarea(nombre, "Descripción", "trabajo")
    assert len(gestor.tareas[tarea_id]['usuario']) == 100

def test_ids_incrementales_despues_de_error(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("Ana", " ", "trabajo")
    id_ = gestor.agregar_tarea("Ana", "Bien", "trabajo")
    assert id_ == 1

def test_agregar_tareas_diferentes_usuarios(gestor):
    for i in range(10):
        gestor.agregar_tarea(f"Usuario{i}", f"Tarea {i}", "personal")
    assert len(gestor.tareas) == 10

def test_usuario_con_numeros_y_tilde(gestor):
    tarea_id = gestor.agregar_tarea("José123", "Escribir", "trabajo")
    assert gestor.tareas[tarea_id]['usuario'] == "José123"

def test_usuario_alfanumerico_mayus(gestor):
    tarea_id = gestor.agregar_tarea("CARLOS_99", "Programar", "trabajo")
    assert "CARLOS_99" in gestor.tareas[tarea_id]['usuario']

def test_descripcion_con_escape(gestor):
    tarea_id = gestor.agregar_tarea("Mia", "Nueva línea\nTest", "estudio")
    assert "\n" in gestor.tareas[tarea_id]['descripcion']

def test_categoria_con_espacio(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("Leo", "Tarea", " personal ")

def test_obtener_con_espacio_nombre(gestor):
    gestor.agregar_tarea("Laura", "Leer", "personal")
    tareas = gestor.obtener_tareas_usuario("Laura")
    assert len(tareas) == 1

def test_agregar_descripcion_con_hashtag(gestor):
    tarea_id = gestor.agregar_tarea("Nico", "#HackathonReady", "trabajo")
    assert "#HackathonReady" in gestor.tareas[tarea_id]['descripcion']

def test_nombre_usuario_minusculas_y_numeros(gestor):
    tarea_id = gestor.agregar_tarea("andres09", "Revisar PR", "personal")
    assert "andres09" in gestor.tareas[tarea_id]['usuario']

def test_agregar_tarea_valida(gestor):
    tarea_id = gestor.agregar_tarea("Juan", "Hacer mercado", "personal")
    assert tarea_id == 1

def test_agregar_tarea_duplicada(gestor):
    gestor.agregar_tarea("Juan", "Hacer mercado", "personal")
    id2 = gestor.agregar_tarea("Juan", "Hacer mercado", "personal")
    assert id2 == 2

def test_agregar_tarea_caracteres_especiales(gestor):
    tarea_id = gestor.agregar_tarea("Sofía", "Estudiar matemáticas #1!", "estudio")
    assert "#1!" in gestor.tareas[tarea_id]['descripcion']

def test_agregar_tarea_emojis(gestor):
    tarea_id = gestor.agregar_tarea("Andrés", "Comprar fruta 🍎", "personal")
    assert "🍎" in gestor.tareas[tarea_id]['descripcion']

def test_secuencia_agregar_eliminar_varios(gestor):
    ids = [gestor.agregar_tarea("User", f"Tarea {i}", "trabajo") for i in range(3)]
    for id_ in ids:
        gestor.eliminar_tarea(id_)
    assert len(gestor.tareas) == 0

def test_mismo_nombre_diferente_usuario(gestor):
    gestor.agregar_tarea("Juan", "Revisar correo", "trabajo")
    gestor.agregar_tarea("Pedro", "Revisar correo", "personal")
    tareas_juan = gestor.obtener_tareas_usuario("Juan")
    tareas_pedro = gestor.obtener_tareas_usuario("Pedro")
    assert tareas_juan[0]['descripcion'] == tareas_pedro[0]['descripcion']

def test_usuario_nombre_largo(gestor):
    nombre = "Usuario" * 20
    tarea_id = gestor.agregar_tarea(nombre, "Tarea especial", "personal")
    assert gestor.tareas[tarea_id]['usuario'] == nombre

def test_eliminar_tareas_intercaladas(gestor):
    ids = [gestor.agregar_tarea("User", f"Tarea {i}", "trabajo") for i in range(5)]
    for i in range(0, 5, 2):  # Eliminar ID impares
        gestor.eliminar_tarea(ids[i])
    assert len(gestor.tareas) == 2  # Deberían quedar 2 tareas

def test_agregar_tarea_usuario_vacio(gestor):
    with pytest.raises(ValueError):
        gestor.agregar_tarea("", "Hacer algo", "personal")

def test_agregar_tarea_descripcion_vacia(gestor):
    with pytest.raises(DescripcionVaciaError):
        gestor.agregar_tarea("Ana", "   ", "trabajo")

def test_agregar_tarea_categoria_invalida(gestor):
    with pytest.raises(CategoriaInvalidaError):
        gestor.agregar_tarea("Pedro", "Estudiar", "diversion")

@pytest.mark.parametrize("categoria", ["trabajo", "personal", "estudio"])
def test_agregar_tarea_categorias_validas(gestor, categoria):
    id_ = gestor.agregar_tarea("Luis", "Tarea prueba", categoria)
    assert gestor.tareas[id_]['categoria'] == categoria.lower()

@pytest.mark.parametrize("usuario,descripcion,categoria", [
    ("", "ok", "personal"),
    ("Juan", "", "trabajo"),
    ("Luisa", "Estudiar", "otro"),
    (" ", "Test", "personal"),
    ("Ana", "Clase", "")
])
def test_agregar_tarea_comb_invalidas(gestor, usuario, descripcion, categoria):
    with pytest.raises(Exception):
        gestor.agregar_tarea(usuario, descripcion, categoria)

"""
Módulo de pruebas unitarias para el gestor de tareas.

Este módulo contiene pruebas unitarias exhaustivas para la clase GestorTareas,
verificando su funcionalidad, manejo de errores y comportamiento en casos límite.

Estructura:
----------
- Fixture:
  * gestor: Proporciona una instancia limpia de GestorTareas para cada prueba.

- Pruebas unitarias:
  * Testeo de funcionalidad básica (CRUD)
  * Validación de entradas (usuarios, descripciones, categorías)
  * Manejo de caracteres especiales (unicode, emojis, acentos)
  * Comportamiento con casos límite (longitudes máximas, strings vacíos)
  * Verificación de IDs incrementales y no reutilizados
  * Pruebas parametrizadas para combinaciones de inputs

Características cubiertas:
-------------------------
- Manejo de usuarios: mayúsculas, minúsculas, tildes, espacios, alfanuméricos
- Descripciones: caracteres especiales, emojis, acentos, longitudes variables
- Categorías: validación estricta (solo lowercase), manejo de errores
- Operaciones: agregar, eliminar, obtener tareas con diferentes escenarios
- Robustez: manejo de errores personalizados, estado consistente tras operaciones

Excepciones probadas:
--------------------
- DescripcionVaciaError
- TareaNoEncontradaError
- UsuarioSinTareasError
- CategoriaInvalidaError

Ejemplos de casos testeados:
--------------------------
- Usuarios con caracteres especiales (tildes, números, espacios)
- Descripciones con emojis, acentos, caracteres de escape
- Categorías inválidas (mayúsculas, espacios, valores vacíos)
- Secuencias complejas de operaciones (agregar/eliminar múltiples)
- Comportamiento con 100+ tareas
- Verificación de IDs únicos e incrementales

Uso:
----
Ejecutar todas las pruebas con pytest:
pytest tests/test_tareas.py -v

"""