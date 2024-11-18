from sat_rosat.database import Database
from sat_rosat.models.grupo_model import Grupo

class GrupoController:
    @staticmethod
    def crear_grupo(nombre_grupo: str) -> int:
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tabla_grupos (nombre_grupo) VALUES (%s) RETURNING id_grupo",
                    (nombre_grupo,)
                )
                return cur.fetchone()[0]  # Accedemos al primer elemento de la tupla

    @staticmethod
    def obtener_todos_grupos():
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tabla_grupos ORDER BY nombre_grupo")
                return [Grupo(id_grupo=row[0], nombre_grupo=row[1]) for row in cur.fetchall()]

    @staticmethod
    def actualizar_grupo(id_grupo: int, nombre_grupo: str):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tabla_grupos SET nombre_grupo = %s WHERE id_grupo = %s",
                    (nombre_grupo, id_grupo)
                )

    @staticmethod
    def eliminar_grupo(id_grupo: int):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tabla_grupos WHERE id_grupo = %s", (id_grupo,))