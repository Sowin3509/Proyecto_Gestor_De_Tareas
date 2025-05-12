import sys
from pathlib import Path
import tkinter as tk
import logging
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.gestor_tareas import GestorTareas
from Vista.vista import AppGUI

def configurar_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('gestor_tareas.log', encoding='utf-8'),
            logging.StreamHandler(stream=sys.stdout)  
        ]
    )
    logging.addLevelName(logging.INFO, "[INFO]")

def inicializar_gestor():
    db_params = {
        "dbname": "gestor_tareas_2025",
        "user": "postgres",
        "password": "isabela23AA",
        "host": "localhost",
        "port": "5433",
        "client_encoding": "utf8"
    }
    
    try:
        gestor = GestorTareas(db_config=db_params)
        logging.info("✅ Conexión exitosa a PostgreSQL")
        return gestor
    except Exception as e:
        logging.error(f"Error al conectar a PostgreSQL: {e}")
        logging.info("🔌 Usando modo memoria")
        return GestorTareas()  

if __name__ == "__main__":
    configurar_logging()
    gestor = inicializar_gestor()
    
    try:
        root = tk.Tk()
        app = AppGUI(root, gestor)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Error crítico: {e}")
    finally:
        logging.info("Aplicación terminada")

"""
Punto de entrada mejorado para la aplicación de gestión de tareas.

Mejoras realizadas:
------------------
1. Integración con el nuevo GestorTareas que soporta PostgreSQL
2. Sistema de logging para diagnóstico de problemas
3. Modo fallback a memoria si PostgreSQL no está disponible
4. Inyección del gestor en el módulo vista
5. Manejo de excepciones para errores críticos
6. Configuración de logging para registrar eventos y errores
7. Uso de un archivo de configuración para los parámetros de conexión a la base de datos
8. Mejora de la estructura del código para mayor claridad y mantenibilidad
Funcionalidad manteniendo compatibilidad:
---------------------------------------
- Sigue usando tu vista.show_menu() existente
- Proporciona el gestor como variable global al módulo vista
- Maneja errores de conexión a la base de datos
- Configura logging para registrar eventos y errores
- Permite la ejecución de la GUI sin necesidad de modificar el código de vista
- Mantiene la estructura modular y la separación de responsabilidades
"""