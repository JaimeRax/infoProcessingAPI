from flask import request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pytesseract
import numpy as np
import zipfile
import cv2
import os

# Función para guardar la imagen de plantilla
def save_template_image(template_image):
    upload_folder = 'template/'
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

def extrain_info(roi_array):

    load_dotenv() # load the .env file 
    base_path = os.getenv('PATH_INFO')

    roi = roi_array;

    points = 0.01
    pixelThreshold = 800
    template_image = os.path.join(base_path, 'app/lectorDPI/plantilla.png')

    imgQ = cv2.imread(template_image)
    per = 25
    h,w,c = imgQ.shape
    num_keypoints = int(h * w * points)

    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(imgQ,None)
    impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

    # read directory of files
    path_files = os.path.join(base_path, 'unzipped/')
    myPiclist = os.listdir(path_files)

    return template_image, myPiclist, roi

