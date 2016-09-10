#from xbee import XBee
import serial

PORT = 'COM5'
BAUD_RATE = 57600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
#xbee = XBee(ser)

# Continuously read and print packets
while True:
    try:
        #response = xbee.wait_read_frame()
        if(ser.inWaiting() >= 52):
            response = ser.read(52)
            print response
    except KeyboardInterrupt:
        break
        
ser.close()
