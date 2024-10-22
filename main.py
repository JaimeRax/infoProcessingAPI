#Importacion de librerias
from flask import Flask, jsonify
from app.lectorDPI.routes import lectorDPI
from app.common.login import login_bp
from flask_cors import CORS

#Instanciando el objeto para nuestra app
app = Flask(__name__)
CORS(app)

#Definicion de rutas
app.register_blueprint(lectorDPI, url_prefix='/api/lectorDPI/')
app.register_blueprint(login_bp, url_prefix='/api/login/')  

#Ruta inicial
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Hola mundo'
        })

#Inicializar la API
if __name__=='__main__':
    app.run(debug=True, port=5001)
