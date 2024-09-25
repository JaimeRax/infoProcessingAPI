import cv2
import pytesseract
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv() # load the .env file 
base_path = os.getenv('PATH_INFO')

per = 25
template_image = os.path.join(base_path, 'app/lectorDPI/plantilla.png')
imgQ = cv2.imread(template_image)
h,w,c = imgQ.shape
# imgQ = cv2.resize(imgQ, (w//3,h//3))
points = 0.1
num_keypoints = int(h * w * points)

orb = cv2.ORB_create(6000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
# impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path_files = os.path.join(base_path, 'media/')
myPiclist = os.listdir(path_files)
print(myPiclist)

for j,y in enumerate(myPiclist):
    img = cv2.imread(path_files + "/" + y)
    # img = cv2.resize(img, (w//3,h//3))
    # cv2.imshow(y,img)
    kp2, des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2,des1)
    matches = list(matches)
    matches.sort(key=lambda x: x.distance)
    good = matches[:int(len(matches)*(per/100))]
    imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:400],None,flags=2)
    # cv2.imshow(y,imgMatch)

    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
    imgScan = cv2.warpPerspective(img,M,(w,h))
    imgScan = cv2.resize(imgScan, (w//3,h//3))
    cv2.imshow(y, imgScan)

# cv2.imshow("keyPontsQuery", impKp1)
cv2.imshow("Output", imgQ)
cv2.waitKey(0)

   # '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
