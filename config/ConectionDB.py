import psycopg2
from psycopg2 import OperationalError, DatabaseError
from dotenv import load_dotenv
import os

class DatabaseConnection:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env

        # Obtener las variables de conexión de las variables de entorno
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")

        # Inicializar la conexión y el cursor
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establecer una conexión con la base de datos."""
        try:
            # Intentamos conectarnos a la base de datos
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            print("Usuario conectado:", self.db_user)
            print("database conectada:", self.db_name)

            self.cursor = self.conn.cursor()
            print("Conexión exitosa a la base de datos.")
        except OperationalError as e:
            print(f"Error de conexión: {e}")
        except DatabaseError as e:
            print(f"Error de base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def execute_query(self, query:str, params=None):
        """Ejecutar una consulta SQL."""
        try:
            if self.cursor:
                self.cursor.execute(query, params)
                # Si es una consulta SELECT, devolvemos los resultados
                if query.strip().lower().startswith("select"):
                    return self.cursor.fetchall()
                else:
                    self.conn.commit()  # Para consultas que modifican la base de datos
            else:
                print("No hay una conexión activa.")
        except OperationalError as e:
            print(f"Error de ejecución de consulta: {e}")
        except Exception as e:
            return {'Errors': str(e)}

    def close(self):
        """Cerrar la conexión y el cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Conexión cerrada correctamente.")

    def rollback(self):
        """Revertir la transacción actual si hay un error."""
        if self.conn:
            self.conn.rollback()
            print("Transacción revertida (rollback ejecutado).")




