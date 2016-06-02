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

    



def updatePlot(sensors):
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
    # KEY

    # halfRaw = [i for i in inData if i is not None]
    if type(inData) is hex:
        logRaw  = str(binascii.unhexlify(inData))
    else:
        logRaw = str(inData)
    # Trimms the binary tag off of the data stream, not really necessary
    return reParser(logRaw[2:-1])

                

def decodeLog(data):
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
    for l in data:
        lines = l.split('0A')
        for i in lines:
            if len(i)>1:
                parse(i)
        # lines = [i+'0A' for i in lines]


def main(): 
    report,serialPort = establishSerial(9600,selectComm=True)
    rawDataLine=[]
    sensors = sensorData()
    plt.show()
    
    i = 0
    if report:
        # Get serial data
        while True:
            try:
                if serialPort.inWaiting():
                    rawDataLine.append(serialPort.read())
                    if rawDataLine[-1] == ENDBYTE:
                        dataLine = b''.join(rawDataLine)
                        if len(dataLine) > 5:
                            
                            
                            toUpdate = reParser(str(dataLine))
                            sensors.updateY(toUpdate[0],toUpdate[1])

                            i +=1;
                            print(i)
                            updatePlot(sensors)
                            

                        rawDataLine = []
            except KeyboardInterrupt:
                serialPort.close()
                if not serialPort.isOpen():
                    print(' Serial successfully closed')
                exit()
    pass

if __name__ == '__main__':
    main()
        
