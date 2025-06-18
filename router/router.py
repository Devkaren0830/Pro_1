from flask import Flask, request, jsonify
from validator.validator_shema import validator_teacher
from marshmallow import ValidationError

class router_maestro:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return  jsonify({'Mensaje': "Servidor funcionando correctamente"})

    @app.route('/register_teacher', methods=['POST'])
    def register_teache():
        try:
            
            
            data = request.get_json()
            
            validator = validator_teacher()
            validar_maestro = validator.validate_teacher(data)
            print(validar_maestro)
            return jsonify(validar_maestro, 500)
        except ValidationError:
            return jsonify({'error': ValidationError})
        
    @app.route('/saludo')
    def saludo():
        return 'HOLA cocomo estas'        
    
    