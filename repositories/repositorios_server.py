class repositorios_:
    def __init__(self, db):
        self.db = db

    def guardar(self, column_tabla, parametros, tabla, data):
        query = f'''
            INSERT INTO {tabla}
            ({column_tabla})
            VALUES ({parametros})
        '''
        r = self.db.execute_query(query, 
                data
            )

        return r
    
    def consultar(self, consulta, data):
         r = self.db.execute_query(
             consulta,
             data
         )
         return r
    


