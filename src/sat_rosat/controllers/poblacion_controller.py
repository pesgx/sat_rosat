from sat_rosat.models.poblacion_model import PoblacionModel
from sat_rosat.database import Database

class PoblacionController:
    @staticmethod
    def crear_poblacion(nombre_poblacion, codigo_postal):
        return PoblacionModel.crear(nombre_poblacion, codigo_postal)

    @staticmethod
    def obtener_todas_poblaciones():
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_poblacion, nombre_poblacion FROM tabla_poblacion ORDER BY nombre_poblacion")
                return cur.fetchall()
    @staticmethod
    def obtener_todas_poblaciones_en_poblaciones():
        return PoblacionModel.obtener_todos()

    @staticmethod
    def obtener_poblacion(id_poblacion):
        return PoblacionModel.obtener_por_id(id_poblacion)

    @staticmethod
    def actualizar_poblacion(id_poblacion, nombre_poblacion, codigo_postal):
        return PoblacionModel.actualizar(id_poblacion, nombre_poblacion, codigo_postal)

    @staticmethod
    def eliminar_poblacion(id_poblacion):
        return PoblacionModel.eliminar(id_poblacion)