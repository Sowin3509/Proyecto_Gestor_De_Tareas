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
