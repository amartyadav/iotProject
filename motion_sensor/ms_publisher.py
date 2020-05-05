#import RPi.GPIO as GPIO
#import time

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#PIR_PIN = 23
#GPIO.setup(PIR_PIN, GPIO.IN)

import paho.mqtt.client as mqttClient
import time


 
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
 
broker_address = "tailor.cloudmqtt.com"
port = 15628
user ="jswnyenq"
password = "UPt8dPRCjneU"

client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:

        #if GPIO.input(PIR_PIN):
         #   client.publish("iot/sensor","Movement detected!")
          #else:
           #   client.publish("iot/sensor","NO movement detected")
        value = input("Please write 1 or 0:")

        if value == "1":
            client.publish("sensor/movement","Movement detected!")
        else:
            client.publish("sensor/movement","NO movement detected")
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()

