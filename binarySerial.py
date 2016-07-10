import os, serial, sys, struct
import numpy as np
'''
could use dictionaries to form key and order of data stream being passed
'''

def cs(inDat):
    return sys.getsizeof(inDat)

startChar = float(1111111111)
endChar = float(1010101010)
outF = 'dataStreamEx.txt'
numData = 10
dataLoops = 3

def genData(length):
    x = np.random.random(length)
    data = [i*100 for i in x]
    return data

def updateData(dataLen):
    upDatedData = []
    for ide in dataLen:
        upDatedData.append(ide * np.random.random())
    return upDatedData



def makeDataStream(*args):
    ds = []
    ds.append(startChar)
    for i,ins in enumerate(args):
        if type(ins) is list:
            [ds.append(x) for x in ins]
        else:
            ds.append(ins)
    ds.append(endChar)
    return ds



# def pack_all(lst):
#     fmt = ''.join('i' if isinstance(x, int) else 'd' for x in lst)
#     return struct.pack(fmt, *lst), fmt
def pack_all(dataList):
    fmt = ''.join('d' for x in range(numData+2))
    return struct.pack(fmt, *dataList)



def clearFile(fName):
    if os.path.isfile(fName):
        os.truncate(fName,0)
    else:
        with open(fName,'wb') as f:
            pass


def writeData(fName,data):
    with open(fName,'ab') as f:
        f.write(data)



def unpack(bl):
    fmt = ''.join('d' for x in range(numData+2))
    return struct.unpack(fmt,bl)   
    
def decodeData(fName,numLoops):
    print("start of decodeData()")
    with open(fName,'rb') as f:
        for i in range(numLoops):
            # retrievedData = f.read(8*(numData + 2))
            retrievedData = f.read(8*(numData +2))

            print(sys.getsizeof(retrievedData))
            c1 = unpack(retrievedData)
            print('size unpacked',cs(c1))
            print(c1)

'''try sending directly to encoder instad of writing to file'''
def main():
    clearFile(outF)
    data = genData(numData)
    for i in range(dataLoops):
        if i > 0:
            data = updateData(data)
        dataStream = makeDataStream(data)
        # [print(sys.getsizeof(x)) for x in dataStream]
        # [print(type(x)) for x in dataStream]
        dataPacket = pack_all(dataStream)
        print(type(dataPacket),sys.getsizeof(dataPacket))
        # print(dataStream,dataPacket)
        writeData(outF,dataPacket)
    
    decodeData(outF,dataLoops)

    pass
main()
