def main():
    import cv2
    import numpy as np
    import RPi.GPIO as GPIO
    import time
    from datetime import datetime

    start = time.time()
    periodOfTime = 30 #30 secs
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #GPIO.setmode(GPIO.BOARD) #to use the physical pin number
    GPIO.setmode(GPIO.BCM) #use the pin's channel number
    gpioPin = 6 #Define the pin to be used
    GPIO.setup(gpioPin, GPIO.OUT) # Set pin as output
    GPIO.output(gpioPin, 0)


    #iniciate id counter
    id = 0

    # names related to the saved ids. Example, A: id=1, B: ID-2  etc...
    names = ['None', 'A', 'B', 'C', 'D'] 

    # Initialise and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognised as a face
    minWidht = 0.1*cam.get(3)
    minHeight = 0.1*cam.get(4)
    authorised = 0

    while True:

        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minWidht), int(minHeight)),
           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 70):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                authorised = 1
                GPIO.output(gpioPin, 1)
                successMsg = ("Success authorisation was given to " + str(id) + " at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     + " with confidence rate of" + confidence + "\n")
                with open("records.txt", "a") as records:
                    records.write(successMsg)
                print (successMsg)
                
                
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                GPIO.output(gpioPin, 0)
                failedMsg = ("A failed attempt was recorded at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ "\n")
                with open("records.txt", "a") as records:
                    records.write(failedMsg)
                print(failedMsg)
                time.sleep(5)

        cv2.imshow('camera',img)
        
        if (authorised == 1): break # Break if the open attempt is authorised
        if time.time() > start + periodOfTime : break # break after 30 secs anyway for security purposes
        k = cv2.waitKey(10) & 0xff
        if k == 27: break # break if 'ESC' was pressed


    #Cleanup
    print("cleaning up and exiting Program")
    cam.release()
    GPIO.cleanup(gpioPin)
    cv2.destroyAllWindows()



