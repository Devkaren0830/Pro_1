import bcrypt
from config.ConectionDB import DatabaseConnection  # Importar la clase

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
        r = db.execute_query(query, (
                data['name'], 
                data['apellidos'], 
                data['email'],
                data['fecha_nacimiento'],
                data['descripcion'],
                data['telefono'],
                contrasenia
            )
        )

        print(r)
        return "Maestro registrado"