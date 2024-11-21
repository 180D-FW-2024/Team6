import IMU_mag_util as IMU
import time
import datetime
import signal
import sys


doorIsOpen = False
doorIsMoving = False
closedDoorHeading = 0
openThresholdAngle = 5

# Used to clean up when Ctrl-c is pressed
def signalHandler(sig, frame):
    # GPIO.cleanup()
    print("Exiting...")
    sys.exit(0)

# Calibrate the magnetometer and get the heading of the closed door
def calibrateDoorPosition():
    IMU.calibrateIMU()  # determine min/max magnetometer readings

    print("Now please close the door.")
    time.sleep(5)

    closedHeading = IMU.getHeading(50)  # get heading of closed position
    return closedHeading

# Calculate <samples> angles and check if the median exceeds the threshold angle
def checkDoorOpen(samples):
    curHeading = IMU.getHeading(samples)
    print(f"(Heading: {curHeading})\n")

    # be careful of wrap around
    angleBtwn = max(curHeading, closedDoorHeading) - min(curHeading, closedDoorHeading)
    otherAngleBtwn = 360 - angleBtwn

    return (min(angleBtwn, otherAngleBtwn) >= openThresholdAngle)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signalHandler)
    # For handling interrupts:
    # GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    # GPIO.setup(INTERRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(LED_PIN, GPIO.OUT)
    # GPIO.output(LED_PIN, 0)
    # GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=LEDnotification, bouncetime=300)


    # Initialize IMU and callibrate closed door position
    IMU.detectIMU()     #Detect if BerryIMU is connected
    IMU.initIMU()       #Initialise the magnetometer

    closedDoorHeading = calibrateDoorPosition()
    print(f"Closed heading: {closedDoorHeading}\n")
    

    doorSamples = 20    # num samples to use to determine door open/not
    checkDoorPeriod = 5    #num seconds to periodically check door position
    lastDoorCheck = datetime.datetime.now()

    # Event loop
    while True:
        #poll status (or callback to update on interrupt) to find if door is moving
        #just poll status register for now, can set up interrupts later

        # print(f"cfx: %d, cfy: %d\n", IMU.getCFangles())
        # doorIsMoving = IMU.checkTilt()

        if doorIsMoving or (datetime.datetime.now() - lastDoorCheck).seconds >= checkDoorPeriod:
            print("Checking door position...")
            doorIsOpen = checkDoorOpen(doorSamples)
            lastDoorCheck = datetime.datetime.now()

            if doorIsOpen:
                print("DOOR IS OPEN")
            else:
                print("DOOR IS CLOSED")

        time.sleep(0.1)   #simulate some other code happening
