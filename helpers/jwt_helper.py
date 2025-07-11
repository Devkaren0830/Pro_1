from dotenv import load_dotenv
import os
import jwt
class jwt_helper:
    def __init__(self):
        load_dotenv() # Cargar las variables de entorno desde el archivo .env
        self.SECRET_KET = os.getenv('SECRET_KEY')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
        self.payload = {}

    def set_payload(self, data):
        """Establece el payload del token JWT."""
        self.payload = data
    
    def get_token(self, data):
        print(f"Datos para generar el token: {data}") 
        """Genera un token JWT a partir del payload."""
        token = jwt.encode(self.payload, self.SECRET_KET, self.JWT_ALGORITHM)
        print(f"Token generado: {token}")
        return {'Message': "Token generado correctamente", "token": token}
    
    def verificar_token(self, token):
        # Verificar token
        try: 
            decode_token = jwt.decode(token, self.SECRET_KET, self.JWT_ALGORITHM)
            return {'Message': 'Token verificado correctamente', 'data': decode_token}
        except jwt.ExpiredSignatureError:
            return {'Errors': 'El token ha expirado'}
        except jwt.InvalidTokenError:
            return {'Errors': 'Token inválido'}