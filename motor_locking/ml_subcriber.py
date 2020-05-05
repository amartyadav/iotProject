import RPi.GPIO as GPIO
import json
import paho.mqtt.client as mqttClient
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True

    else:
        print("Connection failed")


# subscribition to the topic and receiving if the user is successfully recognised or not
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Message received:", data)

    observation = json.loads(data)
    result = observation["hasResult"]
    value = result["value"]

    cmsg = value
    unlock_door(cmsg)


def unlock_door(cmsg):
    # assuming the motor is connected to pins GPIO 04 (Pin 7), GPIO 17 (Pin 11), GPIO 27 (Pin 13), and GPIO 22 (Pin 15).
    # the below code would work after receiving the data from the mqtt broker whether or not to run the motor(lock and
    # unlock) the door.

    GPIO.setmode(GPIO.BOARD)
    control_pins = [7, 11, 13, 15]

    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    halfstep_seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    # if user successfully recognised, then unlock the door by moving the motor.
    if cmsg == 1:
        for i in range(512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.001)
    else:
        print("User not recognised. Access denied")
    GPIO.cleanup()



Connected = False

broker_address = "tailor.cloudmqtt.com"
port = 15628
user = "jswnyenq"
password = "UPt8dPRCjneU"

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)
    client.subscribe("camera/face_recog")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
