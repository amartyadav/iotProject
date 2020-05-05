
import paho.mqtt.client as mqttClient
import time

myGlobalMessagePayload = ''

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True

    else:
        print("Connection failed")

def on_message(client, userdata, message):
    global myGlobalMessagePayload
    if message.topic == "sensor/movement" :
        myGlobalMessagePayload = message.payload
        print ("Message received:" ,str(message.payload.decode("utf-8")))

print (myGlobalMessagePayload)

Connected = False

broker_address = "tailor.cloudmqtt.com"
port = 15628
user = "jswnyenq"
password = "UPt8dPRCjneU"

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect= on_connect
client.on_message= on_message

client.connect(broker_address, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)
    client.subscribe("sensor/movement")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
