import psycopg2
from psycopg2 import pool
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'colegio'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '123456'),
}

# Crear el pool de conexiones
class DBPool:
    def __init__(self, minconn, maxconn):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn,  # Número mínimo de conexiones
            maxconn,  # Número máximo de conexiones
            **DB_CONFIG
        )

    def get_conn(self):
        # Obtener una conexión del pool
        return self.pool.getconn()

    def put_conn(self, conn):
        # Devolver la conexión al pool
        self.pool.putconn(conn)

    def close_all(self):
        # Cerrar todas las conexiones en el pool
        self.pool.closeall()

# Crear una instancia del pool con un mínimo de 1 conexión y un máximo de 10 conexiones
db_pool = DBPool(minconn=1, maxconn=10)

