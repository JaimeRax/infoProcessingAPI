import cv2
import os


imgQ = cv2.imread('plantilla.png')
h,w,c = imgQ.shape
imgQ = cv2.resize(imgQ, (w//3,h//3))

orb = cv2.ORB_create(4000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
# impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path = 'name_route'
myPiclist = os.listdir(path)
print(myPiclist)



# cv2.imshow("keyPontsQuery", impKp1)
cv2.imshow("Output", imgQ)
cv2.waitKey(0)

   # '/home/jaime/Documents/university/infoProcessingAPI/app/lectorDPI/plantilla.png'   
