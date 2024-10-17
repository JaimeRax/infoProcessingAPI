from app.lectorDPI.extract_data import get_best_text 
from dotenv import load_dotenv
import numpy as np
import cv2
import os


# Main function for processing and cropping the images 
def extrain_info_multiple(roi_array, path_template, path_directory):
    output_dir = "cropImage"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    load_dotenv() # load the .env file 
    base_path = os.getenv('PATH_INFO')

    template_image = os.path.join(base_path, path_template)

    imgQ = cv2.imread(template_image)
    per = 25
    h,w,c = imgQ.shape
    num_keypoints = int(h * w * 0.01)

    orb = cv2.ORB_create(num_keypoints)
    kp1, des1 = orb.detectAndCompute(imgQ,None)

    # read directory of files
    path_files = os.path.join(base_path, path_directory)
    myPiclist = os.listdir(path_files)
    print(myPiclist)

    all_extracted_data = {}

    for j,y in enumerate(myPiclist):
        img = cv2.imread(path_files + "/" + y)

        scale_percent = 65  
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

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
        extracted_texts = {}

        print(f'################ Extracting data from form {j} ##################')

        for x,r in enumerate(roi_array):
            if isinstance(r, (list, tuple)):
                cv2.rectangle(imgMask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
                imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)

                # crop to image with roi
                imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

                # extrain data of the image
                if r[2] == 'text':
                    best_text = get_best_text(imgCrop)
                    extracted_texts[r[3]] = best_text

                # save image in 'cropImage'
                if r[2] == 'img':
                    output_path = os.path.join(output_dir, f'{r[3]}-{y}')  
                    cv2.imwrite(output_path, imgCrop)

        all_extracted_data[f'img{j+1}'] = extracted_texts

    return all_extracted_data

