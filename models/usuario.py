class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

    """
    Clase que representa un usuario del sistema.
    """

    def __init__(self, nombre, clave):
        """
        Inicializa un usuario con nombre y contraseña privada.

        Args:
            nombre (str): Nombre del usuario.
            clave (str): Contraseña del usuario (se almacena de forma privada).
        """
        self.nombre = nombre
        self.__clave = clave

    def verificarClave(self, clave_ingresada):
        """
        Verifica si la clave ingresada coincide con la del usuario.

        Args:
            clave_ingresada (str): Contraseña escrita por el usuario.

        Returns:
            bool: True si coincide, False si no.
        """
        return self.__clave == clave_ingresada
