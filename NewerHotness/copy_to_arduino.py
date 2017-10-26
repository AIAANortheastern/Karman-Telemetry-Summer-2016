import os

files = [x for x in os.listdir(".") if (x.lower().endswith(".h") or x.lower().endswith(".cpp"))]

# print files

for f in files:
    