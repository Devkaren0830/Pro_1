import re
from marshmallow import Schema, fields, ValidationError

class additional_validations:
    
    @staticmethod
    def validator_password(password):
        if (len(password) <= 8):
            raise ValidationError('La contraseña debe ser igual o superar los 8 caracteres.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra minuscula.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un número.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')

        return password  
    
    @staticmethod
    def validar_codigo(codigo):
        try:
            if len(codigo) > 5:
                raise ValidationError('El codigo es incorrecto')

            cod = int(codigo)
            return codigo
        except ValidationError:
            raise ValidationError('El codigo es incorrecto')


# 1. Definir el esquema como clase
class TeacherSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    apellidos = fields.String(required=True)
    telefono = fields.Integer(required=True)
    descripcion = fields.String(required=True)
    fecha_nacimiento = fields.Date(required=True)
    password = fields.String(
        required=True,
        validate=additional_validations.validator_password
    )

class ValidarCodigoRegistro(Schema):
    codigo = fields.String(
        required=True, 
        validate=additional_validations.validar_codigo    
    )

class validator_teacher:
    # 2. Función que usa el esquema para validar
    @staticmethod 
    def validate_teacher(data):
        try:
            schema = TeacherSchema()
            r = schema.load(data)
            return {'message': 'Docente validado', 'data': r}
        except ValidationError as e:
            return {'errors': e.messages}
    
    @staticmethod
    def validar_codigo_registro(data):
        try: 
            schema = ValidarCodigoRegistro()
            r = schema.load(data)
            return {'message': 'Código de registro validado', 'data': r}
        except ValidationError as e:
            return {'errors': e.messages}