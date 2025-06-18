# main.py
from config.ConectionDB import DatabaseConnection  # Importar la clase
from router.router import router_maestro

# Usar la clase importada
db = DatabaseConnection()
db.connect()

router_ = router_maestro()

app = router_.app
print(__name__ , 'NAME ')
if __name__ == '__main__':
    app.run(debug=True)