class Tarea:
    def __init__(self, id_tarea, usuario, texto, categoria, estado="Por hacer"):
        self.id_tarea = id_tarea
        self.usuario = usuario
        self.texto = texto
        self.categoria = categoria
        self.estado = estado
