x# ꕤ✿✧ *Engineering Documentation* ✧✿ꕤ

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Documentation

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

 [Schemes](https://github.com/kylln20/WRO-2022-23/tree/main/schemes) | This folder contains the schematic for the vehicle 

 [SRC](https://github.com/kylln20/WRO-2022-23/tree/main/src) | Programming and software is housed here 

 [T-Photos](https://github.com/kylln20/WRO-2022-23/tree/main/t-photos) | Team member photos can be seen here 

 [V-Photos](https://github.com/kylln20/WRO-2022-23/tree/main/v-photos) | Photos of the vehicle from all required sides can be seen here 

 [Video](https://github.com/kylln20/WRO-2022-23/tree/main/video) | Youtube link is here for you to watch our average working day 

 [Other](https://github.com/kylln20/WRO-2022-23/tree/main/other) | Other materials or documentation regarding our vehicle 

‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
##  Robot Design 
  The vehicle is a modded (I forgot the name). We removed the cover, front and back bumper, extra lights, and the suspension mechanism from the base car, and we used metal cut parts to replace and to serve as a base and help mount the electronics. The original ESC and motor have been replaced with a different ESC and motor we bought from (I forgor).
  The robot works using its brain; the Raspberry pi and the extension board. The Raspberry Pi has control over the DC and servo motor which control the movement and steering using pulse-width-modulation (PWM). The raspberry pi has control over our camera and turns based off the detection system we have coded, these signals help steer the vehicle in the right direction.
## ✧ Software Design ✧
  Because our vehicle functions with both a Raspberry Pi and Arduino board, our code runs on two seperate languages. With the Arduino IDE software we coded our arduino board in c++ to take commands from the Raspberry Pi, these commands will dictate the Servo and Dc motor's movement and thus the vehichle's movement. As the main brain of our vehicle, the Raspberry Pi runs on python and works by using its camera to dictate how the vehicle should move.
## ✧ Design choies ✧
  Using the base of the traxxas, our first plan consisted of a fully 3d printed design using it as a chasis. 3D printing was hard to come by so we ended up mixing a bunch of materials together. We still use a 2d pirnted base but instead we have adhesives and glues to stick it and our lego parts together.
## ✧ Open Challenge Strategy ✧
  For the Open Challenge, we decided to take frames recorded from our camera and filter out so the black walls were highlighted. We then use regions of interest to help wall-follow and to help determine when to turn. With a PD following system we can fine tune the driving and turning so that our vehicle wll procede smoothly.
## ✧ Obstacle Challenge strategy ✧
    NA?

## ✧ Parts List ✧
+ TRA97074-1 Traxxas TRX-4M Ford Bronco 1/18 RTR 4X4 Trail Truck, White | [Link](https://www.bigboyswithcooltoys.ca/products/tra97074-1-traxxas-trx-4m-ford-bronco-1-18-rtr-4x4-trail-truck-white)
+ Lego Mindstorm Ev3 Core Set | [Link](https://www.amazon.com/Lego-Mindstorm-Ev3-Core-45544/dp/B00DEA55Z8)
+ Super Start Kit UNO R3 Project | [Link](https://www.amazon.ca/Elegoo-Project-Starter-Tutorial-Arduino/dp/B01D8KOZF4)
+ Raspberry Pi 4B | [Link](https://www.pishop.ca/product/raspberry-pi-4-model-b-2gb/?src=raspberrypi)
+ Double Switches
+ Hot Glue + Hot glue gun
+ Raspberry Pi FIsheye Camera | [Link](https://www.amazon.com/Raspberry-Camera-Module-160FOV-Fisheye/dp/B083XMGSVP/ref=sr_1_3?keywords=raspberry%2Bpi%2Bwide%2Bangle%2Bcamera&qid=1680461882&sr=8-3&th=1)
