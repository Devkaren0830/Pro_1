import bcrypt
from config.ConectionDB import DatabaseConnection  # Importar la clase
from datetime import datetime
import smtplib

class maestros():
    def register_maestro(self, data, db):
        # nombre = self.request.form('nombre')
        # apellidos = self.request.form('apellidos')
        # email = self.request.form('email')
        # telefono = self.request.form('telefono')
        # especialidad = self.request.form('especialidad')
        # fecha_nacimiento = self.request.form('fecha_nacimiento')
        # nombre = self.request.form('nombre')
        print(data)
        query = '''
            INSERT INTO _maestros_
            (nombre, apellidos, email, fecha_nacimiento, descripcion,
            telefono, contrasenia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        print(query)
        contrasenia = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        )

        fecha_2 = self.fecha(data['fecha_nacimiento'])
        anio = fecha_2['anio']       # '2003'
        mes = fecha_2['mes']         # '08'
        dia = fecha_2['dia']         # '30'
        print("Año:", anio)
        print("Mes:", mes)
        print("Día:", dia)
        fecha_2 = datetime(int(anio), int(mes), int(dia))
        fecha_timestamp = int(fecha_2.timestamp())

        print(f"FECHA {fecha_timestamp}")
        print("Valor que se insertará en fecha_nacimiento:", fecha_timestamp, type(fecha_timestamp))

        r = db.execute_query(query, (
            data['name'], 
            data['apellidos'], 
            data['email'],
            fecha_timestamp,
            data['descripcion'],
            data['telefono'],
            contrasenia
        ))
        print("Resultado de la inserción: ", r)

        if isinstance(r, dict) and r.get('Errors'):
            print(r['Errors'])
            db.rollback()
            if 'email_unico' in r['Errors']:
                return {'Mensaje': 'El email ya está registrado', 'num': 400}
            else:
                return {'Mensaje': 'Error inesperado en el servidor', 'num': 500}
        else:
            self.enviar_correo()
            return {'Mensaje': 'Maestro registrado correctamente', 'num': 200}

    

    def fecha(self, fecha):
        fecha = fecha.split('-')
        fechas = {
            'anio': fecha[0],
            'mes': fecha[1],
            'dia': fecha[2]
        }
        return fechas

    def enviar_correo(self):
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Datos del remitente
        remitente = 'lopezkaren43567@gmail.com'
        contraseña = 'suvo pzzk kmma msbb'

        # Datos del destinatario
        destinatario = 'bermudezlopezpedrojose@gmail.com'

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = 'Código en Python'

        # Tu código como texto
        codigo = """
        FEOOO
        """

        mensaje.attach(MIMEText(codigo, 'plain'))

        # Enviar correo por SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        print("Correo enviado con éxito.")
