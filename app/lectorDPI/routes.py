#Librerias
from flask import Blueprint, jsonify, request, send_file, redirect, url_for
from app.common.scripts import inicializandoConexion
from app.lectorDPI.scripts import extract_info_DPI
from app.lectorDPI.scripts import crop_photo
from app.lectorDPI.scripts import resize_selfie
import json, os


# Crear un Blueprint para las rutas relacionadas con los usuarios
lectorDPI = Blueprint('lectorDPI', __name__)


#Ruta principal
@lectorDPI.route('/')
def index():
    msg = inicializandoConexion()
    return jsonify({'msg': msg})


# http://localhost:5000/api/lectorDPI/extrain_info?image_path=media/chavi.jpeg
@lectorDPI.route('/extrain_info', methods=['GET'])
def extrain_info():
    
    # image_path = request.args.get('image_path')  
    # print('Imagen Name: ', image_path)
    # STORAGE_ROUTE_BD = os.environ['STORAGE_ROUTE_BD']  #path for images from the database
    
    # image_path = f"{STORAGE_ROUTE_BD}{image_path}"
    image_path = '/home/jaime/Documents/university/infoProcessingAPI/media/chavi.png'
    results = extract_info_DPI(image_path)
    results = results.replace('\n', ' ')

    return jsonify({'resultExtrain': results})

