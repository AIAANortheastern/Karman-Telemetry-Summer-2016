"""
This program was to test out parsing a fake data stream using regular expressions
"""

import re
fN = 'lineOut.txt'
data = "/Data_One:242^Data_Two:242;\n/Data_One:243^Data_Two:243;'"
# with open(fN,'r') as f:
#     data = f.read()
def oldParse(dataIn):
    return re.findall(r'/(.+)\^',dataIn ),re.findall(r'\^(.+)\;',dataIn)

def dataParse(dataIn):
    return re.findall(r"(\d+)",dataIn)[0]

D1,D2 = oldParse(data)
print(D1)
print('The first data is: ',dataParse(D1[0]))
print('The second data is: ',dataParse(D2[1]))



