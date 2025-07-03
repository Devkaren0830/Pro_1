from repositories.repositories_server import repositories_
import smtplib

class teacher_student_function():
    def __init__(self, base_datos):
        self.db =base_datos
        self.repository = repositories_(self.db)
    
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