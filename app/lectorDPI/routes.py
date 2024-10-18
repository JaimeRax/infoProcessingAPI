from flask import Blueprint, jsonify, request
from app.common.scripts import inicializandoConexion
from app.lectorDPI.processRequest import save_template_image 
from app.lectorDPI.processRequest import delete_directories
from app.lectorDPI.processRequest import unzip_file 
from app.lectorDPI.extract_multiple import extrain_info_multiple 
from app.lectorDPI.extract_single import extrain_info_single 
import ast

# Crear un Blueprint para las rutas 
lectorDPI = Blueprint('lectorDPI', __name__)

# route principal
@lectorDPI.route('/')
def index():
    msg = inicializandoConexion()
    return jsonify({'msg': msg})


# route to the extract multiple files
@lectorDPI.route('/extract_multiple')
def extract_multiple():
    if 'template_image' not in request.files or 'zip_file' not in request.files or 'roi_array' not in request.form:
        return jsonify({'error': 'Faltan archivos. Se requieren template_image y zip_file y roi_array.'}), 400
    
    template_image = request.files['template_image']
    zip_file = request.files['zip_file']
    
    if template_image.filename == '' or zip_file.filename == '':
        return jsonify({'error': 'Uno o mas archivos no fueron seleccionados.'}), 400

    try:
        roi_array = request.form['roi_array']
        roi = ast.literal_eval(roi_array)
        template_filename, template_id = save_template_image(template_image)
        extracted_files = unzip_file(zip_file)
        extrain_data = extrain_info_multiple(roi, template_filename, extracted_files, template_id)
        # delete_directories()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'information': extrain_data,
    })



# route to the extract single file
@lectorDPI.route('/extract_single')
def extract_single():
    if 'template_image' not in request.files or 'roi_array' not in request.form:
        return jsonify({'error': 'Faltan archivos. Se requieren template_image y roi_array.'}), 400
    
    template_image = request.files['template_image']
    
    if template_image.filename == '':
        return jsonify({'error': 'template_image no fue seleccionado.'}), 400

    try:
        roi_array = request.form['roi_array']
        roi = ast.literal_eval(roi_array)
        template_filename, template_id = save_template_image(template_image)
        extrain_data = extrain_info_single(roi, template_filename, template_id)
        # delete_directories()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'information': extrain_data,
    })

