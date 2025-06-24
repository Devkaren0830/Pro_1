import bcrypt
import smtplib
from helpers.timestap import fecha_timestamp
from helpers.random import numeros
from repositories.repositorios_server import repositorios_

class maestros():
    def __init__(self, base_datos):
        self.db =base_datos

    def register_maestro(self, data):
        contrasenia = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        )
        fecha = fecha_timestamp.fecha(data['fecha_nacimiento'])
        codigo = numeros.numero()

        repos = repositorios_(self.db)
        r = repos.guardar(
            '''nombre, apellidos, email, fecha_nacimiento, descripcion,
            telefono, contrasenia, estado''',
            '%s, %s, %s, %s, %s, %s, %s, %s',
            '_maestros_',
            (data['name'], 
             data['apellidos'], 
             data['email'],
             fecha,
             data['descripcion'],
             data['telefono'],
             contrasenia,
             2)
        )

       
        print("Resultado de la inserción: ", r)

        usuario = repos.consultar(
                '''
                SELECT idx FROM _maestros_
                WHERE email = %s
                ''',
                (data['email'],)
            )

        print("Resultado de la consulta: ", usuario)
      

        if isinstance(r, dict) and r.get('Errors'):
            print(r['Errors'])
            self.db.rollback()
            if 'email_unico' in r['Errors']:
                return {'Mensaje': 'El email ya está registrado', 'num': 400}
            else:
                return {'Mensaje': 'Error inesperado en el servidor', 'num': 500}
        
        if isinstance(usuario, dict) and usuario.get('Errors'):
            print(usuario['Errors'])
            self.db.rollback()
            return {'Mensaje': 'Error inesperado en el servidor', 'num': 500}
        
        if(usuario[0]):
             id_r = usuario[0][0]
             r = repos.guardar(
                '''ID_Registro, codigo, tipo''',
                '%s, %s, %s',
                '_codigos_',
                (id_r, codigo, 1)
            )

        self.enviar_correo( data['email'], codigo)
        return {'Mensaje': 'Maestro registrado correctamente', 'num': 200}

    def enviar_correo(self, email, codigo):
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Datos del remitente
        remitente = 'lopezkaren43567@gmail.com'
        contraseña = 'suvo pzzk kmma msbb'

        # Datos del destinatario
        destinatario = email

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = 'Verificación de registro'

        # Tu código como texto
        codigo = f"""
            El codigo de verificación es: 
            {codigo}
        """

        mensaje.attach(MIMEText(codigo, 'plain'))

        # Enviar correo por SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        print("Correo enviado con éxito.")
