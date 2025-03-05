from services.gestor_tareas import GestorTareas
import sqlite3
from database.conexion import ConexionDB
from models.tarea import Tarea
from models.usuario import Usuario

def registrar_usuario(gestor):
    print("\n--- Registro de Usuario ---")
    usuario = input("Ingrese un nombre de usuario: ")
    contraseña = input("Ingrese una contraseña: ")
    
    if gestor.registrar_usuario(usuario, contraseña):  # Llamar al método de GestorTareas
        print("Usuario registrado con éxito.")
    else:
        print("El usuario ya existe.")

def iniciar_sesion(gestor):
    print("\n--- Inicio de Sesión ---")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    
    if gestor.autenticar_usuario(usuario, contraseña):
        print("Inicio de sesión exitoso.")
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None

def cambiar_contraseña(gestor, usuario):
    print("\n--- Cambiar Contraseña ---")
    contraseña_actual = input("Ingrese su contraseña actual: ")
    nueva_contraseña = input("Ingrese su nueva contraseña: ")
    
    if gestor.cambiar_contraseña(usuario, contraseña_actual, nueva_contraseña):
        print("Contraseña cambiada con éxito.")
    else:
        print("Contraseña actual incorrecta o usuario no encontrado.")

def menu(usuario, gestor):
    while True:
        print("\n--- Gestor de Tareas ---")
        print("1. Agregar Tarea")
        print("2. Ver Tareas")
        print("3. Actualizar Estado de Tarea")
        print("4. Cambiar Contraseña")
        print("5. Eliminar Tarea")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            texto = input("Descripción de la tarea: ")
            categoria = input("Categoría: ")
            tarea = Tarea(None, usuario, texto, categoria)
            gestor.agregar_tarea(tarea)
            print("Tarea agregada con éxito.")

        elif opcion == "2":
            tareas = gestor.obtener_tareas(usuario)
            for tarea in tareas:
                print(tarea)

        elif opcion == "3":
            id_tarea = int(input("ID de la tarea a actualizar: "))
            nuevo_estado = input("Nuevo estado: ")
            gestor.actualizar_tarea(id_tarea, nuevo_estado)
            print("Tarea actualizada.")

        elif opcion == "4":
            cambiar_contraseña(gestor, usuario)
            print("Contraseña cambiada con éxito.")

        elif opcion == "5":
            id_tarea = int(input("ID de la tarea a eliminar: "))
            gestor.eliminar_tarea(id_tarea)
            print("Tarea eliminada.")

        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    gestor = GestorTareas()
    while True:
        print("\n--- Bienvenido al Gestor de Tareas ---")
        print("1. Iniciar Sesión")
        print("2. Registrar Usuario")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = iniciar_sesion(gestor)
            if usuario:
                menu(usuario, gestor)
        elif opcion == "2":
            registrar_usuario(gestor)

        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, intenta de nuevo.")