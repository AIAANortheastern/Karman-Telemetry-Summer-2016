fName = "DATA16"

import pdb
import matplotlib.pyplot as plt
import csv

d = {
"currTime": 0,
"temp1": 1,
"temp2": 2,
"temp3": 3,
"temp_10dof": 4,
"alt_press": 5,
"alt_strat": 6,
"alt_gps": 7,
"lat": 8,
"lat": 9,
"accel_x": 10,
"accel_y": 11,
"accel_z": 12,
"poll_flags": 13,
"pressure": 14,
"orientation.roll": 15,
"orientation.pitch": 16,
"orientation.heading": 16,
"accel_x": 18,
"accel_y": 19,
"accel_z": 20,
"mag_x": 21,
"mag_y": 22,
"mag_z": 23,
"gyro_x": 24,
"gyro_y": 25,
"gyro_z": 26
}


buff = []


alt = []
pres = []

with open(fName, "r") as f:

    # throw out the initial data to get to a csv format
    f.readline()
    f.readline()
    f.readline()
    f.readline()

            


    # for i, line in enumerate(f):
        # pdb.set_trace()
        
        # if i > 15000 and i < 18000:
            
        #     alt.append( 3.28 * float(line.split(",")[5]))
        #     pres.append(float(line.split(",")[d['pressure']]))
        
        # pdb.set_trace()
        
# # pdb.set_trace()
# print(max(alt))
# # print(alt[11000]*3.28)
# xs = [x for x in range(len(alt))]
# # plt.plot(xs, alt, label = 'altitude')
# plt.plot(xs, pres, label = 'pressure')
# plt.show()

