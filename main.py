#Importacion de librerias
from flask import Flask, jsonify, request

#Importacion de rutas
from app.lectorDPI.routes import lectorDPI

#Instanciando el objeto para nuestra app
app = Flask(__name__)

#Definicion de rutas
app.register_blueprint(lectorDPI, url_prefix='/api/lectorDPI/')


#Ruta inicial
@app.route('/', methods=['GET'])
def index():
    return 'Hola mundo'


#Inicializar la API
if __name__=='__main__':
    app.run(debug=True)
