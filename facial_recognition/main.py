import RPi.GPIO as GPIO
import time
import sys
import os
import faceRecognition as faceRecognition
#GPIO.setmode(GPIO.BOARD) #to use the physical pin number
GPIO.setmode(GPIO.BCM) #use the pin's channel number
gpioPin = 7 #Define the pin to be used

print ("PIR Module Test (CTRL-C to exit)")
 
GPIO.setup(gpioPin,GPIO.IN) # Set pin as input
Current_State  = 0
Previous_State = 0
try:
 
  print ("Waiting for sensor to settle ...")
 
  # Loop until sensor output is 0
  while GPIO.input(gpioPin)==1:
    Current_State  = 0
 
  print ("The sensor is on and ready")
 
  # Loop until user quits using CTRL+C
  while True :
 
    Current_State = GPIO.input(gpioPin)     # Read sensor state
 
    if Current_State==1 and Previous_State==0:
      print ("Motion detected!")       # sensor is triggered
      faceRecognition.main()       #run face Recognition to id the user
      Previous_State=1       # Record previous state
    elif Current_State==0 and Previous_State==1:
      print ("The sensor is on and ready again")      # sensor returned to ready state
      Previous_State=0
      time.sleep(0.05)     # Wait for 5 millisecond

except KeyboardInterrupt:
    print("\Exit")
    GPIO.cleanup()
    sys.exit(0)