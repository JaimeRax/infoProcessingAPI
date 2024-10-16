from flask import request, jsonify
from werkzeug.utils import secure_filename
import zipfile
import os

# Función para guardar la imagen de plantilla
def save_template_image(template_image):
    upload_folder = 'img/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Obtener el nombre seguro del archivo
    filename = secure_filename(template_image.filename)
    image_path = os.path.join(upload_folder, filename)
    template_image.save(image_path)

    return filename


# Función para descomprimir el archivo ZIP
def unzip_file(zip_file):
    unzip_folder = 'unzipped/'
    if not os.path.exists(unzip_folder):
        os.makedirs(unzip_folder)

    zip_path = os.path.join(unzip_folder, secure_filename(zip_file.filename))
    
    # Guardar el archivo ZIP
    zip_file.save(zip_path)
    
    # Descomprimir el archivo
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)

    # Obtener la lista de archivos descomprimidos
    extracted_files = os.listdir(unzip_folder)
    
    return extracted_files
