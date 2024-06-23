import sys
sys.path.append('/home/pi/TurboPi/')
import cv2
from picamera2 import Picamera2
from time import sleep
import RPi.GPIO as GPIO
import numpy as np
import threading
import HiwonderSDK.Board as Board
import time

debug=True

#look at the name
def displayROI():
    #draw wall box
    image = cv2.line(img, (ROI1[0], ROI1[1]), (ROI1[2], ROI1[1]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI1[0], ROI1[1]), (ROI1[0], ROI1[3]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI1[2], ROI1[3]), (ROI1[2], ROI1[1]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI1[2], ROI1[3]), (ROI1[0], ROI1[3]), (0, 255, 0), 4)
    #draw wall box
    image = cv2.line(img, (ROI2[0], ROI2[1]), (ROI2[2], ROI2[1]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI2[0], ROI2[1]), (ROI2[0], ROI2[3]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI2[2], ROI2[3]), (ROI2[2], ROI2[1]), (0, 255, 0), 4)
    image = cv2.line(img, (ROI2[2], ROI2[3]), (ROI2[0], ROI2[3]), (0, 255, 0), 4)
    #draw line box
    image = cv2.line(img, (ROI3[0], ROI3[1]), (ROI3[2], ROI3[1]), (255, 255, 0), 4)
    image = cv2.line(img, (ROI3[0], ROI3[1]), (ROI3[0], ROI3[3]), (255, 255, 0), 4)
    image = cv2.line(img, (ROI3[2], ROI3[3]), (ROI3[2], ROI3[1]), (255, 255, 0), 4)
    image = cv2.line(img, (ROI3[2], ROI3[3]), (ROI3[0], ROI3[3]), (255, 255, 0), 4)

def write(motor, value):
    #this function tells the servo or dc motor to move
    if(motor == "servo"):
        pulseWidth = int(11.1*value+500)
        Board.setPWMServoPulse(3, pulseWidth, 1)

    elif(motor == "dc"):
        Board.setPWMServoPulse(1, value, 100)

def stop():
    #the name
    write("servo", 87)
    write("dc", 1500)



if __name__ == '__main__':
    #initialize camera, 640-480p, 30fps
    picam2 = Picamera2()
    picam2.preview_configuration.main.size =(640,480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 30
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    print("program started")
    
    lTurn = False
    rTurn = False
    t = 0

    #draw roi
    ROI1 = [0, 260, 240, 310]
    ROI2 = [450, 260, 640, 310]
    ROI3 = [200, 300, 440, 350]

    lDetected = False


    #finee tune later
    kp = 0.025
    kd = 0.01
    speed = 1350
    #1350
    straightConst = 87 #Tested from trial and error
    turnThresh = 150
    exitThresh = 1500

    #just set the angle of the car so it points straight ahead
    angle = 90
    prevAngle = angle
    #what a "sharp turn" angle should be (i guessed)
    sharpRight = 60
    sharpLeft = 120

    #initialize differences of the areas of the contours
    areaDiff = 0
    prevDiff = 0
    
    print("initializing motors")
    write("dc", 1500)

    sleep(5)
    key2_pin = 16

    #initialize values to car
    write("dc", speed) 
    write("servo", angle)

    #write("servo", 100)

    #main loop
    print("main loop started")
    while True:
        rightArea, leftArea = 0, 0
        img = picam2.capture_array()

        #is supposedd to draw contours via defining the range of a colour
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([200, 255, 70])
        imgThresh = cv2.inRange(img_hsv, lower_black, upper_black)
        lower_orange = np.array([0, 100, 20])
        upper_orange = np.array([25, 255, 255])
        o_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)
        contours_orange = cv2.findContours(o_mask[ROI3[1]:ROI3[3], ROI3[0]:ROI3[2]], cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours_left, hierarchy = cv2.findContours(imgThresh[ROI1[1]:ROI1[3], ROI1[0]:ROI1[2]], 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_right, hierarchy = cv2.findContours(imgThresh[ROI2[1]:ROI2[3], ROI2[0]:ROI2[2]], 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(imgThresh, 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        #find biggest area
        for cont in contours_left:
            area = cv2.contourArea(cont)

            leftArea = max(area, leftArea) 

        for cont in contours_right:
            area = cv2.contourArea(cont)

            rightArea = max(area, rightArea)

        #find orang
        for i in range(len(contours_orange)):
            cnt = contours_orange[i]
            area = cv2.contourArea(cnt)
            #orang found!!
            #print("im finding the orange")
            if area > 100:
                lDetected = True

        #draw the contours
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            cv2.drawContours(img, contours, i, (0, 255, 255), 2)
            approx=cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
            x,y,w,h=cv2.boundingRect(approx)
        
        #pid
        aDiff = rightArea - leftArea
        angle = int(max(straightConst + aDiff * kp + (aDiff - prevDiff) * kd, 0)) 
        if leftArea <= turnThresh and not rTurn:
            lTurn = True
            print("i want to turn left")
        elif rightArea <= turnThresh and not lTurn:
            rTurn = True
            print("i want to turn right")
        
        if angle != prevAngle:
            if lTurn or rTurn: 
              if (rightArea > exitThresh and rTurn) or (leftArea > exitThresh and lTurn): 
                  lTurn = False 
                  rTurn = False

                  prevDiff = 0 
                  if lDetected: 
                      t += 1
                      lDetected = False

              #oh turned too far too far
              elif lTurn:
                  angle = max(angle, sharpLeft)
              elif rTurn: 
                  angle = min(angle, sharpRight)
              write("servo", angle)
              time.sleep(0.1)
            else:
                write("servo", max(min(angle, sharpLeft), sharpRight))
                time.sleep(0.1)
        print(angle)
        #reeset
        prevDiff = aDiff

        prevAngle = angle
        
        #if we are done 12 turns (3 laps)
        if t == 12:
            sleep(2)
            stop() 
            break
        if debug:
            if cv2.waitKey(1)==ord('q'):
                stop() 
                break
            displayROI()
            cv2.imshow("finalColor", img)

    if debug: 
        cv2.destroyAllWindows()
#poop isgma ohio