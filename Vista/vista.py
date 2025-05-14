import sys
import os
import logging
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from services.gestor_tareas import GestorTareas
from exceptions.exceptions import (
    DescripcionVaciaError, CategoriaInvalidaError,
    TareaNoEncontradaError, UsuarioSinTareasError
)
from models.usuario import Usuario

class AppGUI:
    def __init__(self, root, gestor=None):
        self.root = root
        self.root.title("Gestor de Tareas - GUI")
        self.gestor = gestor 
        self.db_config = {
            "dbname": "gestor_tareas_2025",
            "user": "postgres",
            "password": "isabela23AA",
            "host": "localhost",
            "port": "5433",
            "client_encoding": "UTF-8"
        }

        try:
            if not self.gestor:
                self.gestor = GestorTareas(self.db_config)
                logging.info("Conexión a PostgreSQL establecida")
        except Exception as e:
            logging.error(f"Error al conectar a PostgreSQL: {e}")
            messagebox.showwarning(
                "Modo Local", 
                "No se pudo conectar a la base de datos. Trabajando en modo local."
            )
            self.gestor = GestorTareas()
            
        self.usuarios = {}  
        self.usuarioActual = None
        self.tarea_seleccionada = None
        self.configurar_logging()
        self.menuPrincipal()

    def configurar_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='gestor_tareas.log',
            encoding='utf-8'
        )

    def limpiarVentana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menuPrincipal(self):
        self.limpiarVentana()
        tk.Label(self.root, text="Gestor de Tareas", font=("Arial", 16)).pack(pady=10)

        botones = [
            ("Crear Cuenta", self.crearCuenta),
            ("Iniciar Sesión", self.iniciarSesion),
            ("Salir", self.root.quit)
        ]

        for texto, comando in botones:
            tk.Button(
                self.root, 
                text=texto, 
                command=comando, 
                width=30
            ).pack(pady=5)

    def menuUsuario(self):
        self.limpiarVentana()
        tk.Label(
            self.root, 
            text=f"Bienvenido, {self.usuarioActual}", 
            font=("Arial", 14)
        ).pack(pady=10)

        opciones = [
            ("Agregar Tarea", self.agregarTarea),
            ("Ver Mis Tareas", self.verTareas),
            ("Eliminar Tarea", self.eliminarTarea),
            ("Cambiar Estado de Tarea", self.mostrar_ventana_cambiar_estado),
            ("Cerrar Sesión", self.cerrarSesion)
        ]

        for texto, comando in opciones:
            tk.Button(
                self.root, 
                text=texto, 
                command=comando, 
                width=30
            ).pack(pady=5)

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
        logging.info(f"Nuevo usuario registrado: {nombre}")

    def iniciarSesion(self):
        nombre = simpledialog.askstring("Inicio de sesión", "Usuario:")
        if not nombre or nombre not in self.usuarios:
            messagebox.showerror("Error", "Usuario no registrado.")
            return
            
        clave = simpledialog.askstring("Inicio de sesión", "Contraseña:", show='*')
        if self.usuarios[nombre].verificarClave(clave):
            self.usuarioActual = nombre
            logging.info(f"Usuario autenticado: {nombre}")
            self.menuUsuario()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            logging.warning(f"Intento de inicio fallido para: {nombre}")

    def cerrarSesion(self):
        logging.info(f"Usuario cerró sesión: {self.usuarioActual}")
        self.usuarioActual = None
        self.menuPrincipal()

    def agregarTarea(self):
        if not self.usuarioActual:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return
            
        descripcion = simpledialog.askstring("Agregar Tarea", "Descripción:")
        if not descripcion:
            return
            
        categoria = simpledialog.askstring("Categoría", "trabajo/personal/estudio:").lower()
        if not categoria or categoria not in ["trabajo", "personal", "estudio"]:
            messagebox.showerror("Error", "Categoría inválida. Use: trabajo, personal o estudio")
            return
            
        try:
            tareaId = self.gestor.agregar_tarea(self.usuarioActual, descripcion, categoria)
            messagebox.showinfo("Éxito", f"Tarea guardada (ID: {tareaId})")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

    def verTareas(self):
        if not self.usuarioActual:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return
            
        try:
            tareas = self.gestor.obtener_tareas_usuario(self.usuarioActual)
            
            ventana_tareas = tk.Toplevel(self.root)
            ventana_tareas.title("Mis Tareas")
            
            tk.Label(ventana_tareas, 
                    text=f"Tareas de {self.usuarioActual}",
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            frame = tk.Frame(ventana_tareas)
            frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(
                frame,
                yscrollcommand=scrollbar.set,
                width=80,
                height=15,
                font=("Arial", 10)
            )
            
            if not tareas:
                listbox.insert(tk.END, "No hay tareas registradas")
            else:
                for tarea in tareas:
                    estado = tarea.get('estado', 'Pendiente')
                    fecha = tarea['fecha_creacion'].strftime("%d/%m/%Y %H:%M") if isinstance(tarea['fecha_creacion'], datetime) else tarea['fecha_creacion']
                    listbox.insert(tk.END, 
                                f"ID: {tarea['id']} | {fecha} | {tarea['descripcion'][:30]}... | Cat: {tarea['categoria']} | Estado: {estado}")
            
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)
            
        except UsuarioSinTareasError:
            messagebox.showinfo("Info", "No hay tareas registradas")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las tareas: {str(e)}")
            logging.error(f"Error al cargar tareas: {str(e)}")

    def eliminarTarea(self):
        if not self.usuarioActual:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return
            
        try:
            tarea_id = simpledialog.askinteger("Eliminar Tarea", "ID de la tarea a eliminar:")
            if tarea_id is None:
                return
                
            if not self.gestor.tarea_pertenece_a_usuario(tarea_id, self.usuarioActual):
                raise TareaNoEncontradaError("Tarea no encontrada o no pertenece al usuario")
                
            tarea = self.gestor.obtener_tarea(tarea_id)
            confirmacion = messagebox.askyesno(
                "Confirmar", 
                f"¿Eliminar esta tarea?\n\nID: {tarea_id}\nDescripción: {tarea['descripcion']}\nCategoría: {tarea['categoria']}"
            )
            
            if confirmacion:
                self.gestor.eliminar_tarea(tarea_id)
                messagebox.showinfo("Éxito", "Tarea eliminada correctamente")
                logging.info(f"Tarea eliminada - ID: {tarea_id} por {self.usuarioActual}")
            
        except TareaNoEncontradaError as e:
            messagebox.showerror("Error", str(e))
            logging.warning(f"Error al eliminar: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            logging.error(f"Error al eliminar tarea: {str(e)}")

    def mostrar_ventana_cambiar_estado(self):
        if not self.usuarioActual:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return

        ventana_estado = tk.Toplevel(self.root)
        ventana_estado.title("Cambiar Estado de Tarea")
        ventana_estado.geometry("400x300")

        tk.Label(ventana_estado, 
                text="Seleccione una tarea y su nuevo estado",
                font=("Arial", 12)).pack(pady=10)

        # Frame para la lista de tareas
        frame_tareas = tk.Frame(ventana_estado)
        frame_tareas.pack(pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_tareas)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_tareas = tk.Listbox(
            frame_tareas,
            yscrollcommand=scrollbar.set,
            width=50,
            height=8,
            font=("Arial", 10)
        )
        self.lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_tareas.yview)

        # Cargar tareas
        try:
            tareas = self.gestor.obtener_tareas_usuario(self.usuarioActual)
            if not tareas:
                self.lista_tareas.insert(tk.END, "No hay tareas registradas")
            else:
                for tarea in tareas:
                    estado = tarea.get('estado', 'Pendiente')
                    self.lista_tareas.insert(
                        tk.END, 
                        f"ID: {tarea['id']} - {tarea['descripcion'][:30]}... ({estado})"
                    )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar tareas: {str(e)}")

        # Frame para el selector de estado
        frame_estado = tk.Frame(ventana_estado)
        frame_estado.pack(pady=10)

        tk.Label(frame_estado, text="Nuevo estado:").pack(side=tk.LEFT)

        self.combo_estado = ttk.Combobox(
            frame_estado,
            values=["Pendiente", "Completada", "Sin realizar"],
            state="readonly"
        )
        self.combo_estado.pack(side=tk.LEFT, padx=5)
        self.combo_estado.set("Pendiente")

        # Botón para aplicar cambios
        btn_actualizar = tk.Button(
            ventana_estado,
            text="Actualizar Estado",
            command=self.actualizar_estado_tarea
        )
        btn_actualizar.pack(pady=10)

    def actualizar_estado_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una tarea primero")
            return

        tarea_texto = self.lista_tareas.get(seleccion[0])
        tarea_id = int(tarea_texto.split("ID: ")[1].split(" -")[0])
        nuevo_estado = self.combo_estado.get()

        try:
            if not self.gestor.tarea_pertenece_a_usuario(tarea_id, self.usuarioActual):
                raise TareaNoEncontradaError("Tarea no encontrada o no pertenece al usuario")

            self.gestor.cambiar_estado(tarea_id, nuevo_estado)
            messagebox.showinfo("Éxito", f"Estado actualizado a: {nuevo_estado}")
            self.lista_tareas.delete(seleccion[0])
            self.lista_tareas.insert(
                seleccion[0],
                f"ID: {tarea_id} - {tarea_texto.split(' - ')[1].split(' (')[0]}... ({nuevo_estado})"
            )
            self.lista_tareas.selection_set(seleccion[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = AppGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Error crítico en la aplicación: {str(e)}")
        messagebox.showerror(
            "Error Fatal", 
            "Ha ocurrido un error crítico. Ver logs para detalles."
        )
        root.destroy()
"""
Interfaz Gráfica Actualizada para Gestor de Tareas con PostgreSQL

Mejoras realizadas:
------------------
1. Conexión robusta a PostgreSQL con verificación de estructura
2. Mensajes claros indicando dónde se guardan los datos (PostgreSQL o local)
3. Interfaz mejorada para visualización de tareas con scroll
4. Validación de usuario logueado antes de operaciones
5. Protección contra eliminación de tareas de otros usuarios
6. Logging detallado de todas las operaciones

Cambios principales:
------------------
- Sistema de conexión a BD más robusto
- Verificación de pertenencia de tareas al usuario
- Ventana especial para visualización de tareas
- Mensajes más informativos para el usuario
- Manejo de errores más completo

Requisitos para la base de datos:
-------------------------------
1. PostgreSQL corriendo en puerto 5433
2. Base de datos 'gestor_tareas_2025' creada
3. Usuario 'postgres' con permisos adecuados
4. Estructura de tablas correcta (se crea automáticamente)

Notas importantes:
----------------
- Los usuarios siguen gestionándose en memoria por simplicidad
- Las tareas se guardan en PostgreSQL cuando hay conexión
- El modo memoria es solo para emergencias (sin conexión)
- Todos los eventos importantes se registran en gestor_tareas.log
"""