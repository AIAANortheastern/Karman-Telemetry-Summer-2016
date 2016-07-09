import os, serial, sys, struct

startChar = float(1111111111)
endChar = float(1010101010)
inF = 'dataStreamEx.txt'
datNums = 5

def readFromF(numData = datNums):
    with open(inF,'rb') as f:
        a1 = float(f.read(24))
        if a1 == startChar:
            print(True)
        else:
            print(a1)

    pass


with open(inF,'rb') as f:
    c2 = f.read(64)
    c3 = struct.unpack('dddddddd',c2)
    print(c3)



# readFromF()