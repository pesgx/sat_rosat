from sat_rosat.database import Database
from sat_rosat.models.marca_model import Marca

class MarcaController:
    @staticmethod
    def crear_marca(nombre_marca: str, grupo_id: int) -> int:
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tabla_marcas (nombre_marca, grupo_id) VALUES (%s, %s) RETURNING id_marca",
                    (nombre_marca, grupo_id)
                )
                return cur.fetchone()[0]

    @staticmethod
    def obtener_todas_marcas():
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT m.id_marca, m.nombre_marca, m.grupo_id, g.nombre_grupo 
                    FROM tabla_marcas m 
                    JOIN tabla_grupos g ON m.grupo_id = g.id_grupo 
                    ORDER BY m.nombre_marca
                """)
                return [Marca(id_marca=row[0], nombre_marca=row[1], grupo_id=row[2], nombre_grupo=row[3]) for row in cur.fetchall()]

    @staticmethod
    def actualizar_marca(id_marca: int, nombre_marca: str, grupo_id: int):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tabla_marcas SET nombre_marca = %s, grupo_id = %s WHERE id_marca = %s",
                    (nombre_marca, grupo_id, id_marca)
                )

    @staticmethod
    def eliminar_marca(id_marca: int):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tabla_marcas WHERE id_marca = %s", (id_marca,))

    @staticmethod
    def obtener_todos_grupos():
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_grupo, nombre_grupo FROM tabla_grupos ORDER BY nombre_grupo")
                return cur.fetchall()