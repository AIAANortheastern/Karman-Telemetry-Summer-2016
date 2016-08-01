"""
groundStating.py is the main data logging program created to decode the data streams
It reads from serial port, decodes the message, then live displays it

Current problems: The program can crash my computer (mac) if is recieves bad serial data
    -believe to be coming from updating the graph is a hugely cpu intensive process

To implement: 1) Fake serial stream that mimics what the downlink will consist of
                for testing purposes
            2) Save the data stream to external memory
            3) Configure serial port connection on windows (then a PI)
"""


import os
import binascii
import codecs
import serial
import re
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import atexit
# customDebug is a modal that I have created to help with debugging programs
# comment it out if you have not downloaded it, it is non-essential
# from customDebug import *

# Enable TEST_SERIAL
TESTSERIAL = False

fn = "XbeeDataDump02.log"
ser = "fakeSerial.txt"
i = 0
# These data format strings are just for refrence and testing
dataForamt = '/Data One:8^Data Two:8;'
ActualFormat = "/Data_One:242^Data_Two:242;\n/Data_One:243^Data_Two:243;'"
BinaryFormat = 'TcTcTc'

# Set this to a default serial port that you know for fast testing
DEFAULT_SERIAL_PORT = '/dev/tty.usbserial-DA01IFE8'
DELIMITER = "^"
ENDBYTE = b';'
STARTBYTE = "/"

# Initialization of the plot, was not sure how to do it locally, so used global vars
style.use('fivethirtyeight')
fig = plt.figure()
plt.ion()
ax1 = fig.add_subplot(1,1,1)



# plt.ion()
# ax1 = plt.axes()


# ani = animatopn.FuncAnimaton(fig,FUNCTION)


class sensorData(object):
    def __init__(self,sen1Y=[],sen2Y=[]):
    # def __init__(self,sen1Y=[],sen1X=[],sen2Y=[],sen2X=[]):
        self.sen1Y = sen1Y
        # self.sen1X = sen1X
        self.sen2Y = sen2Y
        # self.sen2X = sen2X
    def updateY(self,s1,s2):
        self.sen1Y.append(s1)
        self.sen2Y.append(s2)

        

def establishSerial(baud,selectComm=False):
    """Opens the comm port and returns the open serial object"""

    print('Opening Serial Port...')
    # Have the user select the serial port that the xbee is on
    if selectComm:
        # Mac or linux serial ports...
        if os.name == 'posix':
            print('Select comm port number: ')
            commPorts = [i.name for i in os.scandir('/dev') if str(i.name).startswith('tty.')]
            for i in commPorts: print(i)
            serialPath = '/dev/'+ commPorts[int(input('Comm port number: '))-1]
        elif os.name == 'nt':
            # If on windows
            # This needs to be implimentd to work with windows serial ports
            print('maunally add comm port in establishSerial')
            exit()
        else:
            # If on another os, possiblilites are 'ce' or 'java'
            # This needs to be implimentd to work with other serial ports
            print('maunally add comm port in establishSerial')
            exit()
        
    else:
        # This was my default serial port on mac
        serialPath = DEFAULT_SERIAL_PORT
    
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

    



def updatePlot(sensors):
    """Updates the plot: this is where live plotting takes place"""
    # sen1 and sen2 are classes of sensor Data
    x1 = range(len(sensors.sen1Y))
    x2 = range(len(sensors.sen1Y))

    ax1.clear() 
    ax1.plot(x1,sensors.sen1Y,x2,sensors.sen2Y)
    plt.pause(.1)
    


    # plt.draw()
    # ax1.plot(sen1.y,)

    # line, = plt.plot(sen1.y)
    # plt.ylim([0,51])

    pass
    

def reParser(strIn):
    
    # Will be the new way to implement parsing when start and delimiters are changed
    # regex = r"" + re.escape(STARTBYTE) + "(.*?) + re.escape(DELIMITER)"

    fullData1 = re.findall(r'/(.*?)\^',strIn)[0]
    fullData2 = re.findall(r'\^(.*?)\;',strIn)[0]
    # re.findall(r'\d+',d1)[0]

    return re.findall(r'(\d+)',fullData1)[0] , re.findall(r'(\d+)',fullData2)[0]
    # return(int(numData1),int(numData2))

    # print(re.findall(r'/(.*?)\^',strIn ))
    # print(re.findall(r'\^(.*?);',strIn ))
    # print(strIn)

    # print(re.findall(r'/(Data_One.*?)\^',strIn ),re.findall(r'\^(Data_Two.*?)\;',strIn ))
    
    


def parse(inData):
    """An old function previously used to decode the data
    from hex into ascii, keep in-case we send via hex later"""
    # KEY

    # halfRaw = [i for i in inData if i is not None]
    if type(inData) is hex:
        logRaw  = str(binascii.unhexlify(inData))
    else:
        logRaw = str(inData)
    # Trimms the binary tag off of the data stream, not really necessary
    return reParser(logRaw[2:-1])

                

def decodeLog(data):
    """Old function that was used to split and reassemble the data stream
    when the data was recieved from a log file in hex form"""
    for line in data:
        x = line.split()
        if len(x) > 0:
            u = x[1].split(",")
            try: 
                parse(u[-1])
            except Exception as e:
                print(e)
                logRaw = "Failed to parse"
def decodehex(data):
    """old code used to split the data stream when in hex form
    delete in later revisions"""
    for l in data:
        lines = l.split('0A')
        for i in lines:
            if len(i)>1:
                parse(i)
        # lines = [i+'0A' for i in lines]

def fakeSerialStream(numData):
    for i in range(numData):
        pass
    pass

def main(): 
    """Main code execution"""
    
    report,serialPort = establishSerial(57600,selectComm=True)
    
    # On a crash or exit, this should close the serial port    
    atexit.register(onClose(serialPort))
    rawDataLine=[]
    sensors = sensorData()
    plt.show()
    
    # This is the main loop of the function that is reading and parsing data
    i = 0
    # If we have a good serial connection...
    if report:
        # Loop until the user force quits... or the program crashes...
        while True:
            try:
                if serialPort.inWaiting():
                    rawDataLine.append(serialPort.read())
                    # If we are at the last character in the data stream
                    if rawDataLine[-1] == ENDBYTE:
                        # Join the data stream back into one string
                        dataLine = b''.join(rawDataLine)
                        # Makes sure that we have data, might not be nessicary
                        if len(dataLine) is not 0:
                            
                            # parses the data from the data stream
                            toUpdate = reParser(str(dataLine))
                            sensors.updateY(toUpdate[0],toUpdate[1])

                            # Let the user know that the program is running of the graph is frozen
                            i +=1;
                            print(i)

                            # The main plotting, commented out now to prevent crashing
                            # updatePlot(sensors)
                            

                        rawDataLine = []
            except KeyboardInterrupt:
                # closes the serial port uppon force quit
                onClose(serialPort)
                exit()
    pass

def onClose(serialPort):
    """Function to close the serial port upon exit"""
    serialPort.close()
    print('I want')
    if not serialPort.isOpen():
        print(' Serial successfully closed')
    pass

if __name__ == '__main__':
    main()
        

