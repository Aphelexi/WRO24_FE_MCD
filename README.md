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

 [Schemes]| This folder contains the schematic for the vehicle 

 [SRC] | Programming and software is housed here 

 [T-Photos] | Misc. photos can be seen here 

 [V-Photos]| Photos of the vehicle from all required sides can be seen here 

 [Video]| Youtube link is here for you to watch our average working day 

 [Other] | Other materials or documentation regarding our vehicle 

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
##  Robot Design 
  The vehicle is a modded (I forgot the name). We removed the cover, front and back bumper, extra lights, and the suspension mechanism from the base car, and we used metal cut parts to replace and to serve as a base and help mount the electronics. The original ESC and motor have been replaced with a different ESC and motor we bought from (I forgor).
  The robot works using its brain; the Raspberry pi and the extension board. The Raspberry Pi has control over the DC and servo motor which control the movement and steering using pulse-width-modulation (PWM). The raspberry pi has control over our camera and turns based off the detection system we have coded, these signals help steer the vehicle in the right direction.
## Software Design
  As the main brain of our vehicle, the Raspberry Pi runs on python and works by using its camera to dictate how the vehicle should move. (this entire section is just infinite yapping jutsu which i will do later)
## ✧ Open Challenge Strategy ✧
  During the Open Challenge, we take every frame recorded from the camera and filter for the black walls. Next, we draw boxes on specific locations in the frame. These boxes are used to determine if the robot is on a slant, done by measuring the pixels of "wall" inside the box. after this segment runs, we use PID Encoder to adjust the robot's orientation.

  Here is an example:

  (Photo 1)

  ^The robot sees that there is more wall in the left box than the right


  (Photo 2)

  ^The robot begins to turn to compensate


  (Photo 3)

  ^Hooray, robot is nice and straight!
##  Obstacle Challenge strategy 
    im not gonn lie i dont think were finishing this

##  Parts List 
update this from the google classroom

+ TRA97074-1 Traxxas TRX-4M Ford Bronco 1/18 RTR 4X4 Trail Truck, White | [Link](https://www.bigboyswithcooltoys.ca/products/tra97074-1-traxxas-trx-4m-ford-bronco-1-18-rtr-4x4-trail-truck-white)
+ Lego Mindstorm Ev3 Core Set | [Link](https://www.amazon.com/Lego-Mindstorm-Ev3-Core-45544/dp/B00DEA55Z8)
+ Super Start Kit UNO R3 Project | [Link](https://www.amazon.ca/Elegoo-Project-Starter-Tutorial-Arduino/dp/B01D8KOZF4)
+ Raspberry Pi 4B | [Link](https://www.pishop.ca/product/raspberry-pi-4-model-b-2gb/?src=raspberrypi)
+ Double Switches
+ Hot Glue + Hot glue gun
+ Raspberry Pi FIsheye Camera | [Link](https://www.amazon.com/Raspberry-Camera-Module-160FOV-Fisheye/dp/B083XMGSVP/ref=sr_1_3?keywords=raspberry%2Bpi%2Bwide%2Bangle%2Bcamera&qid=1680461882&sr=8-3&th=1)
