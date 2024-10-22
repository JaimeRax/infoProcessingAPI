from flask import Blueprint, jsonify, request, send_file, make_response
from app.common.scripts import inicializandoConexion
from app.lectorDPI.processRequest import save_template_image 
from app.lectorDPI.processRequest import delete_directories
from app.lectorDPI.processRequest import unzip_file 
from app.lectorDPI.extract_multiple import extrain_info_multiple 
from app.lectorDPI.extract_single import extrain_info_single 
import zipfile, ast, os, json

# Crear un Blueprint para las rutas 
lectorDPI = Blueprint('lectorDPI', __name__)

# route principal
@lectorDPI.route('/', methods=['GET'])
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
@lectorDPI.route('/extract_single', methods=['POST'])
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

        CROP_IMAGE_FOLDER = 'cropImage/'

        # Crear el archivo .txt o .json con los datos extraídos
        output_filename = f"{template_id}_data.json"
        output_filepath = os.path.join(CROP_IMAGE_FOLDER, output_filename)
        
        with open(output_filepath, 'w') as f:
            json.dump(extrain_data, f, indent=2)  # Guardar los datos en formato JSON

        # Nombre y ruta para el archivo ZIP
        zip_filename = f"{template_id}_output.zip"
        zip_filepath = os.path.join(CROP_IMAGE_FOLDER, zip_filename)

        # Crear el archivo ZIP
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            # Añadir el archivo de datos JSON al ZIP
            zipf.write(output_filepath, output_filename)

            # Verificar si la carpeta CropImage existe
            if os.path.exists(CROP_IMAGE_FOLDER) and os.listdir(CROP_IMAGE_FOLDER):
                # Añadir las imágenes recortadas al ZIP
                for root, dirs, files in os.walk(CROP_IMAGE_FOLDER):
                    for file in files:
                        if file not in [zip_filename, output_filename]:
                            zipf.write(os.path.join(root, file), file)
            else:
                # Si la carpeta no existe o está vacía, solo agregamos el archivo JSON
                print(f"No se encontraron imágenes en {CROP_IMAGE_FOLDER}.")

        # Enviar el archivo .zip generado
        return send_file(zip_filepath, as_attachment=True, download_name=zip_filename)

        return response
        # delete_directories()

    except Exception as e:
        return jsonify({'error': str(e)}), 500
