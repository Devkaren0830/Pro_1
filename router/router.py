from flask import request, jsonify
from validator.validator_shema import validator_teacher
from marshmallow import ValidationError
from controllers.teacher import teachers_controller

class router_maestro:
 
    def __init__(self, db, app):
        self.conn = db
        self.app = app
        self.teacher = teachers_controller(self.conn)
        self.validator = validator_teacher()

           # Registrar rutas manualmente
        app.add_url_rule('/', view_func=self.home)
        app.add_url_rule(
            '/register_teacher', methods=['POST'], 
            view_func=self.register_teacher
        )
        app.add_url_rule(
            '/verify_code_register/<id_register>',
            methods=['POST'],
            view_func=self.verify_master_registration_code
        )
        app.add_url_rule(
            '/saludo',
            view_func=self.saludo
        )

    def home(self):
        return  jsonify({'Message': "Servidor funcionando correctamente"})

    
    def register_teacher(self):
        try:
            data = request.get_json()
            validar_maestro = self.validator.validate_teacher(data)
            print(f"validar_maestro: {validar_maestro}")
            if 'errors' in validar_maestro:
                return jsonify(validar_maestro['errors']), 500
            print(validar_maestro)
            master =  self.teacher.register_teacher(data)
            return jsonify(master['Message']), master['num']
        except ValidationError:
            return jsonify({'Message': 'Error de validación de datos'}), 400
        
    def verify_master_registration_code(self, id_register):
        try:
            data = request.get_json()
            validate_code = self.validator.validate_registration_code(data)
            if 'errors' in validate_code:
                return jsonify(validate_code['errors']), 500
            
            validate_code = self.teacher.validate_code_register(
                data,
                id_register
            )

            return jsonify({'Message': validate_code['Message']}), validate_code['num'] 
        except ValidationError:
            return jsonify({'Message': 'Error de validación de datos'}), 400
        
    def saludo():
        return 'HOLA cocomo estas'        
    
    