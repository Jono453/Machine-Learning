#PanTilt code

import cv2
import numpy as np
from picamera.array import PiRGBArray
import smbus
import time
bus = smbus.SMBus(1)

address = 0x04 #for 12C with Arduino

def writeNumber(value):
    bus.write_byte(address,value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number

imageWidth  = 320                       # Camera image width
imageHeight = 240                       # Camera image height

camera = PiCamera()
camera.resolution = (imageWidth,imageHeight)
camera.framerate = 18
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
    cv2.imshow("test",mask)
    
    #Using contours for error calculation
    #each contour is a numpy array of (x,y) coordinates = boundary of a shape
    img,contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #Create bounding rectangle
    minArea = 200 #threshold (can modify later to get largest)
    c_max = 1
    #Setpoint
    sp_x = imageWidth/2 #160
    sp_y = imageHeight/2 #120
    
    for c in contours:
        CArea = cv2.contourArea(c)
        if CArea < minArea:
            continue
        x,y,w,h = cv2.boundingRect(c)
        #cv2.drawMarker(img,(sp_x,sp_y),(255,0,255),cv2.MARKER_CROSS,5,1) 

        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        cv2.imshow("test",img)

        #Measured Centre of Box
        measured_x = x + w/2
        measured_y = y + h/2

        #print("image shape",img.shape)
        #print("Image_X: ", sp_x)
        #print("Image_Y: ", sp_y)
        #print("BoxCentre_X: ", measured_x)
        #print("BoxCentre_Y: ", measured_y)
         
        #Error
        error_x = abs(sp_x - measured_x)
        error_y = abs(sp_y - measured_y)

        print("Error_x: ", error_x)
        print("Error_y: ", error_y)
        print("\n")
    
        #Command servo motors to turn on Arduino
        while ():
            var = input("Test")

            writeNumber(var)
            print("Number sent was: ", var)
            time.sleep(1)
            number = readNumber()
            print("I received: ", number)

    #GUI stuff
    key = cv2.waitKey(5) & 0xFF

    frameCapture.truncate(0)

    if key == ord("q"):
        break

