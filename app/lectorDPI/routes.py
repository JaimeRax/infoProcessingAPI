from flask import Blueprint, jsonify, request, send_file, make_response
from app.common.scripts import inicializandoConexion
from app.lectorDPI.processRequest import save_template_image 
from app.lectorDPI.processRequest import delete_directories
from app.lectorDPI.processRequest import unzip_file 
from app.lectorDPI.extract_multiple import extrain_info_multiple 
from app.lectorDPI.extract_single import extrain_info_single 
from app.lectorDPI.deleteDirectories import remove_old_directories 
import zipfile, ast, os, json

# Crear un Blueprint para las rutas 
lectorDPI = Blueprint('lectorDPI', __name__)

# route principal
@lectorDPI.route('/', methods=['GET'])
def index():
    msg = inicializandoConexion()
    return jsonify({'msg': msg})


# route to the extract multiple files
@lectorDPI.route('/extract_multiple', methods=['POST'])
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
        template_filename, template_id, new_filename = save_template_image(template_image)
        extracted_files = unzip_file(zip_file)

        filename_without_extension = os.path.splitext(new_filename)[0]
        extrain_data, output_dir = extrain_info_multiple(roi, template_filename, extracted_files, template_id, filename_without_extension)

        # Crear el archivo .txt o .json con los datos extraídos
        output_filename = f"{filename_without_extension}.json"
        output_filepath = os.path.join(output_dir, output_filename)

        with open(output_filepath, 'w') as f:
            json.dump(extrain_data, f, indent=2)  # Guardar los datos en formato JSON

        # Nombre y ruta para el archivo ZIP
        zip_filename = f"{filename_without_extension}.zip"
        zip_filepath = os.path.join("cropImages", zip_filename)

        # Crear el archivo ZIP
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            if os.path.exists(output_dir) and os.listdir(output_dir):
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, output_dir))

            else:
                print(f"No se encontraron imágenes en {output_dir}.")

        remove_old_directories("cropImages", 5)  # Elimina directorios viejos de más de 5 minutos

        # Enviar el archivo .zip generado
        return send_file(zip_filepath, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        return jsonify({'error': str(e)}), 500




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
        template_filename, template_id, new_filename = save_template_image(template_image)
        
        filename_without_extension = os.path.splitext(new_filename)[0]
        extrain_data, output_dir = extrain_info_single(roi, template_filename, template_id, filename_without_extension)

        # Crear el archivo .txt o .json con los datos extraídos
        output_filename = f"{filename_without_extension}.json"
        output_filepath = os.path.join(output_dir, output_filename)

        with open(output_filepath, 'w') as f:
            json.dump(extrain_data, f, indent=2)  # Guardar los datos en formato JSON

        # Nombre y ruta para el archivo ZIP
        zip_filename = f"{filename_without_extension}.zip"
        zip_filepath = os.path.join("cropImages", zip_filename)

        # Crear el archivo ZIP
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            if os.path.exists(output_dir) and os.listdir(output_dir):
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, output_dir))

            else:
                print(f"No se encontraron imágenes en {output_dir}.")

        remove_old_directories("cropImages", 5)  # Elimina directorios viejos de más de 5 minutos

        # Enviar el archivo .zip generado
        return send_file(zip_filepath, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

