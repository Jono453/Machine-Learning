#Script for computer vision for DRC 2019

import cv2 #using py2
import numpy as np
from imutils import paths
from imutils import build_montages
import argparse
import requests #package for image content
import os
import time

'''
#Video streaming (inbuilt webcam)
cap = cv2.VideoCapture(0)

while (True):
    #capture frame by frame
    ret, frame = cap.read() #returns true or false
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

#load images from folder DRC from C:\Users\Jonathan\ML\DRC
#IMG_0462, IMG_0463...

ap = argparse.ArgumentParser()
ap.add_argument("-i","--drc", required=True, help="path to input folder for drc test images")
args = vars(ap.parse_args())

total = 462
test_images = []

#p = os.path.sep.join(["IMG_", "{}.jpg".format(str(total))])
imagePaths = list(paths.list_images(args["drc"]))

for image in imagePaths:
    img = cv2.imread(image)
    test_images.append(img)

#looping through the set of images in the DRC image folder
for img in test_images:
    #cv2.imshow("test",img)

    #reducing ROI
    #print img.shape #rows x col. 480 x 640
    img = img[185:,55:]

    #1) Detect the track (Blue on Left and Yellow on Right)

    #convert to HSV to find Blue
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    low_blue = np.array([110,50,50])
    hi_blue = np.array([130,230,245])
    low_yellow = np.array([20,50,50])
    hi_yellow = np.array([30,250,240])

    mask = cv2.inRange(hsv,low_blue,hi_blue)
    mask2 = cv2.inRange(hsv,low_yellow,hi_yellow)

    #bitwise AND mask and original
    res = cv2.bitwise_and(img,img,mask = mask)
    res3 = cv2.bitwise_and(img,img,mask = mask2)

    #combine both blue and yellow paths
    detect = cv2.addWeighted(res,0.5,res3,0.5,0.0)

    cv2.imshow('original',img)
    #cv2.imshow('res',res) #blue hsv detection
    #cv2.imshow('yellow_result', res3)
    cv2.imshow('color_path',detect)

    #2) Path planning and calculations




    #3) Steering and Acceleration on UGV
    #Talk to Arduino through i2c or WiringPi?


    cv2.waitKey(0)

cv2.destroyAllWindows()
