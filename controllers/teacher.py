import bcrypt
import smtplib
from helpers.timestap import date_timestamp
from helpers.random import numbers_random
from repositories.repositories_server import repositories_

class teachers_controller():
    def __init__(self, base_datos):
        self.db =base_datos
        self.repository = repositories_(self.db)

    def register_teacher(self, data):
        password = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        )
        date = date_timestamp.date(data['date_birth'])
        code = numbers_random.number()
        current_date = date_timestamp.current_date()

        
        r = self.repository.save(
            '''nombre, apellidos, email, fecha_nacimiento, descripcion,
            telefono, contrasenia, estado, Fecha''',
            '%s, %s, %s, %s, %s, %s, %s, %s, %s',
            '_maestros_',
            (data['name'], 
             data['last_name'], 
             data['email'],
             date,
             data['description'],
             data['phone'],
             password,
             2,
             current_date)
        )

       
        print("Resultado de la inserción: ", r)

        user = self.repository.consult_update(
                '''
                SELECT idx FROM _maestros_
                WHERE email = %s
                ''',
                (data['email'],)
            )

        print("Resultado de la consulta: ", user)
      

        if isinstance(r, dict) and r.get('Errors'):
            print(r['Errors'])
            self.db.rollback()
            if 'email_unico' in r['Errors']:
                return {'Message': 'El email ya está registrado', 'num': 400}
            else:
                return {'Message': 'Error inesperado en el servidor', 'num': 500}
        
        if isinstance(user, dict) and user.get('Errors'):
            print(user['Errors'])
            self.db.rollback()
            return {'Message': 'Error inesperado en el servidor', 'num': 500}
        
        if(user[0]):
             id_r = user[0][0]
             r = self.repository.save(
                '''ID_Registro, codigo, tipo''',
                '%s, %s, %s',
                '_codigos_',
                (id_r, code, 1)
            )

        self.send_mail( data['email'], code)
        return {'Message': 'Maestro registrado correctamente', 'num': 200}

    def send_mail(self, email, code):
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender = 'lopezkaren43567@gmail.com'
        password = 'suvo pzzk kmma msbb'

        # Datos del destinatario
        addressee = email

        # Crear el Message
        menssage = MIMEMultipart()
        menssage['From'] = sender
        menssage['To'] = addressee
        menssage['Subject'] = 'Verificación de registro'

        # Tu código como texto
        code = f"""
            El codigo de verificación es: 
            {code}
        """

        menssage.attach(MIMEText(code, 'plain'))

        # Enviar correo por SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(sender, password)
            servidor.send_message(menssage)
        print("Correo enviado con éxito.")

    def validate_code_register(self, data, id_register):
        # Verificar si esxiste el id del registro
        print(f'DATA  {data}')
        code = data['code']
        current_date = date_timestamp.current_date()
        id_register_verify = self.repository.consult_update(
            '''
                SELECT json_build_object(
                'id', idx
                ) 
                as maestros FROM _maestros_ m
                INNER JOIN _codigos_ on m.idx = _codigos_.id_registro
                and _codigos_.codigo = %s
                WHERE idx = %s 
                AND m.fecha - %s > 600

            ''',
            (
                code,
                id_register,
                current_date
            )
        )

        print('Consulta registro ' , (id_register_verify))
        if(len(id_register_verify) > 0):
            # Actualizar el estado del registro a 1 (verificado)    
            r = self.repository.consult_update(
                '''
                UPDATE _maestros_
                SET estado = %s
                WHERE idx= %s
                AND estado = 2
                ''',
                (1, id_register)
            )
            
            if isinstance(r, dict) and r.get('Errors'):
                print(r['Errors'])
                self.db.rollback()
                return {'Message': 'Error inesperado en el servidor', 'num': 500}
            else:
                print("Registro verificado correctamente")
                return {'Message': 'Código de registro verificado', 'num': 200}
            # return {'Message': 'Código de registro verificado', 'num': 200}
        else:
            return {'Message': 'El código ingresado no es válido o ha expirado. Por favor, verifica e intenta nuevamente.', 'num': 404}        