#Keyboard Controlled Pan/Tilt (note: works in terminal not IDLE)
#Modified from the GPIOZERO documentation

import curses as button
import cv2
from gpiozero import Motor

tiltMotor = Motor(3,4) #Tilt
panMotor = Motor(17,27) #Pan

#Create dictionary for button mapping
actions = {
    button.KEY_UP: tiltMotor.forward(0.01),
    button.KEY_DOWN: tiltMotor.backward(0.01),
    button.KEY_LEFT: panMotor.forward(0.01),
    button.KEY_RIGHT: panMotor.backward(0.01),
    }

def main(window):
    next_key = None
    while True:
        button.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            #Key is down
            button.halfdelay(2)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
                #Key is up
            tiltMotor.stop()
            panMotor.stop()

        key = cv2.waitKey(5) & 0xFF

        if key == ord("q"):
            break

button.wrapper(main)




