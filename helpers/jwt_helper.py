from dotenv import load_dotenv
import os
class jwt_helper:
    def __init__(self):
        load_dotenv() # Cargar las variables de entorno desde el archivo .env
        self.SECRET_KET = os.getenv('SECRET_KEY')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    
    def get_token(self, data):
        print(f"Datos para generar el token: {data}")