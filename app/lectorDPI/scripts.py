import os
import cv2
import numpy as np
import pytesseract
from tqdm import tqdm

#from app.facialRecognition.scripts import facial_compare

#
# list of regions of interest
# positions x, y 

roi = [
        [(24, 164), (327, 215), 'text', 'cui'], 
        [(350, 167), (650, 242), 'text', 'name'], 
        [(350, 255), (548, 338), 'text', 'lasname'], 
        [(350, 357), (515, 390), 'text', 'nac'], 
        [(350, 410), (515, 442), 'text', 'sex'], 
        [(350, 470), (502, 505), 'text', 'fech'], 
        [(550, 355), (630, 390), 'text', 'pais'], 
        [(700, 208), (996, 587), 'img', 'photo'],
        [(294, 524), (543, 602), 'img', 'firm'] 
   ]

numeros = list(range(180, 48, -2))
context = {
        '0': numeros,
        '1': numeros,
        '2': numeros,
        '3': numeros,
        '4': numeros,
        '5': numeros,
        '6': numeros,
}

# conversion of letters to numbers and numbers to letters

letras_numeros = {
      'E': '3',   'N': '8',   'F': '5', 
      'B': '8',   'M': '4',   'A': '4', 
      'R': '2',   'J': '1',   'U': '0', 
      'L': '1',   'G': '6',   'O': '0', 
      'S': '5',   'P': '9',    'T': '7', 
      'D': '0',   'I': '1',    'C': '0', 
      'Y': '7',   'V': '7'
   }

numeros_letras = {
      '0': 'O',
      '1': 'I',
      '3': 'B',
      '4': 'A',
      '5': 'S',
      '6': 'G',
      '7': 'T',
      '8': 'B',
   }


# function to process images with threshold values ​​and text extraction
# receives as parameters an image, accepted list of values, context, and the position of the image       config=f"--psm 6 -c tessedit_char_whitelist={whitelist}"
# returns the best extracted text

def process_threshold(image, whitelist, context, position):
   aux_text = []
   bestText = ""
   gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   position_str = str(position)  
   if position_str in context:
        thresholds = context[position_str]      
        for threshold_value in thresholds:
            _, thresholded_img = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
            text = pytesseract.image_to_string(thresholded_img, config=f"--psm 6 -c tessedit_char_whitelist={whitelist}")
            #print(text)
            if text:
                aux_text.append(text)
            if aux_text:
               bestText = max(aux_text, key=lambda x: aux_text.count(x)) 
               if position == 5:
                  if len(bestText) >= 9:
                     if bestText[0].isalpha() or bestText[1].isalpha():
                        primer_caracter = letras_numeros.get(bestText[0], bestText[0])
                        segundo_caracter = letras_numeros.get(bestText[1], bestText[1])
                        bestText = primer_caracter + segundo_caracter + bestText[2:]
                  
                     if bestText[2].isdigit() or bestText[3].isdigit() or bestText[4].isdigit():
                        tercer_caracter = numeros_letras.get(bestText[2], bestText[2])
                        cuarto_caracter = numeros_letras.get(bestText[3], bestText[3])
                        quinto_caracter = numeros_letras.get(bestText[4], bestText[4])
                        bestText = bestText[:2] + tercer_caracter + cuarto_caracter + quinto_caracter + bestText[5:]
                        
                     if bestText[5].isalpha() or bestText[6].isalpha() or bestText[7].isalpha() or bestText[8].isalpha():
                        sexto_caracter = letras_numeros.get(bestText[5], bestText[5])
                        septimo_caracter = letras_numeros.get(bestText[6], bestText[6])
                        octavo_caracter = letras_numeros.get(bestText[7], bestText[7])
                        noveno_caracter = letras_numeros.get(bestText[8], bestText[8])
                        bestText = bestText[:5] + sexto_caracter + septimo_caracter + octavo_caracter + noveno_caracter + bestText[9:]
                  else:
                     bestText
   return bestText.replace('\n', ' ')


# function to create the match points and roi processing to crop the points of interest
# receives the image and the number of coincidence points as parameters
# returns cropped images and positions

def process_photo_plantilla(image, points):
   
   plantilla = '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
   # STORAGE_ROUTE = os.environ['STORAGE_ROUTE']
   # plantilla_path = f"{STORAGE_ROUTE}{plantilla}"
   
   imgQ = cv2.imread(plantilla)
   per = 25
   h,w,c = imgQ.shape
   num_keypoints = int(h * w * points)

   orb = cv2.ORB_create(num_keypoints)
   kp1, des1 = orb.detectAndCompute(imgQ,None)
   impKp1 = cv2.drawKeypoints(imgQ,kp1,None)
     
   img = cv2.imread(image)  
   kp2, des2 = orb.detectAndCompute(img,None)
   bf = cv2.BFMatcher(cv2.NORM_HAMMING)
   matches = bf.match(des2,des1)
   matches = list(matches)
   matches.sort(key= lambda x: x.distance)
   good = matches[:int(len(matches)*(per/100))]
   imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:500],None,flags=2)
      
   srcPoints = np.float32([kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
   dstPoints = np.float32([kp1[m.trainIdx].pt for m in good ]).reshape(-1, 1, 2)
    
   M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
   imgscan = cv2.warpPerspective(img,M,(w,h))

   imgShow = imgscan.copy()
   imgMask = np.zeros_like(imgShow) 
   
   images_cropped = []  
   positions_x = []
   
   for x,r in enumerate(roi):
        cv2.rectangle(imgMask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.1,0)
        imgCrop = imgscan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        images_cropped.append(imgCrop)
        positions_x.append(x)
        
   return images_cropped, positions_x


# processes an image, extracts text from a specific region in the image and filters the resulting text
# receives as parameters an image, accepted list of values, context, and the position of the image
# returns the best extracted text

def crop_information(image, index, whitelist, context):
   points = 0.01
   images_cropped, positions_x = process_photo_plantilla(image, points)
   imagen_dpi = images_cropped[index]
   extracted_text = process_threshold(imagen_dpi, whitelist, context, index)
   return extracted_text 
 

# function to crop a single image of interest
# receives as parameters an image
# returns the cropped image

def crop_firm(image_path):
   points = 0.1
   images_cropped, positions_x = process_photo_plantilla(image_path, points)
   imagen_dpi = images_cropped[8]

   return imagen_dpi
 

#######################################################################################
########################   principal function for face compare ########################                            
#######################################################################################

 
# function to crop a single image of interest
# receives as parameters an image
# returns the cropped image

def crop_photo(image_path):
   
   points = 0.015
   images_cropped, positions_x = process_photo_plantilla(image_path, points)
   imagen_dpi = images_cropped[7]
   
   altura = 600
   altura_actual, ancho_actual = imagen_dpi.shape[:2]
   factor_de_escala = altura / altura_actual
   imagen_redimensionada = cv2.resize(imagen_dpi, (int(ancho_actual * factor_de_escala), altura))

   cv2.imwrite('img/foto_dpi.png', imagen_redimensionada)
   
   return "img/foto_dpi.png"


#resize selfie
def resize_selfie(selfie_path):
    selfie = cv2.imread(selfie_path)
    altura = 600
    altura_actual, ancho_actual = selfie.shape[:2]
    factor_de_escala = altura / altura_actual
    imagen_redimensionada = cv2.resize(selfie, (int(ancho_actual * factor_de_escala), altura))
    cv2.imwrite('img/selfie.png',imagen_redimensionada)
    
    return "img/selfie.png"



#######################################################################################
########################   principal function for extract info ########################                            
#######################################################################################


# The extract_info_DPI function processes a specified image (image_path) 
# and uses the crop_information function to extract information from various regions of interest in the image
# receives as parameters an image
# returns all the results of the extracted texts

def extract_info_DPI(image_path):
   
   result_dict = {}
   
   regions = [
       ('cui', 0, '0123456789 '),
       ('name', 1, 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ'),
       ('lastname', 2, 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ'),
       ('nationality', 3, 'GTMASCULINOFE'),
       ('sex', 4, 'GUTMASCULINOFEN'),
       ('fech', 5, '0123456789ENFBMARJULGOSPTDICYV'),
       ('country', 6, 'GTM')
   ]

   for key, index, whitelist in tqdm(regions, desc="Processing regions"):
       result_dict[key] = crop_information(image_path, index, whitelist, context)
    
   output_str = ""
   for key, value in result_dict.items():
       output_str += f"{key}: {value}\n"

   return output_str

