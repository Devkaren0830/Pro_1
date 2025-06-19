from flask import request, jsonify
from validator.validator_shema import validator_teacher
from marshmallow import ValidationError
from controllers.maestro import maestros
maestro = maestros()

class router_maestro:
 
    def __init__(self, db, app):
        self.conn = db
        self.app = app
        self.maestro = maestros()

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
            print(validar_maestro)
            self.maestro.register_maestro(data, self.conn)
            return jsonify(validar_maestro, 500)
        except ValidationError:
            return jsonify({'error': ValidationError})
        
    def saludo():
        return 'HOLA cocomo estas'        
    
    