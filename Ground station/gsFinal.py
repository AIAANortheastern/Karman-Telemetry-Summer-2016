import os
import atexit
import serial
import pdb
import sys
import time

DEFAULT_SERIAL_PORT = '/dev/tty.usbserial-DA01IFE8'

    # currTime) + ',';
    # gWriteData.write_send.component.temp1
    # gWriteData.write_send.component.temp2
    # gWriteData.write_send.component.temp3
    # gWriteData.write_send.component.temp_10dof
    # gWriteData.write_send.component.alt_press
    # gWriteData.write_send.component.alt_strat
    # gWriteData.write_send.component.alt_gps
    # gWriteData.write_send.component.lat
    # gWriteData.write_send.component.lat
    # gWriteData.write_send.component.accel_x
    # gWriteData.write_send.component.accel_y
    # gWriteData.write_send.component.accel_z
    # gWriteData.write_send.component.poll_flags

    # gWriteData.write_only.gyro->z

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


def getFileName(dataBase):
    # # os.
    # files = [x for x in os.listdir(".") if x.startswith(dataBase)]
    # num = 0
    # if files == []:
    #     return dataBase + "001.txt"
    # else:
    #     for f in files:
    #         num2 = int(f[:3]) + 1
    #         if num2 > num1



    
    pass

def plotData(serialPort, dataFile):
    
    # pdb.set_trace()
    start = time.time()
    dataLine = b""
    while True:
        # print("NEW LINE")

        
            # dataLine = ""
        # print(time.time() - start)

        if serialPort.inWaiting():
            d = serialPort.read()
            # print(d)
            with open(dataFile, "ab") as f:
                f.write(d)
            if (time.time() - start) % 5 < 0.0000001:
                print("good data")
            # dataLine += serialPort.read()



    pass


def main():
    """Main code execution"""
    print("Karman Telemetry ground station execution!\n")
    print("Establishing serial connection...")

    # pdb.set_trace()
    x = os.getcwd()
    dataBase = x + "/savedTelemetry_"
    # fNmae = getFileName(dataBase)

    args = sys.argv
    
    if len(args) > 1:
        fName = args[-1]

    report,serialPort = establishSerial(57600,selectComm=True)
    # atexit.register(onClose,serialPort)
    
    if report:
        plotData(serialPort, fName)
        pass
    # On a crash or exit, this should close the serial port    
    
    # print("THIS IS DONE")
    # rawDataLine=[]
    # sensors = sensorData()
    quit(0)

    pass

def onClose(serialPort):
    """Function to close the serial port upon exit"""
    serialPort.close()
    print('I want')
    if not serialPort.isOpen():
        print(' Serial successfully closed')
    pass
    quit(1)

if __name__ == '__main__':
    main()


main();