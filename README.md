✾ *Engineering Documentation* ✾

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ 

## Table of Contents
  A list of things in this readme file

+ **Repository Contents**
+ **Robot Mechanical Design**
+ **Open Challenge Strategy**
+ **Obstacle Challenge Strategy**
+ **Parts List**

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

## Respository Contents
  Contents of the full repository

 [Schemes] | This folder contains the schematic for the vehicle 

 [SRC] | Programming and software is housed here 

 [T-Photos] | Misc. photos can be seen here 

 [V-Photos] | Photos of the vehicle from all required sides can be seen here 

 [Video] | Youtube link is here for you to watch our average working day 

 [Other] | Other materials or documentation regarding our vehicle 

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

## Robot Design
The vehicle is a modified [model name omitted]. We removed the cover, front and rear bumpers, additional lights, and the suspension system from the original chassis. Metal cut parts were then used to create a new base, which also facilitated the mounting of electronics. The original ESC and motor were replaced with new components sourced from [supplier name omitted].

The robot is primarily controlled by a Raspberry Pi and an extension board. The Raspberry Pi manages both the DC and servo motors, which govern movement and steering through pulse-width modulation (PWM). Additionally, it interfaces with the camera and processes image data to guide the vehicle based on a coded detection system, ensuring the robot navigates accurately.

## Software Design
The Raspberry Pi, functioning as the core control unit, operates using Python. It leverages the camera to determine vehicle movement by analyzing each frame for wall positions relative to the robot. This process is adapted based on the specific challenge the robot is addressing. Once movement decisions are made, a PID controller calculates the most efficient trajectory. The PID controller helps to minimize errors by adjusting the steering angle according to proportional, integral, and derivative terms. The robot also identifies turning points by detecting an orange line, which is selected for its visibility. When the orange line is detected within a predefined region, it registers a "turn." The system tracks these turns, where a count of four turns equates to one lap, and continues this process to complete the required course.
## ✧ Open Challenge Strategy ✧
This script is designed to use computer vision to allow the robot to adjust its orientation. The program begins by setting up the camera and motor configurations, and initializing the camera to capture images and centering the wheels. Afterwards, the script creates a function to draw regions of interest (ROIs) based on the captured images and another function to command the servo and DC motors. The primary loop processes camera frames to detect contours and regions with specific colors, adjusting the robot's steering angle using a PID controller to maintain a path based on detected areas.

In its operation, the robot captures images and processes them to detect black and orange areas, which are used to guide its movement. By analyzing the size of detected contours within predefined ROIs, the robot adjusts its steering angle and direction to navigate the environment. The ultimate goal is to complete a series of turns while avoiding obstacles and maintaining the correct trajectory. The script includes a debugging mode to visualize the robot's view and ROIs, and it stops the robot after completing a set number of turns or when a manual stop command is issued.
  Here is an example:

  (Photo 1)

  ^The robot sees that there is more wall in the left box than the right


  (Photo 2)

  ^The robot begins to turn to compensate


  (Photo 3)

  ^Hooray, robot is nice and straight!
##  Obstacle Challenge strategy

Our obstacle challenge shares significant similarities with the open challenge, with only a few key differences. The primary distinction is the additional stage in the color filtering process, designed to address the presence of obstacles such as pillars on the course. Specifically, the system is now configured to recognize and differentiate between red and green pillars, which requires an enhanced color filtering algorithm. This adaptation ensures that the robot can accurately detect and navigate around these new obstacles, thereby improving its ability to complete the course effectively. The integration of these additional color filters enhances the robot's situational awareness and obstacle avoidance capabilities, which are crucial for navigating the more complex environment of the obstacle challenge.
    
##  Parts List 
update this from the google classroom or else we are cooked!!

+ TRA97074-1 Traxxas TRX-4M Ford Bronco 1/18 RTR 4X4 Trail Truck, White | [Link](https://www.bigboyswithcooltoys.ca/products/tra97074-1-traxxas-trx-4m-ford-bronco-1-18-rtr-4x4-trail-truck-white)
+ Lego Mindstorm Ev3 Core Set | [Link](https://www.amazon.com/Lego-Mindstorm-Ev3-Core-45544/dp/B00DEA55Z8)
+ Super Start Kit UNO R3 Project | [Link](https://www.amazon.ca/Elegoo-Project-Starter-Tutorial-Arduino/dp/B01D8KOZF4)
+ Raspberry Pi 4B | [Link](https://www.pishop.ca/product/raspberry-pi-4-model-b-2gb/?src=raspberrypi)
+ Double Switches
+ Hot Glue + Hot glue gun
+ Raspberry Pi FIsheye Camera | [Link](https://www.amazon.com/Raspberry-Camera-Module-160FOV-Fisheye/dp/B083XMGSVP/ref=sr_1_3?keywords=raspberry%2Bpi%2Bwide%2Bangle%2Bcamera&qid=1680461882&sr=8-3&th=1)
