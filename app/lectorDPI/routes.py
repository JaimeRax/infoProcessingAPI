from flask import Blueprint, jsonify, request
from app.common.scripts import inicializandoConexion
from app.lectorDPI.processRequest import save_template_image 
from app.lectorDPI.processRequest import unzip_file 
from app.lectorDPI.processRequest import extrain_info 
from app.lectorDPI.processRequest import delete_directories
import ast

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
    
    if template_image.filename == '' or zip_file.filename == '' or roi_array.filename == '':
        return jsonify({'error': 'Uno o mas archivos no fueron seleccionados.'}), 400

    try:
        roi_array = request.form['roi_array']
        roi = ast.literal_eval(roi_array)
        template_filename = save_template_image(template_image)
        extracted_files = unzip_file(zip_file)
        extrain_data = extrain_info(roi, template_filename, extracted_files)
        # delete_directories()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'information': extrain_data,
    })
