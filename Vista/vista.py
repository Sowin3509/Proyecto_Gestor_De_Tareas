from services.gestor_tareas import GestorTareas

gestor = GestorTareas()

def mostrar_menu():
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
            descripcion = input("Descripción de la tarea: ")
            categoria = input("Categoría: ")
            gestor.agregar_tarea(usuario, descripcion, categoria)
            print("✅ Tarea agregada con éxito.")

        elif opcion == "2":
            usuario = input("Ingrese su usuario: ")
            tareas = gestor.obtener_tareas(usuario)
            if tareas:
                for tarea in tareas:
                    print(f"[{tarea['id']}] {tarea['descripcion']} - {tarea['categoria']} - {tarea['estado']}")
            else:
                print("⚠ No hay tareas registradas para este usuario.")

        elif opcion == "3":
            tarea_id = int(input("ID de la tarea a actualizar: "))
            nuevo_estado = input("Nuevo estado (1: Pendiente, 2: En progreso, 3: Completada): ").strip()
            if gestor.actualizar_tarea(tarea_id, nuevo_estado):
                print("✅ Tarea actualizada correctamente.")
            else:
                print("⚠ No se pudo actualizar la tarea.")

        elif opcion == "4":
            tarea_id = int(input("ID de la tarea a eliminar: "))
            if gestor.eliminar_tarea(tarea_id):
                print("✅ Tarea eliminada correctamente.")
            else:
                print("⚠ No se encontró la tarea.")

        elif opcion == "5":
            print("👋 Saliendo del programa.")
            break

        else:
            print("⚠ Opción inválida. Intente nuevamente.")
