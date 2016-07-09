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

def genData(len = 5):
    x = np.random.random(len)
    data = [i for i in x]
    return data

data = genData(5)
addData = float(5)



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

dataStream = makeDataStream(data,addData)
# toBytes = struct.pack('%d' %len(dataStream), *dataStream)
# toBytes = struct.pack('%d', dataStream)


def pack_all(lst):
    fmt = ''.join('i' if isinstance(x, int) else 'd' for x in lst)
    return struct.pack(fmt, *lst), fmt
x1,FMT = pack_all(dataStream)

with open(outF,'wb') as f:
    f.write(x1)
print(cs(x1))

def unpack(bl):

    return struct.unpack('dddddddd',bl)
    # return struct.calcsize(bl)
    pass    


print(unpack(x1))