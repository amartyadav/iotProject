def main():
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
     
    broker_address= "tailor.cloudmqtt.com"
    port = 15628
    user = "jswnyenq"
    password = "UPt8dPRCjneU"
     
    client = mqttClient.Client("Python07")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password
    client.on_connect= on_connect                      #attach function to callback
    client.connect(broker_address, port=port) 
    client.publish("camera/face_recog", "1");
    print("A message has been published")
    client.disconnect();

