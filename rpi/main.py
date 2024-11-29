import IMU_mag_util as IMU
import picamera
import requests
import RPi.GPIO as GPIO
import time
import datetime
import signal
import sys
import cv2
import numpy as np


doorIsOpen = False
closedDoorHeading = 0
openThresholdAngle = 10
server = None

SOLENOID_PIN = 23

# Used to clean up when Ctrl-c is pressed
def signalHandler(sig, frame):
    GPIO.cleanup()
    print("Exiting... to do some clean up later")
    camera.close()
    sys.exit(0)

# Calibrate the magnetometer and get the heading of the closed door
def calibrateDoorPosition():
    IMU.calibrateIMU()  # determine min/max magnetometer readings

    print("Now please close the door.")
    time.sleep(5)

    closedHeading = IMU.getHeading(50)  # get accurate heading of closed position
    return closedHeading

# Calculate <samples> angles and check if the median exceeds the threshold angle
def checkDoorOpen(samples):
    curHeading = IMU.getHeading(samples)
    print(f"(Heading: {curHeading})\n")
    # be careful of wrap around
    angleBtwn = max(curHeading, closedDoorHeading) - min(curHeading, closedDoorHeading)
    otherAngleBtwn = 360 - angleBtwn

    return (min(angleBtwn, otherAngleBtwn) >= openThresholdAngle)

# Return grayscale faces extracted from image
def extractFace(frame):
    extracted_faces = []
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.equalizeHist(gray_image) #adjust contrast
    # downsize the image to increase detector speed (slightly)
    shrunk_image = cv2.resize(gray_image, dsize=None, fx=0.5, fy=0.5) #shrink by half
    
    faces = face_cascade.detectMultiScale(
        shrunk_image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100), # min size of faces in pixels to detect
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
        extracted_faces.append(gray_image[2*y:2*(y+h), 2*x:2*(x+w)])
        # extracted_faces.append

    return extracted_faces, faces

# If faces found, save to file and return the file names as a list
# Else, return an empty list
def detectFaces(path):
    paths = []
    # capture image to np array, in bgr encoding for opencv
    # make sure the buffer dim are multiples of 32
    frame = np.empty((1088 * 1920 * 3), dtype=np.uint8)
    camera.capture(frame, 'bgr')
    frame = frame.reshape((1088, 1920, 3))
    frame = frame[:1080, :1920, :]

    extracted_faces, _ = extractFace(frame)
    print(f"face count: {len(extracted_faces)}")
    
    for i in range(len(extracted_faces)):   # how should we handle multiple people?
        # save as path/face_#.jpg
        cv2.imwrite(path + "/face_" + str(i) + ".jpg", extracted_faces[i])
        paths.append(str(path + "/face_" + str(i) + ".jpg"))
    return paths

# Query server and return bool if door should unlock(true)/lock(false)
def checkServerUnlock():
    r = requests.get(server+'/getunlocked')
    data = r.json()
    if data['door_unlocked']:
        print("Server says UNLOCK")
    else:
        print("Server says LOCK")
    return data['door_unlocked']


if __name__ == '__main__':
    GPIO.cleanup()
    server = sys.argv[1]
    signal.signal(signal.SIGINT, signalHandler)
    # Ex for handling interrupts:
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    # GPIO.setup(INTERRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    GPIO.output(SOLENOID_PIN, 1) # 0 or 1 for high/low
    # GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=LEDnotification, bouncetime=300)

    

    # Initialize camera
    camera = picamera.PiCamera()
    camera.resolution = (1920, 1080)
    camera.exposure_mode='sports' #supposedly reduces motion blur
    time.sleep(2)   #to adjust inital gain and exposure time (auto-adjusts by default)

    face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

    # Initialize IMU and callibrate closed door position
    IMU.detectIMU()     # Detect if BerryIMU is connected
    IMU.initIMU()       # Initialise the magnetometer
   
    closedDoorHeading = calibrateDoorPosition()
    print(f"Closed heading: {closedDoorHeading}\n")

    doorSamples = 20    # num samples to use to determine door open/not
    checkDoorPeriod = 10    # num seconds to periodically check door position
    lastDoorCheck = datetime.datetime.now()

    # Event loop
    while True:
        #poll status (or callback to update on interrupt) to find if door is moving
        #just periodically compute heading, can set up interrupts later

        # Check door position periodically
        if (datetime.datetime.now() - lastDoorCheck).seconds >= checkDoorPeriod:
            print("Checking door position...")
            doorIsOpen = checkDoorOpen(doorSamples)
            lastDoorCheck = datetime.datetime.now()

            if doorIsOpen:
                print("DOOR IS OPEN")
            else:
                print("DOOR IS CLOSED")
            # Notify server (blocking)
            r = requests.post(server+'/receiveposition', data={'position':'unlocked' if doorIsOpen else 'locked'})
            print(r)
        
        # Check if face detected as often as possible
        faceFiles = detectFaces("detected_faces")
        print(faceFiles)
        for faceFile in faceFiles:
            r = requests.post(server+'/receive', files={'image': open(faceFile, "rb")})
            print(r)
            time.sleep(1) # remove later

        # query server if door should open or not
        GPIO.output(SOLENOID_PIN, 0 if checkServerUnlock() else 1)

        # time.sleep(0.1)   #simulate some other code happening
