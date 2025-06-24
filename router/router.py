from flask import request, jsonify
from validator.validator_shema import validator_teacher
from marshmallow import ValidationError
from controllers.maestro import maestros

class router_maestro:
 
    def __init__(self, db, app):
        self.conn = db
        self.app = app
        self.maestro = maestros(self.conn)

           # Registrar rutas manualmente
        app.add_url_rule('/', view_func=self.home)
        app.add_url_rule(
            '/register_teacher', methods=['POST'], 
            view_func=self.register_teacher
        )
        app.add_url_rule('/saludo', view_func=self.saludo)
    
    def home():
        return  jsonify({'Mensaje': "Servidor funcionando correctamente"})

    
    def register_teacher(self):
        try:
            data = request.get_json()
            validator = validator_teacher()
            validar_maestro = validator.validate_teacher(data)
            print(f"validar_maestro: {validar_maestro}")
            if 'errors' in validar_maestro:
                return jsonify(validar_maestro['errors']), 500
            print(validar_maestro)
            maestro =  self.maestro.register_maestro(data)
            return jsonify(maestro['Mensaje']), maestro['num']
        except ValidationError:
            return jsonify({'Mensaje': 'Error de validación de datos'}), 400
        
    def saludo():
        return 'HOLA cocomo estas'        
    
    