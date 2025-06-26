from flask import request, jsonify
from validator.validator_shema import validator_teacher
from marshmallow import ValidationError
from controllers.maestro import maestros

class router_maestro:
 
    def __init__(self, db, app):
        self.conn = db
        self.app = app
        self.maestro = maestros(self.conn)
        self.validator = validator_teacher()

           # Registrar rutas manualmente
        app.add_url_rule('/', view_func=self.home)
        app.add_url_rule(
            '/register_teacher', methods=['POST'], 
            view_func=self.register_teacher
        )
        app.add_url_rule(
            '/verificar_codigo_registro/<id_registro>',
            methods=['POST'],
            view_func=self.verificar_codigo_registro_maestro
        )
        app.add_url_rule(
            '/saludo',
            view_func=self.saludo
        )

    def home(self):
        return  jsonify({'Mensaje': "Servidor funcionando correctamente"})

    
    def register_teacher(self):
        try:
            data = request.get_json()
            validar_maestro = self.validator.validate_teacher(data)
            print(f"validar_maestro: {validar_maestro}")
            if 'errors' in validar_maestro:
                return jsonify(validar_maestro['errors']), 500
            print(validar_maestro)
            maestro =  self.maestro.register_maestro(data)
            return jsonify(maestro['Mensaje']), maestro['num']
        except ValidationError:
            return jsonify({'Mensaje': 'Error de validación de datos'}), 400
        
    def verificar_codigo_registro_maestro(self, id_registro):
        try:
            data = request.get_json()
            validar_codigo = self.validator.validar_codigo_registro(data)
            if 'errors' in validar_codigo:
                return jsonify(validar_codigo['errors']), 500
            
            validar_codigo = self.maestro.validar_codigo_registro(
                data,
                id_registro
            )

            return jsonify({'Mensaje': 'HOLA'}), 200 
        except ValidationError:
            return jsonify({'Mensaje': 'Error de validación de datos'}), 400
        
    def saludo():
        return 'HOLA cocomo estas'        
    
    