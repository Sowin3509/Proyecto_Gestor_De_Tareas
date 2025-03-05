from services.gestor_tareas import GestorTareas
from models.tarea import Tarea

def menu():
    gestor = GestorTareas()
    while True:
        print("\n--- Gestor de Tareas ---")
        print("1. Agregar Tarea")
        print("2. Ver Tareas")
        print("3. Actualizar Estado de Tarea")
        print("4. Eliminar Tarea")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = input("Usuario: ")
            texto = input("Descripción de la tarea: ")
            categoria = input("Categoría: ")
            tarea = Tarea(None, usuario, texto, categoria)
            gestor.agregar_tarea(tarea)
            print("Tarea agregada con éxito.")

        elif opcion == "2":
            usuario = input("Ingrese su usuario: ")
            tareas = gestor.obtener_tareas(usuario)
            for tarea in tareas:
                print(tarea)

        elif opcion == "3":
            id_tarea = int(input("ID de la tarea a actualizar: "))
            nuevo_estado = input("Nuevo estado: ")
            gestor.actualizar_tarea(id_tarea, nuevo_estado)
            print("Tarea actualizada.")

        elif opcion == "4":
            id_tarea = int(input("ID de la tarea a eliminar: "))
            gestor.eliminar_tarea(id_tarea)
            print("Tarea eliminada.")

        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
