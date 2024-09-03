import cv2
import sys
sys.path.append('/home/pi/TurboPi/')
from picamera2 import Picamera2
import libcamera
import time
import RPi.GPIO as GPIO
import numpy as np
import HiwonderSDK.Board as Board
import math

#set speed
def write(value):

    if 180 > value > 0:
        pulseWidth = int(11.1*value+500)
        Board.setPWMServoPulse(1, pulseWidth, 1)

    elif 2000 > value > 1000:
        Board.setPWMServoPulse(5, value, 100)

#read the name roi=region of intrest
def display_roi(color):
    for ROI in ROIs: 
        image = cv2.line(img, (ROI[0], ROI[1]), (ROI[2], ROI[1]), color, 4)
        image = cv2.line(img, (ROI[0], ROI[1]), (ROI[0], ROI[3]), color, 4)
        image = cv2.line(img, (ROI[2], ROI[3]), (ROI[2], ROI[1]), color, 4)
        image = cv2.line(img, (ROI[2], ROI[3]), (ROI[0], ROI[3]), color, 4)



#read name
def stop_car():

    write(87)
    write(1500)

    cv2.destroyAllWindows()

#find contour in roi
def contours(hsvRange, ROI): 
    lower_mask = np.array(hsvRange[0])
    upper_mask = np.array(hsvRange[1])

    mask = cv2.inRange(img_hsv, lower_mask, upper_mask)

    kernel = np.ones((7, 7), np.uint8)

    eMask = cv2.erode(mask, kernel, iterations=1)
    dMask = cv2.dilate(eMask, kernel, iterations=1)

    contours = cv2.findContours(dMask[ROI[1]:ROI[3], ROI[0]:ROI[2]], cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]

    return contours

#finds biggest contour
def max_contour(contours): 
    maxArea = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        maxArea = max(area, maxArea)

    return maxArea

#write to multiple threads
def multi_write(sequence):

    for action in sequence: 

        #delay commands
        if action < sharpRight: 
            time.sleep(action)
        else: 
            write(action)

if __name__ == '__main__':

    time.sleep(3)

    #initialize camera
    picam2 = Picamera2()

    picam2.set_controls({"AeEnable": True})
    picam2.preview_configuration.main.size = (640,480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 30
    picam2.preview_configuration.align()
    picam2.configure("preview")

    picam2.start()

    #turn by wall or pillar
    eTurnMethod = ""

    #read the name
    lapsComplete = False

    #target color for pillar
    redTarget = 110 
    greenTarget = 530

    #what was te last pillar the car passed
    lastTarget = 0

    #did we go the wrong way?
    reverse = False

    #so basically the code doesnt work so this is a bandaid fix
    tempR = False

    #did we turn?
    turnDir = "none" 

    #park right or left
    parkingR = False
    parkingL = False

    #stores a stop time 
    sTime = 0

    #how long do we stop time
    s = 0

    #park when no pillars (bandaid for niche case)
    tempParking = False

    #offset to where we stop
    endConst = 30

    #distance from pillar to the car
    pDist = 0

    #stores whether a pillar or no pillar was seen, true for if a pillar was seen, false for if no pillar was seen, blah, blah, blah
    tList = []

    #if car go back, no count as turn
    ignore = False
    prevIgnore = False

    #regions of interest
    ROI1 = [0, 165, 330, 255]
    ROI2 = [330, 165, 640, 255]
    ROI3 = [redTarget - 40, 110, greenTarget + 40, 335]
    ROI4 = [200, 250, 440, 300]

    ROIs = [ROI1, ROI2, ROI3, ROI4]

    #colors
    rBlack = [[0, 0, 0], [180, 255, 50]]
    rBlue = [[100, 100, 100], [135, 255, 255]]
    rRed = [[171, 175, 50], [180, 255, 255]]
    rGreen = [[58, 62, 55], [96, 255, 255]]
    rMagenta = [[160, 140, 50], [170, 255, 255]]
    rOrange = [[0, 100, 175], [25, 255, 255]]
    rWhite = [[0, 0, 150], [180, 28, 255]]

    #read the name
    lTurn = False
    rTurn = False

    #init kp and kd, for cases and stuff
    kp = 0.02
    kd = 0.01
    cKp = 0.2
    cKd = 0.2
    cy = 0.15

    straightConst = 87 #angle in which car goes straight
    exitThresh = 4000 #tells when the car is supposed to stop turning

    angle = 87 #current angle (default straight because sigma dennis)
    prevAngle = angle #for pid control
    tDeviation = 50 #max turning angle change
    sharpRight = straightConst - tDeviation
    sharpLeft = straightConst + tDeviation

    speed = 1650 #car speed
    reverseSpeed = 1340 #car speed, but backwards
    aDiff = 0 #dif of areas between contours
    prevDiff = 0 #pid numbers

    error = 0 #diff between pillar and target
    prevError = 0 #stores previous error

    cTarget = 0 #where the pillar should be
    contX = 0 #where the pillar is x axis
    contY = 0 #where the pillar is y axis
    pArea = 0 #so basically we need area because x and y axis is not enough

    #temp is used to make sure a three-point turn
    temp = False

    t = 0 #number of turns

    t2 = 0 #number of turns, backup (detects lines instead)
    
    tSignal = False #another backup to make sure that pillars didnt make a turn


    write(1500) # stop car to begin code

    time.sleep(8) #wait for code to begin
    

    #start button
    key2_pin = 16

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(key2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    #write initial values
    time.sleep(0.5)
    multi_write([angle, 0.5, 1670, 0.1, speed])

    #let the pain begin
    while True:
        #detect things
        #check if we are done laps
        if sTime != 0 and not lapsComplete:
            if time.time() - sTime > s:
                multi_write([1500, 2.5, 1680, 0.1, 1650])
                lapsComplete = True

        #reset variables so we can read areas again
        rightArea, leftArea, areaFront, areaFrontMagenta = 0, 0, 0, 0

        #get image
        img = picam2.capture_array()

        #funny color stuff (something about color encoding)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #read contour of wall and make image grey
        contours_left = contours(rBlack, ROI1)
        contours_right = contours(rBlack, ROI2)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #define black color in grey image
        ret, imgThresh = cv2.threshold(imgGray, 55, 255, cv2.THRESH_BINARY_INV)

        #parking using the location based off black in image
        contours_parking, hierarchy = cv2.findContours(imgThresh[ROI4[1]:ROI4[3], ROI4[0]:ROI4[2]], 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        #find biggest contour
        leftArea = max_contour(contours_left)
        rightArea = max_contour(contours_right)
        areaFront = max_contour(contours_parking)

        #find contours for pillars
        contours_red = contours(rRed, ROI3)
        contours_green = contours(rGreen, ROI3)
        contours_blue = contours(rBlue, ROI4)
        contours_orange = contours(rOrange, ROI4)

        # # number of red and green pillars
        num_pillars_g = 0
        num_pillars_r = 0

        #distance of the pillar
        pDist = 100000
        pArea = 0


        arr1 = [contours_green, contours_red]
        targets = [greenTarget, redTarget]

        ignore = False

        #iterate through both lists of contours
        for i in range(len(arr1)): 
            for x in range(len(arr1[i])):
                cnt = arr1[i][x]
                area = cv2.contourArea(cnt)

                if area > 100:

                    #get width, height, and x and y coordinates
                    approx=cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
                    x,y,w,h=cv2.boundingRect(approx)

                    #scale to image
                    x += ROI3[0] + w // 2 
                    y += ROI3[1] + h

                    #if the pillar is close enough add it to the number of pillars
                    temp_dist = round(math.dist([x, y], [320, 480]), 0)
                    if 160 < temp_dist < 380 : #395
                        if i == 0: 
                            num_pillars_g += 1
                        else: 
                            num_pillars_r += 1

                    #if too close, go back
                    if ((area > 6500 and ((x <= 420 and i == 0) or (x >= 220 and i == 1)))) and t < 13:

                        multi_write([straightConst, 0.1, 1500, 0.1, reverseSpeed, 0.5, speed])

                        if s != 0:
                            s += 1.5

                        ignore = True
                        if reverse == "turning" and turnDir == "right":
                            reverse = "done"
                            turnDir = "left"
                            t += 1

                    #deselects current pillar if its too close
                    if y > ROI3[3] - endConst or (temp_dist > 370 and t2 != 7) or (t2 == 7 and temp_dist > 380):
                        continue

                    #other cases i dont even know atp
                    if leftArea > 13000 or rightArea > 13000:
                        continue
                    if debug: cv2.rectangle(img,(x - w // 2, y - h),(x+ w // 2,y),(0,0,255),2)

                    if temp_dist < pDist:
                        pArea = area
                        contY = y
                        contX = x
                        cTarget = targets[i]
                        pDist = temp_dist


        #check if we are turning wide or short
        if (num_pillars_r >= 2 or num_pillars_g >= 2):


            endConst = 60

            cKp = 0.2 
            cKd = 0.2 
            cy = 0.05 

        #any other combination of number of pillars
        else:     

            endConst = 30

            cKp = 0.25
            cKd = 0.25 
            cy = 0.08 

        arr2 = [contours_orange, contours_blue]
        directions = ["right", "left"]

        #go through contours
        for i in range(len(arr2)): 
            for x in range(len(arr2[i])):

                cnt = arr2[i][x]
                area = cv2.contourArea(cnt)

                if area > 100:

                    #set the turn direction
                    if turnDir == "none":
                        turnDir = directions[i]

                    if turnDir == directions[i] and not parkingR and not parkingL:

                        if ignore == False and prevIgnore == True:
                            t -= 1
                            ignore = False
                        t2 = t

                        #check if we can 3 point turn
                        if t2 == 7:
                            ROI3 = [redTarget - 40, 90, greenTarget + 40, 335]
                            ROIs = [ROI1, ROI2, ROI3, ROI4]

                        if i == 0:
                            rTurn = True
                        else:
                            lTurn = True

        #reset numbers
        maxAreaL = 0 
        leftY = 0 
        maxAreaR = 0 
        rightY = 0 
        centerY = 0 
        # check if parking spot contours directly in front of car
        if t == 8 or tempParking:

            #find largest magenta contour
            contours_magenta_c = contours(rMagenta, ROI4)
            areaFrontMagenta = max_contour(contours_magenta_c)

            #turn left if wrong way
            if areaFrontMagenta > 500 and t == 8:
                angle = sharpLeft

        if tempParking:

            #things didnt work so we just gotta find anything we can
            contours_magenta_l = contours(rMagenta, ROI1)
            contours_magenta_r = contours(rMagenta, ROI2)

            info = [[0, 0, ROI1], [0, 0, ROI2], [0, 0, ROI4]]
            conts = [contours_magenta_l, contours_magenta_r, contours_magenta_c]

            #finds the largest magenta contour in the left, right, and centre + coordinates
            for i in range(len(conts)): 
                for x in range(len(conts[i])):
                    cnt = conts[i][x]
                    area = cv2.contourArea(cnt)

                    if area > 100:
                        approx=cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
                        x,y,w,h=cv2.boundingRect(approx)

                        x += info[i][2][0]
                        y += info[i][2][1] + h

                        #replace largest contour 
                        if area > info[i][0]:
                            info[i][0] = area
                            info[i][1] = y

            maxAreaL = info[0][0] 
            leftY = info[0][1]
            maxAreaR = info[1][0]
            rightY = info[1][1]
            centerY = info[2][1]

            #conditions for parking left
            if leftY >= 220 and maxAreaL > 100 and t2 >= 12:
                if not parkingL and not parkingR:
                    write(1640)
                    parkingL = True

                #readajust region of interest for parking
                ROI4 = [230, 250, 370, 300]
                ROIs = [ROI1, ROI2, ROI3, ROI4]

            #conditions for initiating parking on the right side
            if rightY >= 240 and maxAreaR > 100 and t2 >= 12:
                if not parkingL and not parkingR:

                    parkingR = True
                    write(1640)

                #readajust region of interest for parking
                ROI4 = [250, 250, 390, 300]
                ROIs = [ROI1, ROI2, ROI3, ROI4]

            if parkingR:

                #readajust by backing up if the parking lot is in front
                if centerY > 290:
                    multi_write([1500, 0.1, 1352, sharpLeft, 0.5, 1500])
                #turn right into parking lot
                else:
                    multi_write([1640, sharpRight])

            elif parkingL:

                #if car is too for left turn back to the right
                if rightArea > 8000 and maxAreaR > 2000:
                    multi_write([1640, sharpRight, 1])
                elif centerY > 290 and areaFront < 3000:
                    multi_write([1500, 0.1, 1352, sharpRight, 0.5, 1500])
                else:
                    multi_write([1640, sharpLeft])

            #check if we are in front of a wall and about to crash
            if areaFront > 3500:
                multi_write([straightConst, 0.2, 1640, 1])
                stop_car()
                break
            #if q is pressed break out of main loop and stop the car
            if cv2.waitKey(1)==ord('q'):
                stop_car() 
                break

            #display regions of interest
            display_roi((255, 204, 0))

            #display image
            cv2.imshow("finalColor", img)

            ##gMask = cv2.inRange(img_hsv, np.array(rGreen[0]), np.array(rGreen[1]))
            #cv2.imshow("Green Mask", gMask)

            #rMask = cv2.inRange(img_hsv, np.array(rRed[0]), np.array(rRed[1]))
            #cv2.imshow("Red Mask", rMask)

            pColour = "r" if lastTarget == redTarget else "g"
            if cTarget == redTarget: 
                cpColour = "r"
            elif cTarget == greenTarget:
                cpColour = "g"
            else:
                cpColour = "n"

            if rTurn:
                turn_status = "r"
            elif lTurn:
                turn_status = "l"
            else:
                turn_status = "n"

        # reset variables
        prevAngle = angle
        tSignal = False
        
        prevError = error
        contY = 0
        contX = 0
        cTarget = 0
        pArea = 0
        prevIgnore = ignore

        #safety if the turn counter kills itself
        if t == 13 and not tempParking:
            redTarget, greenTarget = (greenTarget, greenTarget) if turnDir == "right" else (redTarget, redTarget)
            tempParking = True

        time.sleep(0.1)

picam2.stop()
cv2.destroyAllWindows()
