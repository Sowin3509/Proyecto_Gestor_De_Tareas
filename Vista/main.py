import vista

if __name__ == "__main__":
    vista.mostrar_menu()

"""
Punto de entrada principal de la aplicación de gestión de tareas.

Este módulo inicia la interfaz de usuario de la aplicación, mostrando el menú principal
y gestionando el flujo inicial del programa.

Funcionalidad:
-------------
- Importa e inicializa el módulo de vista que contiene la interfaz de usuario.
- Ejecuta la función principal mostrar_menu() cuando el script es ejecutado directamente.

Uso:
----
Para iniciar la aplicación:
1. Ejecutar este archivo directamente:
   $ python nombre_del_archivo.py

2. La aplicación mostrará el menú interactivo principal donde el usuario podrá:
   * Gestionar tareas (crear, modificar, eliminar)
   * Realizar búsquedas y filtros
   * Acceder a diferentes funcionalidades del sistema

Dependencias:
------------
- Requiere el módulo 'vista' que contiene la implementación de la interfaz de usuario.
- El módulo 'vista' debe tener implementada la función mostrar_menu().

Notas:
------
- Este archivo sigue el patrón clásico de Python para puntos de entrada (__name__ == "__main__")
- La separación entre este módulo principal y la vista permite una fácil modificación
  de la interfaz sin afectar el punto de entrada.
"""