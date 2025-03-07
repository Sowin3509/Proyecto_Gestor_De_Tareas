import sqlite3
from database.conexion import ConexionDB
from models.tarea import Tarea

class GestorTareas:
    def __init__(self, db_path="tareas.db"):
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()

    def limpiar_tareas(self):
        """Elimina todas las tareas de la base de datos"""
        self.cursor.execute("DELETE FROM tareas")  # Borra todas las tareas
        self.conexion.commit()


class GestorTareas:
    def __init__(self):
        self.db = ConexionDB()  # Crear una instancia de ConexionDB
        self.usuarios = []  # Inicializar la lista de usuarios
        self.tareas = []    # Inicializar la lista de tareas

    def registrar_usuario(self, usuario, contraseña):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        try:
            cursor.execute("""
                INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)
            """, (usuario, contraseña))
            self.db.conexion.commit()  # Guardar los cambios en la base de datos
            return True  # Usuario registrado con éxito
        except sqlite3.IntegrityError:
            return False  # El usuario ya existe

    def autenticar_usuario(self, usuario, contraseña):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        cursor.execute("""
            SELECT id FROM usuarios WHERE usuario = ? AND contraseña = ?
        """, (usuario, contraseña))
        resultado = cursor.fetchone()
        return resultado is not None  # True si el usuario y la contraseña son correctos

    def cambiar_contraseña(self, usuario, contraseña_actual, nueva_contraseña):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        
        # Verificar que el usuario y la contraseña actual sean correctos
        cursor.execute("""
            SELECT id FROM usuarios WHERE usuario = ? AND contraseña = ?
        """, (usuario, contraseña_actual))
        
        resultado = cursor.fetchone()
        
        if resultado:
            # Actualizar la contraseña en la base de datos
            cursor.execute("""
                UPDATE usuarios SET contraseña = ? WHERE usuario = ?
            """, (nueva_contraseña, usuario))
            self.db.conexion.commit()  # Guardar los cambios en la base de datos
            return True  # Contraseña cambiada con éxito
        else:
            return False  # Usuario o contraseña actual incorrectos

    def agregar_tarea(self, tarea):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        cursor.execute("""
            INSERT INTO tareas (usuario, texto, categoria, estado)
            VALUES (?, ?, ?, ?)
        """, (tarea.usuario, tarea.texto, tarea.categoria, tarea.estado))
        self.db.conexion.commit()  # Guardar los cambios en la base de datos

    def obtener_tareas(self, usuario):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        cursor.execute("""
            SELECT id, usuario, texto, categoria, estado FROM tareas WHERE usuario = ?
        """, (usuario,))
        return cursor.fetchall()

        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        cursor.execute("""
            UPDATE tareas SET estado = ? WHERE id = ?
        """, (nuevo_estado, id_tarea))
        self.db.conexion.commit()  # Guardar los cambios en la base de datos

    def eliminar_tarea(self, id_tarea):
        cursor = self.db.cursor  # Acceder al cursor de la base de datos
        cursor.execute("""
            DELETE FROM tareas WHERE id = ?
        """, (id_tarea,))
        self.db.conexion.commit()  # Guardar los cambios en la base de datos

    def __del__(self):
        self.db.cerrar()  # Cerrar la conexión a la base de datos

    def obtener_todas_las_tareas(self):
        return self.tareas  # Asumiendo que `tareas` es la lista donde se almacenan
