import sqlite3

class ConexionDB:
    def __init__(self):
        self.conexion = sqlite3.connect("gestor_tareas.db")  # Conectar a la base de datos
        self.cursor = self.conexion.cursor()  # Crear un cursor
        self._crear_tablas()  # Crear las tablas si no existen

    def _crear_tablas(self):
        # Crear la tabla de usuarios si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contraseña TEXT NOT NULL
            )
        """)
        # Crear la tabla de tareas si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                texto TEXT NOT NULL,
                categoria TEXT,
                estado TEXT
            )
        """)
        self.conexion.commit()  # Guardar los cambios

    def cerrar(self):
        self.conexion.close()  # Cerrar la conexión a la base de datos