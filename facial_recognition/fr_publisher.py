import paho.mqtt.client as mqttClient
import time

#txt= input("Please enter 1 or 0")
number = 1


def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
 
broker_address= "tailor.cloudmqtt.com"
port = 15628
user = "jswnyenq"
password = "UPt8dPRCjneU"
 
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)     
 
client.loop_start()        
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)

try:
    while True:

        value = input("Please write 1 or 0:")

        if value == "1":
            client.publish("camera/face_recog","Movement detected!")
        else:
            client.publish("camera/face_recog","NO movement detected")

 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
