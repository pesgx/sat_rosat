from sat_rosat.database import execute_query

class PoblacionModel:
    @staticmethod
    def crear(nombre_poblacion, codigo_postal):
        query = "INSERT INTO tabla_poblacion (nombre_poblacion, codigo_postal) VALUES (%s, %s) RETURNING id_poblacion"
        result = execute_query(query, (nombre_poblacion, codigo_postal))
        return result[0][0] if result else None

    @staticmethod
    def obtener_todos():
        query = "SELECT * FROM tabla_poblacion ORDER BY id_poblacion DESC"
        return execute_query(query)

    @staticmethod
    def obtener_por_id(id_poblacion):
        query = "SELECT * FROM tabla_poblacion WHERE id_poblacion = %s"
        result = execute_query(query, (id_poblacion,))
        return result[0] if result else None

    @staticmethod
    def actualizar(id_poblacion, nombre_poblacion, codigo_postal):
        query = "UPDATE tabla_poblacion SET nombre_poblacion = %s, codigo_postal = %s WHERE id_poblacion = %s"
        return execute_query(query, (nombre_poblacion, codigo_postal, id_poblacion))

    @staticmethod
    def eliminar(id_poblacion):
        query = "DELETE FROM tabla_poblacion WHERE id_poblacion = %s"
        return execute_query(query, (id_poblacion,))