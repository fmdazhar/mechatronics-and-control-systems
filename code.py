#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO #Import GPIO library
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup() # programming the GPIO by BCM pin numbers

servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz


# set trigger and echo pins for the ultrasonic sensor
TRIG1 = 18
ECHO1 = 24
TRIG2=  19
ECHO2=  26
 
motor1_1 = 5
motor1_2 = 6
motor2_1 = 20
motor2_2 = 21
 
# setup for Ultrasonic sensor
GPIO.setup(TRIG1,GPIO.OUT) # initialize GPIO Pin as outputs
GPIO.setup(ECHO1,GPIO.IN) # initialize GPIO Pin as input
GPIO.setup(TRIG2,GPIO.OUT) # initialize GPIO Pin as outputs
GPIO.setup(ECHO2,GPIO.IN) # initialize GPIO Pin as input
# setup for motors
GPIO.setup(motor1_1, GPIO.OUT)
GPIO.setup(motor1_2, GPIO.OUT)
GPIO.setup(motor2_1, GPIO.OUT)
GPIO.setup(motor2_2, GPIO.OUT)

 
# Defining functions for the motor.
 
def stop():
    GPIO.output(motor1_1,0)
    GPIO.output(motor1_2,0)
    GPIO.output(motor2_1,0)
    GPIO.output(motor2_2,0) 

def forward():
    print("Forward")
    GPIO.output(motor1_1,1)
    GPIO.output(motor1_2,0)
    GPIO.output(motor2_1,1)
    GPIO.output(motor2_2,0)
 
def back():
    print("Back")
    GPIO.output(motor1_1,0)
    GPIO.output(motor1_2,1)
    GPIO.output(motor2_1,0)
    GPIO.output(motor2_2,1) 
 
def left():
    print("Left")
    GPIO.output(motor1_1,0)
    GPIO.output(motor1_2,0)
    GPIO.output(motor2_1,1)
    GPIO.output(motor2_2,0)  
 
def right():
    print("Right")
    GPIO.output(motor1_1,1)
    GPIO.output(motor1_2,0)
    GPIO.output(motor2_1,0)
    GPIO.output(motor2_2,0)

def SetAngle(angle):
    duty = ((angle/180.0) + 1.0) * 5.0
    p.ChangeDutyCycle(duty)
    time.sleep(0.5)
    p.ChangeDutyCycle(0)
    time.sleep(0.5)

def distance(GPIO_TRIGGER,GPIO_ECHO):
	i=0
    for i in range(5):
		# set Trigger to HIGH
		GPIO.output(GPIO_TRIGGER, True)
	 
		# set Trigger after 0.01ms to LOW
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER, False)
	 
		StartTime = time.time()
		StopTime = time.time()
	 
		# save StartTime
		while GPIO.input(GPIO_ECHO) == 0:
			StartTime = time.time()
	 
		# save time of arrival
		while GPIO.input(GPIO_ECHO) == 1:
			StopTime = time.time()
	 
		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		dis = (TimeElapsed * 34300) / 2
		Distance=Distance+dis
		Distance=Distance/5
    print Distance
	return Distance


stop()
p.start(7.5)
SetAngle(90)
time.sleep(1.5)
payload=0
  
while True:
    avgDistance1=distance(TRIG1,ECHO1)  
    avgDistance2=distance(TRIG2,ECHO2)
    if (payload == 0 and avgDistance1<6):
        SetAngle(0) 
        payload = 1
    else:
        forward()
        if (avgDistance1 < 8 and payload == 1):
            if avgDistance2 < 10:
                right()
                time.sleep(0.5)
                stop()
            else:
                left()
                time.sleep(0.5)
                stop()