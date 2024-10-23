import os
import time
import shutil

def remove_old_directories(base_dir, age_limit_minutes=5):
    current_time = time.time()
    age_limit_seconds = age_limit_minutes * 60

    # Verificar si la carpeta base existe
    if not os.path.exists(base_dir):
        print(f"El directorio {base_dir} no existe.")
        return
    
    # Recorrer todos los elementos dentro de la carpeta base
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)

        # Si el item es un directorio
        if os.path.isdir(item_path):
            # Obtener el tiempo de última modificación
            last_modified_time = os.path.getmtime(item_path)
            # Calcular la antigüedad
            age_in_seconds = current_time - last_modified_time

            # Si el directorio es más antiguo que el límite, eliminarlo
            if age_in_seconds > age_limit_seconds:
                try:
                    shutil.rmtree(item_path)  # Eliminar la carpeta y su contenido
                    print(f"Carpeta eliminada: {item_path}")
                except Exception as e:
                    print(f"Error al eliminar {item_path}: {str(e)}")
        else:
            # Si es un archivo, verificar si es un archivo ZIP
            if item.endswith('.zip'):
                print(f"Archivo .zip encontrado, no se eliminará: {item_path}")


