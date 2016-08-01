"""This is a program that reads the data from a strat that is sending out serial data
All it does is read and export the data, is is a stripped down version of xbeeParse
Mostly a testing program"""
import os
import binascii
import codecs
import serial
import re
import time
from customDebug import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np



fn = "XbeeDataDump02.log"
ser = "fakeSerial.txt"
i = 0
dataForamt = '/Data One:8^Data Two:8;'
ActualFormat = "/Data_One:242^Data_Two:242;\n/Data_One:243^Data_Two:243;'"
ENDBYTE = b';'

style.use('fivethirtyeight')
fig = plt.figure()
plt.ion()
ax1 = fig.add_subplot(1,1,1)

WINDOWS= False

def establishSerial(baud,selectComm=False):
    print('Opening Serial Port...')
    
    
    if selectComm:
        if not WINDOWS:
            print('Select comm port number: ')
            commPorts = [i.name for i in os.scandir('/dev') if str(i.name).startswith('tty.')]
            for i in commPorts: print(i)
            serialPath = '/dev/'+ commPorts[int(input('Comm port number: '))-1]
        else:
            print('maunally add comm port in establishSerial')
            exit()
        
    else:
        serialPath = '/dev/tty.usbserial-DA01IFE8'
    
    try:
        serialPort = serial.Serial(serialPath,baud,timeout=1)
        while True:
            if serialPort.isOpen():
                break
            else:
                time.sleep(0.5)
        print('Connected to serial port\n')
        return True,serialPort
    except:
        print('Could not connect to comm port, please check connections: ')
        return False,None

    


def main(): 
    report,serialPort = establishSerial(9600,selectComm=True)
    rawDataLine=[]
    


    i = 0
    if report:
        # Get serial data
        while True:
            try:
                if serialPort.inWaiting():
                    rawDataLine.append(serialPort.read())
                    if rawDataLine[-1] == b'\n':
                        dataLine = b''.join(rawDataLine)
                        print(dataLine)
                        
                        
                        
                        # sensors.updateY(toUpdate[0],toUpdate[1])
#
                        rawDataLine = []
            except KeyboardInterrupt:
                serialPort.close()
                if not serialPort.isOpen():
                    print(' Serial successfully closed')
                exit()
    pass

if __name__ == '__main__':
    main()
        
