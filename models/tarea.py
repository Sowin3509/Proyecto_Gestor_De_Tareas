class Tarea:
    def __init__(self, id_tarea, usuario, descripcion, categoria):
        self.id = id_tarea
        self.usuario = usuario
        self.descripcion = descripcion
        self.categoria = categoria

        
class Tarea:
    """
    Clase que representa una tarea dentro del sistema.

    Atributos:
        id (int): Identificador único de la tarea.
        usuario (str): Nombre del usuario al que pertenece la tarea.
        descripcion (str): Descripción detallada de la tarea.
        categoria (str): Categoría de la tarea (trabajo, personal, estudio).

    Métodos:
        __str__(): Representación en texto de la tarea.
    """

    def __init__(self, id, usuario, descripcion, categoria):
        """
        Inicializa una nueva instancia de Tarea.

        Args:
            id (int): ID único de la tarea.
            usuario (str): Usuario al que pertenece la tarea.
            descripcion (str): Descripción de la tarea.
            categoria (str): Categoría de la tarea.
        """
        self.id = id
        self.usuario = usuario
        self.descripcion = descripcion
        self.categoria = categoria

    def __str__(self):
        """
        Devuelve una representación en cadena de la tarea.

        Returns:
            str: Representación formateada de la tarea.
        """
        return f"[{self.id}] {self.descripcion} - {self.categoria} (Usuario: {self.usuario})"


"""
Modelo que representa una tarea en el sistema de gestión.

La clase Tarea encapsula todos los atributos y comportamientos fundamentales
de una tarea dentro del sistema, siguiendo el principio de responsabilidad única.

Atributos:
---------
id : int
    Identificador único numérico de la tarea (inmutable)
usuario : str
    Nombre del usuario propietario de la tarea (requerido)
descripcion : str
    Contenido textual que describe la tarea (requerido)
categoria : str
    Clasificación de la tarea entre valores predefinidos:
    - 'trabajo'
    - 'personal' 
    - 'estudio'

Métodos:
-------
__init__(id, usuario, descripcion, categoria)
    Constructor que inicializa todos los atributos requeridos
__str__()
    Representación legible para humanos de la instancia

Ejemplo de uso:
--------------
>>> tarea = Tarea(1, "juan", "Revisar documentación", "trabajo")
>>> print(tarea)
[1] Revisar documentación - trabajo (Usuario: juan)

Validaciones implícitas:
----------------------
- Todos los parámetros son requeridos
- No se realizan validaciones de formato en el constructor
- La consistencia de datos es responsabilidad del GestorTareas

Notas de diseño:
--------------
- Modelo de datos simple e inmutable (atributos públicos)
- No contiene lógica de negocio
- Fácilmente serializable para persistencia
- __str__() diseñado para logging e interfaz de usuario básica

Relaciones:
----------
- Agregada por GestorTareas
- Referenciada por Usuario
- Independiente del mecanismo de almacenamiento
"""