
import psycopg2

class ClienteModel:
    def __init__(self):
        self.conexion = psycopg2.connect(
            host="localhost",
            database="bd_rosat",
            user="postgres",
            password="pescacom_2"
        )

    def obtener_todos(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cliente, c.codigo_cliente, c.nombre_cliente, c.nif_cliente, 
                p.nombre_poblacion, c.telefono_1 AS telefono
                FROM tabla_clientes c
                LEFT JOIN tabla_poblacion p ON c.poblacion_id = p.id_poblacion
            """)
            return [
                {
                    "id_cliente": row[0],
                    "codigo_cliente": row[1],
                    "nombre_cliente": row[2],
                    "nif_cliente": row[3],
                    "nombre_poblacion": row[4],
                    "telefono": row[5],
                }
                for row in cursor.fetchall()
            ]

    def obtener_poblaciones(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_poblacion, nombre_poblacion FROM tabla_poblacion")
            return [
                {"id_poblacion": row[0], "nombre_poblacion": row[1]} for row in cursor.fetchall()
            ]

    def insertar_cliente(self, codigo, nombre, nif, poblacion_id, telefono, nota):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tabla_clientes (codigo_cliente, nombre_cliente, nif_cliente, poblacion_id, telefono_1, nota_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, nif, poblacion_id, telefono, nota))
            self.conexion.commit()
