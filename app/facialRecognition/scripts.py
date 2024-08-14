from deepface import DeepFace

def facial_compare(first_image, second_image):
    try:
        if first_image and second_image:
            # Comprobar si las imagenes muestran la misma persona
            result = DeepFace.verify(first_image, second_image)
            # Obteniendo resultados
            if result["verified"]:
                return True   
            else:
                return False
        else:
            return "Debes proporcionar ambas imagenes."
    except: 
        return "No se pudo detectar un rostro. Confirme que la imagen es una foto un rostro"


    