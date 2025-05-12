import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.usuario import Usuario

from services.gestor_tareas import GestorTareas
from exceptions.exceptions import (
    DescripcionVaciaError, TareaNoEncontradaError, UsuarioSinTareasError,
    CategoriaInvalidaError
)

class AppConsola:
    def __init__(self):
        self.__usuariosRegistrados = {}  # Dict[str, Usuario]
        self.__usuarioActual = None
        self.__gestor = GestorTareas()

    def mostrarMenu(self):
        print("\n--- GESTOR DE TAREAS ---")
        if self.__usuarioActual:
            print(f"🔒 Sesión activa como: {self.__usuarioActual}")
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        if self.__usuarioActual:
            print("3. Agregar tarea")
            print("4. Eliminar tarea")
            print("5. Ver mis tareas")
            print("6. Cerrar sesión")
        print("7. Salir")

    def crearCuenta(self):
        nombre = input("🧾 Ingresa un nombre de usuario: ").strip()
        if nombre in self.__usuariosRegistrados:
            print("⚠️ Ese usuario ya está registrado.")
        else:
            clave = input("🔑 Ingresa tu contraseña: ").strip()
            self.__usuariosRegistrados[nombre] = Usuario(nombre, clave)
            print("✅ Usuario registrado con éxito.")


    def iniciarSesion(self):
        nombre = input("🔐 Ingresa tu nombre de usuario: ").strip()
        clave = input("🔑 Ingresa tu contraseña: ").strip()

        if nombre in self.__usuariosRegistrados:
            usuario = self.__usuariosRegistrados[nombre]
            if usuario.verificarClave(clave):
                self.__usuarioActual = usuario.nombre
                print(f"✅ Sesión iniciada como {self.__usuarioActual}")
            else:
                print("🚫 Contraseña incorrecta.")
        else:
            print("🚫 Usuario no registrado.")



    def cerrarSesion(self):
        print(f"🔓 Sesión cerrada de {self.__usuarioActual}")
        self.__usuarioActual = None

    def agregarTarea(self):
        if not self.__usuarioActual:
            print("🚫 Debes iniciar sesión para agregar tareas.")
            return
        descripcion = input("📝 Descripción de la tarea: ")
        categoria = input("📂 Categoría (trabajo/personal/estudio): ")
        try:
            tareaId = self.__gestor.agregar_tarea(self.__usuarioActual, descripcion, categoria)
            print(f"✅ Tarea agregada con ID {tareaId}")
        except (DescripcionVaciaError, CategoriaInvalidaError, ValueError) as e:
            print(f"❌ Error: {e}")

    def eliminarTarea(self):
        if not self.__usuarioActual:
            print("🚫 Debes iniciar sesión para eliminar tareas.")
            return
        try:
            tareaId = int(input("🗑️ ID de la tarea a eliminar: "))
            self.__gestor.eliminar_tarea(tareaId)
            print("✅ Tarea eliminada correctamente.")
        except (TareaNoEncontradaError, ValueError) as e:
            print(f"❌ Error: {e}")

    def verMisTareas(self):
        if not self.__usuarioActual:
            print("🚫 Debes iniciar sesión para ver tus tareas.")
            return
        try:
            tareas = self.__gestor.obtener_tareas_usuario(self.__usuarioActual)
            print(f"📋 Tareas de {self.__usuarioActual}:")
            for t in tareas:
                print(f"- [{t.id}] {t.descripcion} ({t.categoria})")
        except UsuarioSinTareasError as e:
            print(f"⚠️ {e}")

    def ejecutar(self):
        while True:
            self.mostrarMenu()
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.crearCuenta()
            elif opcion == "2":
                self.iniciarSesion()
            elif opcion == "3" and self.__usuarioActual:
                self.agregarTarea()
            elif opcion == "4" and self.__usuarioActual:
                self.eliminarTarea()
            elif opcion == "5" and self.__usuarioActual:
                self.verMisTareas()
            elif opcion == "6" and self.__usuarioActual:
                self.cerrarSesion()
            elif opcion == "7":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida o requiere iniciar sesión.")

if __name__ == "__main__":
    app = AppConsola()
    app.ejecutar()


"""
Módulo principal de la aplicación de gestión de tareas en consola.

Este módulo implementa una interfaz de línea de comandos (CLI) interactiva para el
sistema de gestión de tareas, con autenticación de usuarios y operaciones CRUD.

Estructura:
----------
- AppConsola: Clase principal que maneja:
  * Autenticación de usuarios (registro/login/logout)
  * Operaciones con tareas (crear/eliminar/listar)
  * Flujo principal de la aplicación

- Dependencias:
  * models.usuario: Gestiona la entidad Usuario
  * services.gestor_tareas: Maneja la lógica de negocio de tareas
  * exceptions.exceptions: Contiene excepciones personalizadas

Funcionalidades clave:
---------------------
✔ Sistema de autenticación con usuarios y contraseñas
✔ Menú contextual que cambia según estado de sesión
✔ Gestión completa de tareas (CRUD)
✔ Manejo de errores con mensajes descriptivos
✔ Persistencia de datos en memoria (durante ejecución)

Flujo de trabajo:
----------------
1. Inicio de aplicación -> Muestra menú principal
2. Usuario debe registrarse o iniciar sesión
3. Menú ampliado muestra opciones de gestión de tareas
4. Operaciones disponibles:
   - Agregar tareas con categorías específicas
   - Eliminar tareas por ID
   - Listar todas las tareas del usuario
   - Cerrar sesión
5. Salir del programa

Manejo de errores:
-----------------
- DescripcionVaciaError: Validación de descripciones no vacías
- TareaNoEncontradaError: Al intentar operar con tareas inexistentes
- UsuarioSinTareasError: Cuando un usuario no tiene tareas registradas
- CategoriaInvalidaError: Validación de categorías permitidas

Ejemplo de uso:
--------------
>>> python app_consola.py
--- GESTOR DE TAREAS ---
1. Crear cuenta
2. Iniciar sesión
7. Salir
Selecciona una opción: 1
🧾 Ingresa un nombre de usuario: prueba
🔑 Ingresa tu contraseña: ***
✅ Usuario registrado con éxito.

Notas de implementación:
----------------------
- Estado mantenido en memoria durante la ejecución
- Interfaz intuitiva con emojis visuales
- Validación de inputs en cada operación
- Separación clara entre:
  * Lógica de presentación (esta clase)
  * Lógica de negocio (gestor_tareas)
  * Modelos de datos (usuario)
"""