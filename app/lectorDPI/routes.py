#Librerias
from flask import Blueprint, jsonify, request, send_file, redirect, url_for
from app.common.scripts import inicializandoConexion
from app.lectorDPI.scripts import extract_info_DPI
from app.lectorDPI.scripts import crop_photo
from app.lectorDPI.scripts import resize_selfie
from app.facialRecognition.scripts import facial_compare
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

# lectorDPI/compares?image_path=(relative route)&selfie_path(relative route)
# http://localhost:5000/api/lectorDPI/compares?image_path=media/dpi1.jpeg&selfie_path=media/selfie4.jpeg
@lectorDPI.route('/compares', methods=['GET'])
def compare():
    image_path = request.args.get('image_path')
    selfie_path =  request.args.get('selfie_path')

    #getting the full path
    STORAGE_ROUTE = os.environ['STORAGE_ROUTE']     #path for processed images
    STORAGE_ROUTE_BD = os.environ['STORAGE_ROUTE_BD']  #path for images from the database
    image_path = f"{STORAGE_ROUTE_BD}{image_path}"
    selfie_path = f"{STORAGE_ROUTE_BD}{selfie_path}"
       
    # Verificar si las imágenes existen
    if not os.path.isfile(image_path):
        return jsonify({'error': f'DPI image not found at path: {image_path}'})

    if not os.path.isfile(selfie_path):
        return jsonify({'error': f'Selfie image not found at path: {selfie_path}'})

    #crop and resize photo_dpi, selfie 
    dpi = crop_photo(image_path)
    selfie = resize_selfie(selfie_path)
    
    #getting the full path
    img_results = f"{STORAGE_ROUTE}{dpi}"
    selfie_results = f"{STORAGE_ROUTE}{selfie}"

    #function to compare faces
    #obtains as parameters the cropped dpi photo and the resized selfie
    #returns true or false
    results = facial_compare(img_results, selfie_results)

    json_result = json.dumps({'results': results}, ensure_ascii=False) 
    return json_result
