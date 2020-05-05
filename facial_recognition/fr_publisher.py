import paho.mqtt.client as mqttClient
import time

myGlobalMessagePayload = ''

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")

#subscribition to the topic 
def on_message(client, userdata, message):
    global myGlobalMessagePayload             #create global varaible to store value
    if message.topic == "sensor/movement" :
        myGlobalMessagePayload = message.payload
        print ("Message received:" ,str(message.payload.decode("utf-8")))

print (myGlobalMessagePayload)
 
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

        if myGlobalMessagePayload == "Movement detected!":
            client.publish("camera/face_recog","Unlock!")
        else:
            client.publish("camera/face_recog","Nothing")

 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
