from re import template
import cv2
import os
from dotenv import load_dotenv

load_dotenv() # load the .env file 
base_path = os.getenv('PATH_INFO')

template_image = os.path.join(base_path, 'app/lectorDPI/plantilla.png')
imgQ = cv2.imread(template_image)
h,w,c = imgQ.shape
imgQ = cv2.resize(imgQ, (w//3,h//3))

orb = cv2.ORB_create(4000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
# impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path_files = os.path.join(base_path, 'media/')
myPiclist = os.listdir(path_files)
print(myPiclist)



# cv2.imshow("keyPontsQuery", impKp1)
cv2.imshow("Output", imgQ)
cv2.waitKey(0)

   # '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
