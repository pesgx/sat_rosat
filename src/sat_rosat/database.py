import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

# Cargar variables de entorno
load_dotenv()

class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls):
        cls.__connection_pool = pool.SimpleConnectionPool(
            1,  # Mínimo de conexiones
            20,  # Máximo de conexiones
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'bd_rosat'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', 5432)
        )

    @classmethod
    def get_connection(cls):
        if cls.__connection_pool is None:
            cls.initialize()
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls.__connection_pool is not None:
            cls.__connection_pool.closeall()

def execute_query(query, params=None):
    conn = Database.get_connection()
    try:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if query.strip().upper().startswith('SELECT'):               
                return cur.fetchall()

            else:
                conn.commit()
    finally:
        Database.return_connection(conn)

def execute_many(query, params):
    conn = Database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(query, params)
            conn.commit()
    finally:
        Database.return_connection(conn)