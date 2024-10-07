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
   ]

per = 25
pixelThreshold = 800
template_image = os.path.join(base_path, 'app/lectorDPI/plantilla.png')
imgQ = cv2.imread(template_image)
h,w,c = imgQ.shape
points = 0.01
num_keypoints = int(h * w * points)

orb = cv2.ORB_create(5000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
# impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path_files = os.path.join(base_path, 'media/')
myPiclist = os.listdir(path_files)
print(myPiclist)

for j,y in enumerate(myPiclist):
    img = cv2.imread(path_files + "/" + y)

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

print(myData)
cv2.imshow(y+"2", imgShow)

# cv2.imshow("keyPontsQuery", impKp1)
cv2.waitKey(0)

   # '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
