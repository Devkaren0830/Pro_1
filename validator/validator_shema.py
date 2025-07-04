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
    def validate_code(code):
        try:
            if len(code) > 5:
                raise ValidationError('El codigo es incorrecto')

            cod = int(code)
            return code
        except ValidationError:
            raise ValidationError('El codigo es incorrecto')


# 1. Definir el esquema como clase
class TeacherSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    last_name = fields.String(required=True)
    phone = fields.Integer(required=True)
    description = fields.String(required=True)
    date_birth = fields.Date(required=True)
    password = fields.String(
        required=True,
        validate=additional_validations.validator_password
    )

class ValidateCodeRegister(Schema):
    code = fields.String(
        required=True, 
        validate=additional_validations.validate_code    
    )

class ValidateLoginTeacher(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True
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
    def validate_registration_code(data):
        try: 
            schema = ValidateCodeRegister()
            r = schema.load(data)
            return {'message': 'Código de registro validado', 'data': r}
        except ValidationError as e:
            return {'errors': e.messages}
    
    @staticmethod
    def validate_teacher_login(data):
        try:
            schema = ValidateLoginTeacher()
            r = schema.load(data)
            return {'message': 'Docente validado', 'data': r}
        except ValidationError as e:
            return {'errors': e.messages}