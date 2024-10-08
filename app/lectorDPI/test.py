import cv2
import pytesseract
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv() # load the .env file 
base_path = os.getenv('PATH_INFO')


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

per = 25
template_image = os.path.join(base_path, 'app/lectorDPI/plantilla.png')
imgQ = cv2.imread(template_image)
h,w,c = imgQ.shape
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
    
    # cv2.imshow(y, imgScan)
    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    for x,r in enumerate(roi):
        cv2.rectangle(imgMask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.1,0)
        # imgCrop = imgscan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        # images_cropped.append(imgCrop)
        # positions_x.append(x)

    imgShow = cv2.resize(imgShow, (w // 2, h // 2))
    cv2.imshow(y+"2", imgShow)
# cv2.imshow("keyPontsQuery", impKp1)
cv2.waitKey(0)

   # '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
