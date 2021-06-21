Code to be run on raspberry

import RPi.GPIO as GPIO          
from time import sleep
from oscpy.server import OSCThreadServer
GPIO.setwarnings(False)
 
# Raspberry GPIO number and l298n connection
in1 = 27
in2 = 22
in3 = 23
in4 = 24
ena = 6
enb = 5
 
# Handles OSC communication with neuromore studio
osc = OSCThreadServer()
sock = osc.listen(address='raspberry IP', port=12345, default=True) # enter the raspberry pi IP in address
 
#initialising GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
 
p1=GPIO.PWM(ena,1000)
p2=GPIO.PWM(enb,1000)
p1.start(100)
p2.start(100)
 
def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
 
def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
 
def left():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
 
def right():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
 
def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
 
# Receives data from neuromore studio
@osc.address(b'/out/car')
def callback(values):
    if values == 1:
        print("Car moved")
        forward()
    else:
        print("Car stopped")
        stop()
