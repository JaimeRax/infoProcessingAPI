#Librerias
from flask import Blueprint, jsonify, request               

#Scripts
from app.facialRecognition.scripts import facial_compare    
from app.common.scripts import inicializandoConexion
import os 

# Crear un Blueprint para las rutas relacionadas con los usuarios
facialRecognition = Blueprint('facialRecognition', __name__)

#Ruta principal
@facialRecognition.route('/')
def index():
    msg = inicializandoConexion()
    return jsonify({'msg': msg})


# http://localhost:5000/facial_recognition/compare?first_image=media/imagen1.png&second_image=media/imagen2.jpg
@facialRecognition.route('/compare', methods=['GET'])
def facial_recognition():
    first_image = request.args.get('first_image')
    second_image = request.args.get('second_image')
    
    # #Obtiendo la ruta completa
    # STORAGE_ROUTE = os.environ['STORAGE_ROUTE']       
    # first_image = f"{STORAGE_ROUTE}{first_image}"
    # second_image = f"{STORAGE_ROUTE}{second_image}"
    
    msg = facial_compare(first_image, second_image)
    
    return jsonify({'resultCompare': msg})
