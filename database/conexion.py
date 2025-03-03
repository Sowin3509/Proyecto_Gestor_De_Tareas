import sqlite3

class ConexionDB:
    def __init__(self, db_name="gestor_tareas.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tablas()

    def _crear_tablas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                texto TEXT,
                categoria TEXT,
                estado TEXT,
                FOREIGN KEY(usuario) REFERENCES usuarios(username)
            )
        ''')
        self.conn.commit()

    def cerrar(self):
        self.conn.close()
