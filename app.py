# main.py
from config.ConectionDB import DatabaseConnection  # Importar la clase
from router.router import router_maestro
from flask import Flask
# jhdsfdjhkgfd

# Usar la clase importada
db = DatabaseConnection()
db.connect()
db.rollback()
app = Flask(__name__)
router_maestro(db, app );
print('HOLA')
print(__name__ , 'NAME ')
if __name__ == '__main__':
    app.run(debug=True)