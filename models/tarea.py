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
