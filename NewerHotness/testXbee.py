
import serial
from struct import unpack
import os.path


PORT = 'COM5'
BAUD_RATE = 57600

# Safely open serial port
with serial.Serial(PORT, BAUD_RATE) as ser:
    fileName = "RecvData"
    i = 0
    # Name the file using the next available number to differentiate it
    # Checks to see if the next numbered filename already exists
    while os.path.isfile(fileName + str(i) + ".csv"):
        i = i + 1

    with open(fileName + str(i) + ".csv") as dataFile:
        # Continuously read and print packets
        while True:
            if ser.inWaiting() >= 52:
                response = ser.read(52)
                temp1, temp2, temp3, temp10dof, alt_press, alt_strat, \
                  alt_gps, lat, lon, accx, accy, accz, flags, \
                  pad = unpack('fffffiffffffhh', response)
                print("Temp: ", temp1 , "accel: ", accx)
                dataFile.write(",".join(map(str, [temp1, temp2, temp3, \
                  temp10dof, alt_press, alt_strat, alt_gps, lat, lon, accx, \
                  accy, accz, flags])) + "\n")
