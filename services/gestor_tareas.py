from database.conexion import ConexionDB
from models.tarea import Tarea

class GestorTareas:
    def __init__(self):
        self.db = ConexionDB()

    def agregar_tarea(self, tarea):
        self.db.cursor.execute(
            "INSERT INTO tareas (usuario, texto, categoria, estado) VALUES (?, ?, ?, ?)",
            (tarea.usuario, tarea.texto, tarea.categoria, tarea.estado),
        )
        self.db.conn.commit()

    def obtener_tareas(self, usuario):
        self.db.cursor.execute("SELECT * FROM tareas WHERE usuario = ?", (usuario,))
        return self.db.cursor.fetchall()

    def actualizar_tarea(self, id_tarea, nuevo_estado):
        self.db.cursor.execute(
            "UPDATE tareas SET estado = ? WHERE id = ?", (nuevo_estado, id_tarea)
        )
        self.db.conn.commit()

    def eliminar_tarea(self, id_tarea):
        self.db.cursor.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
        self.db.conn.commit()
