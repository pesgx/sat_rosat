from sat_rosat.database import Database
from sat_rosat.models.cliente_model import Cliente

class ClienteController:
    def crear_cliente(self, cliente_data):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tabla_clientes (
                        codigo_cliente, nombre_cliente, nombre_cliente_comercial, 
                        nif_cliente, domicilio, poblacion_id, telefono_1, telefono_2, nota_cliente
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_cliente
                """, (
                    cliente_data['codigo_cliente'], cliente_data['nombre_cliente'],
                    cliente_data['nombre_cliente_comercial'], cliente_data['nif_cliente'],
                    cliente_data['domicilio'], cliente_data['poblacion_id'],
                    cliente_data['telefono_1'], cliente_data['telefono_2'],
                    cliente_data['nota_cliente']
                ))
                return cur.fetchone()[0]

    def actualizar_cliente(self, cliente_data):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE tabla_clientes
                    SET codigo_cliente = %s, nombre_cliente = %s, nombre_cliente_comercial = %s,
                        nif_cliente = %s, domicilio = %s, poblacion_id = %s,
                        telefono_1 = %s, telefono_2 = %s, nota_cliente = %s
                    WHERE id_cliente = %s
                """, (
                    cliente_data['codigo_cliente'], cliente_data['nombre_cliente'],
                    cliente_data['nombre_cliente_comercial'], cliente_data['nif_cliente'],
                    cliente_data['domicilio'], cliente_data['poblacion_id'],
                    cliente_data['telefono_1'], cliente_data['telefono_2'],
                    cliente_data['nota_cliente'], cliente_data['id_cliente']
                ))

    def eliminar_cliente(self, id_cliente):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tabla_clientes WHERE id_cliente = %s", (id_cliente,))

    def obtener_todos_clientes(self):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.*, p.nombre_poblacion
                    FROM tabla_clientes c
                    JOIN tabla_poblacion p ON c.poblacion_id = p.id_poblacion
                    ORDER BY c.id_cliente DESC
                """)
                return [self._crear_objeto_cliente(row) for row in cur.fetchall()]

    def obtener_cliente_por_id(self, id_cliente):
        with Database.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.*, p.nombre_poblacion
                    FROM tabla_clientes c
                    JOIN tabla_poblacion p ON c.poblacion_id = p.id_poblacion
                    WHERE c.id_cliente = %s
                """, (id_cliente,))
                row = cur.fetchone()
                return self._crear_objeto_cliente(row) if row else None

    def _crear_objeto_cliente(self, row):
        return Cliente(
            id_cliente=row[0],
            codigo_cliente=row[1],
            nombre_cliente=row[2],
            nombre_cliente_comercial=row[3],
            nif_cliente=row[4],
            domicilio=row[5],
            poblacion_id=row[6],
            telefono_1=row[7],
            telefono_2=row[8],
            nota_cliente=row[9],
            nombre_poblacion=row[10]
        )