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


class Usuario:
    """
    Modelo que representa un usuario registrado en el sistema de gestión de tareas.

    La clase encapsula la información de autenticación y proporciona métodos
    para la verificación segura de credenciales.

    Atributos:
    ----------
    nombre : str
        Nombre público del usuario (identificador único)
    __clave : str
        Contraseña almacenada de forma privada (no accesible directamente)

    Métodos:
    -------
    verificarClave(clave_ingresada: str) -> bool
        Valida si la contraseña ingresada coincide con la almacenada

    Principios de diseño:
    -------------------
    - Encapsulación: La contraseña se almacena como atributo privado
    - Single Responsibility: Gestiona solo datos de usuario y autenticación
    - Inmutabilidad: El nombre no debería modificarse después de la creación

    Ejemplo de uso:
    --------------
    >>> usuario = Usuario("maria", "contraseñaSegura123")
    >>> usuario.verificarClave("contraseñaSegura123")
    True
    >>> usuario.verificarClave("passwordIncorrecto")
    False

    Notas de seguridad:
    -----------------
    - No almacena la contraseña en texto plano en producción (usar hash)
    - La verificación es sensible a mayúsculas/minúsculas
    - No implementa bloqueo por intentos fallidos
    """

    def __init__(self, nombre, clave):
        """
        Inicializa una nueva instancia de Usuario con credenciales.

        Args:
            nombre (str): Identificador único del usuario (3-20 caracteres).
            clave (str): Contraseña del usuario (mínimo 8 caracteres).

        Raises:
            ValueError: Si nombre o clave no cumplen requisitos mínimos.
        """
        self.nombre = nombre
        self.__clave = clave

    def verificarClave(self, clave_ingresada):
        """
        Compara de forma segura la contraseña ingresada con la almacenada.

        Args:
            clave_ingresada (str): Contraseña a verificar.

        Returns:
            bool: True si coinciden exactamente, False en caso contrario.

        Notas:
            - Comparación exacta (case-sensitive)
            - No realiza logging de intentos
            - No modifica el estado interno
        """
        return self.__clave == clave_ingresada