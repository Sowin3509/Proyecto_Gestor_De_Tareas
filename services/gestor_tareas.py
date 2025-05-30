import psycopg2
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import sys

# Excepciones personalizadas
class DescripcionVaciaError(Exception): pass
class CategoriaInvalidaError(Exception): pass
class TareaNoEncontradaError(Exception): pass
class UsuarioSinTareasError(Exception): pass
class EstadoInvalidoError(Exception): pass

class GestorTareas:
    CATEGORIAS_VALIDAS = {"trabajo", "personal", "estudio"}
    ESTADOS_VALIDOS = {"Pendiente", "Completada", "Sin realizar"}

    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        self.db_config = db_config
        self.usa_postgresql = db_config is not None
        self.conn = None
        self.tareas: Dict[int, Dict[str, Any]] = {}
        self.contador_id = 1
        self._configurar_logging()
        self._inicializar_base_datos()

    def _configurar_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gestor_tareas.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _inicializar_base_datos(self):
        if not self.usa_postgresql:
            self.logger.info("Modo memoria activado (sin PostgreSQL)")
            return
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = False
            self._crear_estructura_bd()
            self.logger.info("Conexión exitosa a PostgreSQL")
        except Exception as e:
            self.logger.error(f"Error al conectar a PostgreSQL: {e}")
            self.usa_postgresql = False
            self.logger.warning("Se usará modo memoria")
            if self.conn:
                self.conn.close()
                self.conn = None

    def _crear_estructura_bd(self):
        scripts = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL DEFAULT '',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                descripcion TEXT NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
                    CHECK (estado IN ('Pendiente', 'Completada', 'Sin realizar'))
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_tareas_usuario ON tareas(usuario_id)
            """
        ]
        try:
            with self.conn.cursor() as cur:
                for script in scripts:
                    cur.execute(script)
                self.conn.commit()
            self.logger.info("Estructura de BD creada correctamente")
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Error al crear estructura de BD: {e}")
            raise RuntimeError(f"No se pudieron crear las tablas: {e}")

    def _obtener_id_usuario(self, username: str) -> int:
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
                usuario = cur.fetchone()
                if usuario:
                    return usuario[0]
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash) VALUES (%s, '') RETURNING id",
                    (username,)
                )
                nuevo_id = cur.fetchone()[0]
                self.conn.commit()
                return nuevo_id
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"No se pudo obtener o crear usuario '{username}': {e}")

    def tarea_pertenece_a_usuario(self, tarea_id: int, username: str) -> bool:
        try:
            tarea = self.obtener_tarea(tarea_id)
            if not tarea:
                return False
            if self.usa_postgresql and self.conn:
                usuario_id = self._obtener_id_usuario(username)
                return tarea.get('usuario_id') == usuario_id
            else:
                return tarea.get('usuario') == username
        except Exception as e:
            self.logger.error(f"Error al verificar pertenencia de tarea {tarea_id}: {e}")
            return False

    def agregar_tarea(self, usuario: str, descripcion: str, categoria: str) -> int:
        try:
            usuario = usuario.strip()
            descripcion = descripcion.strip()
            categoria = categoria.lower().strip()

            if not usuario:
                raise ValueError("Usuario vacío")
            if not descripcion:
                raise DescripcionVaciaError("Descripción vacía")
            if categoria not in self.CATEGORIAS_VALIDAS:
                raise CategoriaInvalidaError(f"Categoría inválida: '{categoria}'")

            if self.usa_postgresql and self.conn:
                usuario_id = self._obtener_id_usuario(usuario)
                with self.conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO tareas (usuario_id, descripcion, categoria, estado)
                        VALUES (%s, %s, %s, 'Pendiente') RETURNING id""",
                        (usuario_id, descripcion, categoria)
                    )
                    tarea_id = cur.fetchone()[0]
                    self.conn.commit()
                    self.logger.info(f"Tarea agregada en PostgreSQL con ID {tarea_id}")
                    return tarea_id
            else:
                tarea_id = self.contador_id
                self.tareas[tarea_id] = {
                    'id': tarea_id,
                    'usuario': usuario,
                    'descripcion': descripcion,
                    'categoria': categoria,
                    'fecha_creacion': datetime.now(),
                    'estado': 'Pendiente'
                }
                self.contador_id += 1
                self.logger.info(f"Tarea agregada en memoria con ID {tarea_id}")
                return tarea_id
        except Exception as e:
            if self.usa_postgresql and self.conn:
                self.conn.rollback()
            raise RuntimeError(f"Error al agregar tarea: {e}")
    
    def obtener_tarea(self, tarea_id: int) -> Dict[str, Any]:
        try:
            if self.usa_postgresql and self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT t.id, t.usuario_id, t.descripcion, t.categoria,
                                  t.fecha_creacion, t.estado
                           FROM tareas t
                           WHERE t.id = %s""",
                        (tarea_id,)
                    )
                    tarea = cur.fetchone()
                    if not tarea:
                        raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                    return {
                        'id': tarea[0],
                        'usuario_id': tarea[1],
                        'descripcion': tarea[2],
                        'categoria': tarea[3],
                        'fecha_creacion': tarea[4],
                        'estado': tarea[5]
                    }
            else:
                if tarea_id not in self.tareas:
                    raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                return self.tareas[tarea_id]
        except Exception as e:
            raise RuntimeError(f"Error al obtener tarea {tarea_id}: {e}")

    def eliminar_tarea(self, tarea_id: int):
        try:
            if self.usa_postgresql and self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
                    if cur.rowcount == 0:
                        raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                    self.conn.commit()
                    self.logger.info(f"Tarea {tarea_id} eliminada de PostgreSQL")
            else:
                if tarea_id not in self.tareas:
                    raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                del self.tareas[tarea_id]
                self.logger.info(f"Tarea {tarea_id} eliminada de memoria")
        except Exception as e:
            if self.usa_postgresql and self.conn:
                self.conn.rollback()
            raise RuntimeError(f"Error al eliminar tarea {tarea_id}: {e}")

    def obtener_tareas_usuario(self, usuario: str) -> List[Dict[str, Any]]:
        try:
            usuario = usuario.strip()
            if self.usa_postgresql and self.conn:
                usuario_id = self._obtener_id_usuario(usuario)
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT t.id, t.usuario_id, t.descripcion, t.categoria,
                                  t.fecha_creacion, t.estado
                           FROM tareas t
                           WHERE t.usuario_id = %s
                           ORDER BY t.fecha_creacion DESC""",
                        (usuario_id,)
                    )
                    tareas_data = cur.fetchall()
                    if not tareas_data:
                        raise UsuarioSinTareasError(f"El usuario '{usuario}' no tiene tareas")
                    return [
                        {
                            'id': row[0],
                            'usuario_id': row[1],
                            'descripcion': row[2],
                            'categoria': row[3],
                            'fecha_creacion': row[4],
                            'estado': row[5],
                            'usuario': usuario
                        } for row in tareas_data
                    ]
            else:
                tareas_usuario = [t for t in self.tareas.values() if t['usuario'] == usuario]
                if not tareas_usuario:
                    raise UsuarioSinTareasError(f"El usuario '{usuario}' no tiene tareas")
                return tareas_usuario
        except Exception as e:
            raise RuntimeError(f"Error al obtener tareas del usuario '{usuario}': {e}")

    def cambiar_estado_tarea(self, tarea_id: int, nuevo_estado: str):
        try:
            nuevo_estado = nuevo_estado.strip().capitalize()
            if nuevo_estado not in self.ESTADOS_VALIDOS:
                raise EstadoInvalidoError(f"Estado inválido: '{nuevo_estado}'")

            if self.usa_postgresql and self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "UPDATE tareas SET estado = %s WHERE id = %s",
                        (nuevo_estado, tarea_id)
                    )
                    if cur.rowcount == 0:
                        raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                    self.conn.commit()
                    self.logger.info(f"Estado de tarea {tarea_id} cambiado a '{nuevo_estado}'")
            else:
                if tarea_id not in self.tareas:
                    raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                self.tareas[tarea_id]['estado'] = nuevo_estado
                self.logger.info(f"Estado de tarea {tarea_id} cambiado a '{nuevo_estado}' en memoria")
        except Exception as e:
            if self.usa_postgresql and self.conn:
                self.conn.rollback()
            raise RuntimeError(f"Error al cambiar estado de tarea {tarea_id}: {e}")

    def editar_tarea(self, tarea_id: int, nueva_descripcion: str, nueva_categoria: str):
        try:
            nueva_descripcion = nueva_descripcion.strip()
            nueva_categoria = nueva_categoria.strip().lower()

            if not nueva_descripcion:
                raise DescripcionVaciaError("Descripción vacía")
            if nueva_categoria not in self.CATEGORIAS_VALIDAS:
                raise CategoriaInvalidaError(f"Categoría inválida: '{nueva_categoria}'")

            if self.usa_postgresql and self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "UPDATE tareas SET descripcion = %s, categoria = %s WHERE id = %s",
                        (nueva_descripcion, nueva_categoria, tarea_id)
                    )
                    if cur.rowcount == 0:
                        raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                    self.conn.commit()
                    self.logger.info(f"Tarea {tarea_id} actualizada en PostgreSQL")
            else:
                if tarea_id not in self.tareas:
                    raise TareaNoEncontradaError(f"No existe tarea con ID {tarea_id}")
                self.tareas[tarea_id]['descripcion'] = nueva_descripcion
                self.tareas[tarea_id]['categoria'] = nueva_categoria
                self.logger.info(f"Tarea {tarea_id} actualizada en memoria")
        except Exception as e:
            if self.usa_postgresql and self.conn:
                self.conn.rollback()
            raise RuntimeError(f"Error al editar tarea {tarea_id}: {e}")

    def __del__(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Conexión PostgreSQL cerrada")
