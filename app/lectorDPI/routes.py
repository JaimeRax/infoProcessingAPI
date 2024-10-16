from flask import Blueprint, jsonify, request
from app.common.scripts import inicializandoConexion
from app.lectorDPI.processRequest import save_template_image 
from app.lectorDPI.processRequest import unzip_file 
from app.lectorDPI.processRequest import extrain_info 
import json

# Crear un Blueprint para las rutas 
lectorDPI = Blueprint('lectorDPI', __name__)

# route principal
@lectorDPI.route('/')
def index():
    msg = inicializandoConexion()
    return jsonify({'msg': msg})


# route to testing
@lectorDPI.route('/test')
def test():
    if 'template_image' not in request.files or 'zip_file' not in request.files or 'roi_array' not in request.form:
        return jsonify({'error': 'Faltan archivos. Se requieren template_image y zip_file y roi_array.'}), 400
    
    template_image = request.files['template_image']
    zip_file = request.files['zip_file']
    
    if template_image.filename == '' or zip_file.filename == '':
        return jsonify({'error': 'Uno o ambos archivos no fueron seleccionados.'}), 400

    try:

        roi_array = request.form['roi_array']
        template_filename = save_template_image(template_image)
        extracted_files = unzip_file(zip_file)

        extrain_data = extrain_info(roi_array, template_filename, extracted_files)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'data': extrain_data,
        'template': template_filename,
        'directory': extracted_files
    })


# http://localhost:5000/api/lectorDPI/extrain_info?image_path=media/chavi.jpeg
# @lectorDPI.route('/extrain_info', methods=['GET'])
# def extrain_info():
#     image_path = '/home/jaime/Documents/university/infoProcessingAPI/media/chavi.png'
#     results = extract_info_DPI(image_path)
#     results = results.replace('\n', ' ')
#
#     return jsonify({'resultExtrain': results})


# @lectorDPI.route('/extrain_info', methods=['POST'])
# def extrain_info():
#     # Obtener parámetros de la solicitud POST
#     # 1. image_path como parámetro en JSON
#     data = request.json
#     image_path = data.get('image_path')
#
#     # 2. Recibir el archivo ZIP
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#
#     # 3. Recibir el array como parte de la solicitud JSON
#     data_array = data.get('data_array', [])
#
#     # Verificar que el archivo sea un ZIP
#     if file.filename == '' or not file.filename.endswith('.zip'):
#         return jsonify({'error': 'Invalid file type. Only ZIP files are allowed.'}), 400
#
#     # Descomprimir el archivo ZIP
#     zip_path = '/tmp/uploaded.zip'  # Ruta temporal para guardar el archivo
#     file.save(zip_path)
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall('/tmp/unzipped')  # Directorio temporal para los archivos extraídos
#
#     # Procesar la imagen (usar el image_path recibido)
#     results = extract_info_DPI(image_path)
#     results = results.replace('\n', ' ')
#
#     # Realizar las operaciones que necesites con el array
#     # Por ejemplo, puedes iterar sobre el array y hacer algo con cada elemento.
#     for item in data_array:
#         # Procesar cada elemento
#         print(f"Procesando item: {item}")
#
#     return jsonify({'resultExtrain': results, 'processed_array': data_array})
