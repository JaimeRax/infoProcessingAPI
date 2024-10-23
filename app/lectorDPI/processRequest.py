from app.common.scripts import inicializandoConexion
from werkzeug.utils import secure_filename
from sqlalchemy import text as sql_text  
from datetime import datetime
import zipfile
import shutil
import os

# function to save the template
def save_template_image(template_image):
    upload_folder = 'template/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Get current date and time for upload date
    now = datetime.now()
    current_date = now.date()  
    current_time = now.time() 

    # Initialize the DB connection
    engine = inicializandoConexion()
    if engine is None:
        print("No se pudo establecer conexión con la base de datos.")
        return None

    try:
        # Insert into the database using raw SQL
        with engine.connect() as connection:

            # obtain image name
            filename = secure_filename(template_image.filename)

            select_query = sql_text("""
                    SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM templates
                """)
                
            # Ejecutar la consulta
            result = connection.execute(select_query)
            next_id = result.scalar()  # Obtener el valor del siguiente ID

            # Concatenar el siguiente ID con el filename original
            new_filename = f"{next_id}_{filename}"

            image_path = os.path.join(upload_folder, new_filename)
            template_image.save(image_path)


            insert_query = sql_text("""
                INSERT INTO templates(filename, date, time, file_path)
                VALUES (:filename, :date, :time, :file_path)
            """)
            connection.execute(insert_query, {
                'filename': new_filename,
                'date': current_date,
                'time': current_time,
                'file_path': image_path
            })

            template_id_query = sql_text("SELECT LAST_INSERT_ID()")
            result = connection.execute(template_id_query)
            template_id = result.scalar()

            connection.commit()  # Commit the transaction
            print("Datos insertados correctamente en la tabla 'templates'.")

    except Exception as ex:
        print(f"Error al insertar los datos: {ex}")
        return None, None

    return image_path, template_id, new_filename

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
    directories = ['cropImage/'] 
    
    for directory in directories:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory) 
                print(f"Eliminado: {directory}")
                return True
            except Exception as e:
                print(f"Error al eliminar {directory}: {e}")
                return False
        else:
            print(f"El directorio {directory} no existe.")
            return True
