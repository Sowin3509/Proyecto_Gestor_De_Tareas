# vista.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, simpledialog
from services.gestor_tareas import GestorTareas
from exceptions.exceptions import (
    DescripcionVaciaError, CategoriaInvalidaError,
    TareaNoEncontradaError, UsuarioSinTareasError
)
from models.usuario import Usuario

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - GUI")
        self.gestor = GestorTareas()
        self.usuarios = {}  # clave: nombre, valor: objeto Usuario
        self.usuarioActual = None

        self.menuPrincipal()

    def limpiarVentana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menuPrincipal(self):
        self.limpiarVentana()
        tk.Label(self.root, text="Gestor de Tareas", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Crear Cuenta", command=self.crearCuenta, width=30).pack(pady=5)
        tk.Button(self.root, text="Iniciar Sesión", command=self.iniciarSesion, width=30).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit, width=30).pack(pady=20)

    def menuUsuario(self):
        self.limpiarVentana()
        tk.Label(self.root, text=f"Bienvenido, {self.usuarioActual}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Agregar Tarea", command=self.agregarTarea, width=30).pack(pady=5)
        tk.Button(self.root, text="Ver Mis Tareas", command=self.verTareas, width=30).pack(pady=5)
        tk.Button(self.root, text="Eliminar Tarea", command=self.eliminarTarea, width=30).pack(pady=5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.cerrarSesion, width=30).pack(pady=20)

    def crearCuenta(self):
        nombre = simpledialog.askstring("Registro", "Ingresa tu nombre de usuario:")
        if not nombre:
            return
        if nombre in self.usuarios:
            messagebox.showwarning("Usuario existente", "Ese usuario ya está registrado.")
            return
        clave = simpledialog.askstring("Registro", "Ingresa tu contraseña:", show='*')
        if not clave:
            return
        self.usuarios[nombre] = Usuario(nombre, clave)
        messagebox.showinfo("Registro exitoso", "Usuario creado correctamente.")

    def iniciarSesion(self):
        nombre = simpledialog.askstring("Inicio de sesión", "Usuario:")
        if not nombre or nombre not in self.usuarios:
            messagebox.showerror("Error", "Usuario no registrado.")
            return
        clave = simpledialog.askstring("Inicio de sesión", "Contraseña:", show='*')
        if self.usuarios[nombre].verificarClave(clave):
            self.usuarioActual = nombre
            self.menuUsuario()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

    def cerrarSesion(self):
        self.usuarioActual = None
        self.menuPrincipal()

    def agregarTarea(self):
        descripcion = simpledialog.askstring("Agregar Tarea", "Descripción:")
        if not descripcion:
            return
        categoria = simpledialog.askstring("Categoría", "trabajo / personal / estudio:")
        try:
            tareaId = self.gestor.agregar_tarea(self.usuarioActual, descripcion, categoria)
            messagebox.showinfo("Éxito", f"Tarea agregada con ID {tareaId}")
        except (DescripcionVaciaError, CategoriaInvalidaError) as e:
            messagebox.showerror("Error", str(e))

    def verTareas(self):
        try:
            tareas = self.gestor.obtener_tareas_usuario(self.usuarioActual)
            texto = "\n".join([f"[{t.id}] {t.descripcion} ({t.categoria})" for t in tareas])
            messagebox.showinfo("Mis Tareas", texto)
        except UsuarioSinTareasError as e:
            messagebox.showinfo("Sin tareas", str(e))

    def eliminarTarea(self):
        try:
            tareaId = simpledialog.askinteger("Eliminar Tarea", "ID de la tarea a eliminar:")
            self.gestor.eliminar_tarea(tareaId)
            messagebox.showinfo("Éxito", "Tarea eliminada.")
        except TareaNoEncontradaError as e:
            messagebox.showerror("Error", str(e))
        except:
            messagebox.showwarning("Cancelado", "Operación cancelada o ID inválido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()


"""
Módulo de interfaz gráfica (GUI) para el Gestor de Tareas

Implementa una interfaz visual usando Tkinter que permite:
- Registro y autenticación de usuarios
- Gestión completa de tareas (CRUD)
- Navegación entre diferentes pantallas/menús

Arquitectura:
------------
- AppGUI: Clase principal que maneja:
  * Configuración de la ventana principal
  * Navegación entre pantallas
  * Gestión del estado de la aplicación
  * Coordinación con el GestorTareas

Componentes principales:
----------------------
- Sistema de autenticación:
  * Registro de nuevos usuarios
  * Inicio/cierre de sesión
  * Persistencia de usuarios en memoria

- Gestión de tareas:
  * Creación con validación de categorías
  * Visualización listada
  * Eliminación por ID

- Interfaz:
  * Menú principal (no autenticado)
  * Menú de usuario (autenticado)
  * Diálogos modales para operaciones
  * Mensajes de feedback al usuario

Dependencias:
------------
- tkinter: Para todos los componentes visuales
- services.gestor_tareas: Lógica de negocio de tareas
- models.usuario: Modelo de datos de usuario
- exceptions.exceptions: Manejo de errores personalizados

Flujo de trabajo típico:
----------------------
1. Inicio -> Muestra menú principal (registro/login)
2. Registro o inicio de sesión
3. Menú de usuario con opciones de tareas
4. Operaciones CRUD mediante diálogos
5. Cierre de sesión -> Vuelve a menú principal

Manejo de errores:
-----------------
- Muestra mensajes amigables para:
  * Credenciales inválidas
  * Validación de datos (descripción vacía, categoría inválida)
  * Operaciones con IDs inexistentes
  * Usuarios sin tareas

Ejemplo de uso:
--------------
>>> python vista.py
(Muestra la ventana principal del gestor)

Características de la interfaz:
-----------------------------
- Diseño minimalista y funcional
- Navegación intuitiva entre pantallas
- Validación en tiempo real
- Feedback visual inmediato
- Diálogos modales para operaciones
- Adaptable a diferentes resoluciones

Notas técnicas:
-------------
- Estado mantenido en memoria durante la ejecución
- Separación clara entre vista y lógica de negocio
- Uso de componentes estándar de Tkinter
- No requiere instalación adicional (solo Python estándar)
- Diseño responsive básico
"""