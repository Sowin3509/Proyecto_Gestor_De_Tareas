# database.py
import sys
from pathlib import Path
import psycopg2
from psycopg2 import OperationalError

# Configuración de paths para imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

from Proyecto_De_Aula_Gestor_De_Tareas_2025.database.database_config import DB_CONFIG

def __init__(self, db_config=None):
    self.connection = None
    self.db_config = db_config or DB_CONFIG
    
    # Validación de configuración completa
    required_keys = ['dbname', 'user', 'password', 'host', 'port']
    for key in required_keys:
        if key not in self.db_config:
            raise ValueError(f"Configuración incompleta: falta '{key}'")

class Database:
    def __init__(self, db_config=None):
        self.connection = None
        self.db_config = db_config or DB_CONFIG
        
        if not self.db_config.get('password'):
            raise ValueError("La configuración debe incluir 'password'")
            
    def connect(self):
        try:
            print("ℹ️ Intentando conexión con estos parámetros:")
            print(f"- Host: {self.db_config['host']}")
            print(f"- Puerto: {self.db_config['port']}")
            print(f"- Usuario: {self.db_config['user']}")
            print(f"- Base de datos: {self.db_config['dbname']}")
            
            self.connection = psycopg2.connect(
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            print(f"✅ Conexión exitosa a PostgreSQL en puerto {self.db_config['port']}")
            return self.connection
        except OperationalError as e:
            print("❌ Error de conexión a PostgreSQL:")
            print(f"Detalle técnico: {str(e)}")
            print("\nPasos para solucionar:")
            print("1. Verifica que PostgreSQL esté corriendo")
            print("2. Confirma usuario/contraseña en pgAdmin")
            print("3. Revisa el archivo pg_hba.conf")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {type(e).__name__}: {str(e)}")
            return None
    
    def close(self):
        """Cierra la conexión si está abierta"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    # Prueba de conexión al ejecutar directamente
    db = Database()
    conn = db.connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            print("Versión PostgreSQL:", cursor.fetchone()[0])
        finally:
            db.close()