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

    return image_path


# Función para descomprimir el archivo ZIP
def unzip_file(zip_file):
    unzip_folder = 'unzipped/'
    zip_name = os.path.splitext(secure_filename(zip_file.filename))[0]  # Obtener nombre sin extensión
    extract_folder = os.path.join(unzip_folder, zip_name)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    zip_path = os.path.join(unzip_folder, secure_filename(zip_file.filename))
    zip_file.save(zip_path)
    
    # Descomprimir el archivo
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extraer los archivos sin incluir rutas internas adicionales
        for member in zip_ref.namelist():
            if not member.endswith('/'):
                zip_ref.extract(member, unzip_folder)

        path_dir = unzip_folder+zip_name
        # extracted_files = os.listdir(path_dir)
    
    return path_dir

def extrain_info(roi_array, path_template, path_directory):

    load_dotenv() # load the .env file 
    base_path = os.getenv('PATH_INFO')

    roi = roi_array;

    points = 0.01
    pixelThreshold = 800
    template_image = os.path.join(base_path, path_template)

    imgQ = cv2.imread(template_image)
    per = 25
    h,w,c = imgQ.shape
    num_keypoints = int(h * w * points)

    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(imgQ,None)
    impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

    # read directory of files
    path_files = os.path.join(base_path, path_directory)
    print(path_files)
    myPiclist = os.listdir(path_files)

    for j,y in enumerate(myPiclist):
        img = cv2.imread(path_files + "/" + y)

        print(img)
        kp2, des2 = orb.detectAndCompute(img,None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2,des1)
        matches = list(matches)
        matches.sort(key=lambda x: x.distance)
        good = matches[:int(len(matches)*(per/100))]
        imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:400],None,flags=2)

        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
        imgScan = cv2.warpPerspective(img,M,(w,h))

        imgShow = imgScan.copy()
        imgMask = np.zeros_like(imgShow)

        myData = []

        print(f'################ Extracting data from form {j} ##################')

        for x,r in enumerate(roi):
            cv2.rectangle(imgMask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.1,0)
            imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

            if r[2] == 'text':
                print('{} :{}'.format(r[3], pytesseract.image_to_string(imgCrop)))
                myData.append(pytesseract.image_to_string(imgCrop))
            if r[3] == 'img':
                imgGray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
                imgThresh = cv2.threshold(imgGray, 170,255,cv2.THRESH_BINARY_INV)[1]
                totalPixels = cv2.countNonZero(imgThresh)
                if totalPixels>pixelThreshold: totalPixels =1;
                else: totalPixels=0
                print(f'{r[3]} :{totalPixels}')
                myData.append(totalPixels)

    return myPiclist

