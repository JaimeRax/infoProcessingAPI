from werkzeug.utils import secure_filename
import zipfile
import shutil
import os

# function to save the template
def save_template_image(template_image):
    upload_folder = 'template/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(template_image.filename)
    image_path = os.path.join(upload_folder, filename)
    template_image.save(image_path)

    return image_path


# function to unzip the zip file
def unzip_file(zip_file):
    unzip_folder = 'unzipped/'
    zip_name = os.path.splitext(secure_filename(zip_file.filename))[0]  # obtain name
    extract_folder = os.path.join(unzip_folder, zip_name)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    zip_path = os.path.join(unzip_folder, secure_filename(zip_file.filename))
    zip_file.save(zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: # unzip the file 
        for member in zip_ref.namelist():
            if not member.endswith('/'):
                zip_ref.extract(member, unzip_folder)

        path_dir = unzip_folder+zip_name
    
    return path_dir


# function to delete directories
def delete_directories():
    directories = ['template/', 'unzipped/', 'cropImage/'] 
    
    for directory in directories:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory) 
                print(f"Eliminado: {directory}")
            except Exception as e:
                print(f"Error al eliminar {directory}: {e}")
        else:
            print(f"El directorio {directory} no existe.")
