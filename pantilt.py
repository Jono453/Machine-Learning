#PanTilt code

'''
Pseudocode:
1. Detect red object
2. Remove noise
3. Create bounding box
4. PD controller for x and y motion of mechanism
5. Calculate offset in x and y directions.
6. Rotate motors until object is centre of camera field of view
(Later - machine learning/classifier to add on)
'''

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import Motor

imageWidth  = 320                       # Camera image width
imageHeight = 240                       # Camera image height

camera = PiCamera()
camera.resolution = (imageWidth,imageHeight)
camera.framerate = 15
frameCapture = PiRGBArray(camera,size = (imageWidth,imageHeight))

for frame in camera.capture_continuous(frameCapture,format = "bgr", use_video_port=True):

    image = frame.array

    #flip image to correct orientation
    image = cv2.flip(image,0)
    image = cv2.flip(image,1) #left-right

    #Blur - remove initial noise (low pass filter kernel)
    image = cv2.medianBlur(image,5)
        
    #convert to HSV image (basic thresholding)
    #Hue (0,179), Saturation (0,255), Value (0,255)
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 

    redLower = np.array([50,100,100]) 
    redUpper = np.array([240,255,250])
    
    mask = cv2.inRange(hsv,redLower,redUpper)
    #result = cv2.bitwise_and(image,image,mask = mask)
    
    #Using contours for error calculation
    #each contour is a numpy array of (x,y) coordinates = boundary of a shape
    img, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #Create bounding rectangle
    minArea = 200 #threshold (can modify later to get largest)
    c_max = 1
    #Setpoint
    sp_x = imageWidth/2
    sp_y = imageHeight/2
    
    for c in contours:
        CArea = cv2.contourArea(c)
        if CArea < minArea:
            continue
        x,y,w,h = cv2.boundingRect(c)
        cv2.drawMarker(img,(sp_x,sp_y),(255,0,255),cv2.MARKER_CROSS,5,1) 

        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        cv2.imshow("test",img)

        #Measured Centre of Box
        measured_x = x + w/2
        measured_y = y - h/2

        #Error
        error_x = abs(sp_x - measured_x)
        error_y = abs(sp_y - measured_y)

        print("Error [x]: %d" %error_x)
        print("Error [y]: %d\n" %error_y)
    
        #move motors
        #PanMotor = Motor(4,14)
        #TiltMotor = Motor(5,10)

    #GUI stuff
    key = cv2.waitKey(5) & 0xFF

    frameCapture.truncate(0)

    if key == ord("q"):
        break

