from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pytesseract
import numpy as np
import zipfile
import shutil
import cv2
import os

# Funcion para guardar la imagen de plantilla
def save_template_image(template_image):
    upload_folder = 'template/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(template_image.filename)
    image_path = os.path.join(upload_folder, filename)
    template_image.save(image_path)

    return image_path



# Funcion para descomprimir el archivo ZIP
def unzip_file(zip_file):
    unzip_folder = 'unzipped/'
    zip_name = os.path.splitext(secure_filename(zip_file.filename))[0]  # Obtener nombre sin extension
    extract_folder = os.path.join(unzip_folder, zip_name)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    zip_path = os.path.join(unzip_folder, secure_filename(zip_file.filename))
    zip_file.save(zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: # Descomprimir el archivo
        for member in zip_ref.namelist():
            if not member.endswith('/'):
                zip_ref.extract(member, unzip_folder)

        path_dir = unzip_folder+zip_name
    
    return path_dir



def delete_directories():
    directories = ['template/', 'unzipped/'] # Directorios a eliminar
    
    for directory in directories:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory) # Elimina el directorio y todo su contenido
                print(f"Eliminado: {directory}")
            except Exception as e:
                print(f"Error al eliminar {directory}: {e}")
        else:
            print(f"El directorio {directory} no existe.")



def extrain_info(roi_array, path_template, path_directory):
    output_dir = "cropImage"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    load_dotenv() # load the .env file 
    base_path = os.getenv('PATH_INFO')

    points = 0.01
    pixelThreshold = 800
    template_image = os.path.join(base_path, path_template)

    imgQ = cv2.imread(template_image)
    per = 25
    h,w,c = imgQ.shape
    num_keypoints = int(h * w * points)

    orb = cv2.ORB_create(num_keypoints)
    kp1, des1 = orb.detectAndCompute(imgQ,None)

    # read directory of files
    path_files = os.path.join(base_path, path_directory)
    myPiclist = os.listdir(path_files)
    print(myPiclist)

    all_extracted_data = []

    for j,y in enumerate(myPiclist):
        img = cv2.imread(path_files + "/" + y)
        kp2, des2 = orb.detectAndCompute(img,None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2,des1)
        matches = list(matches)
        matches.sort(key=lambda x: x.distance)
        good = matches[:int(len(matches)*(per/100))]

        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
        imgScan = cv2.warpPerspective(img,M,(w,h))

        imgShow = imgScan.copy()
        imgMask = np.zeros_like(imgShow)
        myData = []

        print(f'################ Extracting data from form {j} ##################')

        for x,r in enumerate(roi_array):
            cv2.rectangle(imgMask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask,0.1,0)

            # crop to image with roi
            imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

            # extrain data of the image
            if r[2] == 'text':
                best_text = get_best_text(imgCrop)
                myData.append(best_text)

            # save image in 'cropImage'
            if r[2] == 'img':
                output_path = os.path.join(output_dir, f'{y}')  
                cv2.imwrite(output_path, imgCrop)
        all_extracted_data.extend(myData)
        
    return all_extracted_data



def get_best_text(cropped_image):
    aux_texts = []
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    for threshold_value in range(50,220,10):
        _, thresholded_img = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY) # Aplicar umbral

        text = pytesseract.image_to_string(thresholded_img, config=f"--psm 6 -l spa")

        # Añadir texto extraído a la lista si no está vacío
        if text.strip():
            aux_texts.append(text.strip())

    if aux_texts:
        best_text = max(aux_texts, key=aux_texts.count)  # El texto mas frecuente
        return best_text.replace('\n', ' ')  # Devolvemos el texto sin saltos de linea
    else:
        return ""  # En caso de que no se extraiga ningun texto


