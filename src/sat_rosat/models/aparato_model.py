from sat_rosat.database import execute_query

class AparatoModel:
    @staticmethod
    def crear(nombre_aparato):
        query = "INSERT INTO tabla_aparatos (nombre_aparato) VALUES (%s) RETURNING id_aparato"
        result = execute_query(query, (nombre_aparato,))
        return result[0][0] if result else None

    @staticmethod
    def obtener_todos():
        query = "SELECT * FROM tabla_aparatos ORDER BY id_aparato DESC"
        return execute_query(query)

    @staticmethod
    def obtener_por_id(id_aparato):
        query = "SELECT * FROM tabla_aparatos WHERE id_aparato = %s"
        result = execute_query(query, (id_aparato,))
        return result[0] if result else None

    @staticmethod
    def actualizar(id_aparato, nombre_aparato):
        query = "UPDATE tabla_aparatos SET nombre_aparato = %s WHERE id_aparato = %s"
        return execute_query(query, (nombre_aparato, id_aparato))

    @staticmethod
    def eliminar(id_aparato):
        query = "DELETE FROM tabla_aparatos WHERE id_aparato = %s"
        return execute_query(query, (id_aparato,))