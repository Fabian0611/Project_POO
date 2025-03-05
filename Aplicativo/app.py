from flask import Flask
from controllers.controller import HomeController , PropietarioController, VehiculoController, ParqueaderoController


app = Flask(__name__)

# Inicializar controladores
HomeController(app)
PropietarioController(app)
VehiculoController(app)
ParqueaderoController(app)

if __name__ == '__main__':
    app.run(debug=True)
