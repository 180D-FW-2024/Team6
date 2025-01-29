# Selected initialization functions, angle calucations, and constants from
# https://github.com/ozzmaker/BerryIMU/blob/master/python-BerryIMU-gyro-accel-compass-filters
# (which also includes Kalman filtering)

# IMU register mappings on spec sheet
# https://www.st.com/resource/en/datasheet/lis3mdl.pdf
# There are also various interrupt events that can be configured.
# Check the application notes
# https://www.st.com/en/mems-and-sensors/lis3mdl.html#documentation
# for more detail.

import smbus2 as smbus
import sys
import time
import datetime
import math

# For i2c with HW: use bus 1 (unreliable b/c of magnetometer clock stretching?)
# For i2c in SW(using overlay): use bus 3
bus = smbus.SMBus(3) 

# magnetometer registers
LIS3MDL_ADDRESS     = 0x1C
LIS3MDL_WHO_AM_I    = 0x0F
LIS3MDL_CTRL_REG1   = 0x20
LIS3MDL_CTRL_REG2   = 0x21
LIS3MDL_CTRL_REG3   = 0x22
LIS3MDL_OUT_X_L     = 0x28
LIS3MDL_OUT_X_H     = 0x29
LIS3MDL_OUT_Y_L     = 0x2A
LIS3MDL_OUT_Y_H     = 0x2B
LIS3MDL_OUT_Z_L     = 0x2C
LIS3MDL_OUT_Z_H     = 0x2D


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
MAG_LPF_FACTOR = 0.4        # Low pass filter constant magnetometer
MAG_MEDIANTABLESIZE = 9     # Median filter table size for magnetometer. Higher = smoother but a longer delay


# for calibration -- run calibrate() and open the door fully
magXmin =  32767
magYmin =  32767
magZmin =  32767
magXmax =  -32767
magYmax =  -32767
magZmax =  -32767


def detectIMU():
    try:
        #Check for BerryIMUv3 (LIS3MDL(magnetometer) only)
        #If no LSM6DSL or LIS3MDL is connected, there will be an I2C bus error and the program will exit.
        LIS3MDL_WHO_AM_I_response = (bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_WHO_AM_I))
    except IOError as f:
        print('IMU not detected')
        sys.exit()
    else:
        if (LIS3MDL_WHO_AM_I_response == 0x3D):
            print("Found BerryIMUv3 (LIS3MDL)")
    time.sleep(1)


def readMAGx():
    mag_l = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_X_L)
    mag_h = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_X_H)
    mag_combined = (mag_l | mag_h <<8)
    return mag_combined  if mag_combined < 32768 else mag_combined - 65536

def readMAGy():
    mag_l = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_Y_L)
    mag_h = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_Y_H)
    mag_combined = (mag_l | mag_h <<8)
    return mag_combined  if mag_combined < 32768 else mag_combined - 65536

def readMAGz():
    mag_l = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_Z_L)
    mag_h = bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_OUT_Z_H)
    mag_combined = (mag_l | mag_h <<8)
    return mag_combined  if mag_combined < 32768 else mag_combined - 65536

# To write to a register
def writeByte(device_address,register,value):
    bus.write_byte_data(device_address, register, value)

# To read from a register
def readByte(device_address,register):
    return bus.read_byte_data(device_address, register)

# Initialize magnetometer and interrupt detection
def initIMU():
    # refer to spec sheet about control registers
    #initialise the magnetometer
    writeByte(LIS3MDL_ADDRESS,LIS3MDL_CTRL_REG1, 0b01011100)         # High performance, ODR 80 Hz, FAST ODR disabled and Selft test disabled.
    writeByte(LIS3MDL_ADDRESS,LIS3MDL_CTRL_REG2, 0b00100000)         # +/- 8 gauss
    writeByte(LIS3MDL_ADDRESS,LIS3MDL_CTRL_REG3, 0b00000000)         # Continuous-conversion mode

# Determine range of mag values for each axis over the range of motion
def calibrateIMU():
    global magXmin, magXmax, magYmin, magYmax, magZmin, magZmax
    rawmagXmin =  32767
    rawmagYmin =  32767
    rawmagZmin =  32767
    rawmagXmax =  -32767
    rawmagYmax =  -32767
    rawmagZmax =  -32767
    print('Open the door as far as possible over five seconds.')
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 5:
        magX = readMAGx()
        magY = readMAGy()
        magZ = readMAGz()
        rawmagXmin = min(rawmagXmin, magX)
        rawmagYmin = min(rawmagYmin, magY)
        rawmagZmin = min(rawmagZmin, magZ)
        rawmagXmax = max(rawmagXmax, magX)
        rawmagYmax = max(rawmagYmax, magY)
        rawmagZmax = max(rawmagZmax, magZ)
        # time.sleep(0.25 /1e6) # ** not sure if necessary
    magXmax = rawmagXmax
    magYmax = rawmagYmax
    magZmax = rawmagZmax
    magXmin = rawmagXmin
    magYmin = rawmagYmin
    magZmin = rawmagZmin
    print('Calibration complete.')

# Calculate the heading over n samples (multiple samples required for filters)
def getHeading(samples):
    samples = max(samples, 2*MAG_MEDIANTABLESIZE)
    
    #Setup the tables for the median filter. Fill them all with '1' so we dont get devide by zero error
    mag_medianTable1X = [1] * MAG_MEDIANTABLESIZE
    mag_medianTable1Y = [1] * MAG_MEDIANTABLESIZE
    mag_medianTable1Z = [1] * MAG_MEDIANTABLESIZE
    mag_medianTable2X = [1] * MAG_MEDIANTABLESIZE
    mag_medianTable2Y = [1] * MAG_MEDIANTABLESIZE
    mag_medianTable2Z = [1] * MAG_MEDIANTABLESIZE

    oldXMagRawValue = 0
    oldYMagRawValue = 0
    oldZMagRawValue = 0
    
    headings = (samples - MAG_MEDIANTABLESIZE) * [0]
    for i in range (0, samples):
        MAGx = readMAGx()
        MAGy = readMAGy()
        MAGz = readMAGz()

        # #Apply compass calibration
        MAGx -= (magXmin + magXmax) /2
        MAGy -= (magYmin + magYmax) /2
        MAGz -= (magZmin + magZmax) /2

        ###############################################
        #### Apply low pass filter ####
        ###############################################
        MAGx =  MAGx  * MAG_LPF_FACTOR + oldXMagRawValue*(1 - MAG_LPF_FACTOR)
        MAGy =  MAGy  * MAG_LPF_FACTOR + oldYMagRawValue*(1 - MAG_LPF_FACTOR)
        MAGz =  MAGz  * MAG_LPF_FACTOR + oldZMagRawValue*(1 - MAG_LPF_FACTOR)

        oldXMagRawValue = MAGx
        oldYMagRawValue = MAGy
        oldZMagRawValue = MAGz

        #########################################
        #### Median filter for magnetometer ####
        #########################################
        # cycle the table
        for x in range (MAG_MEDIANTABLESIZE-1,0,-1 ):
            mag_medianTable1X[x] = mag_medianTable1X[x-1]
            mag_medianTable1Y[x] = mag_medianTable1Y[x-1]
            mag_medianTable1Z[x] = mag_medianTable1Z[x-1]

        # Insert the latest values
        mag_medianTable1X[0] = MAGx
        mag_medianTable1Y[0] = MAGy
        mag_medianTable1Z[0] = MAGz

        # Copy the tables
        mag_medianTable2X = mag_medianTable1X[:]
        mag_medianTable2Y = mag_medianTable1Y[:]
        mag_medianTable2Z = mag_medianTable1Z[:]

        # Sort table 2
        mag_medianTable2X.sort()
        mag_medianTable2Y.sort()
        mag_medianTable2Z.sort()

        # The middle value is the value we are interested in
        MAGx = mag_medianTable2X[int(MAG_MEDIANTABLESIZE/2)]
        MAGy = mag_medianTable2Y[int(MAG_MEDIANTABLESIZE/2)]
        MAGz = mag_medianTable2Z[int(MAG_MEDIANTABLESIZE/2)]

        #Calculate heading
        heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        #Only have our heading between 0 and 360
        if heading < 0:
            heading += 360
        
        if i>=MAG_MEDIANTABLESIZE:
            headings[i-MAG_MEDIANTABLESIZE] = heading

    # return median heading
    headings.sort()
    return headings[(samples - MAG_MEDIANTABLESIZE)//2]