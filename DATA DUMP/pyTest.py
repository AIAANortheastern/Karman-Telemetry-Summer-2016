fName = "DATA16"

import pdb
alt = []
with open(fName, "r") as f:
    for i, line in enumerate(f):
        # pdb.set_trace()
        
        if i > 15000 and i < 18000:
            alt.append( 3.28 * float(line.split(",")[5]))
        
        # pdb.set_trace()
        

import matplotlib.pyplot as plt
# pdb.set_trace()
print(max(alt))
# print(alt[11000]*3.28)
plt.plot([x for x in range(len(alt))], alt)
plt.show()


    'currTime'
    'temp1'
    'temp2'
    'temp3'
    'temp_10dof'
    'alt_press'
    'alt_strat'
    'alt_gps'
    'lat'
    'lat'
    'accel_x'
    'accel_y'
    'accel_z'
    'poll_flags'
    'pressure'
    'orientation.roll'
    'orientation.pitch'
    'orientation.heading'
    'accel_X'
    'accel_Y'
    'accel_Z'
    'mag_X'
    'mag_Y'
    'mag_Z'
    'gyro_X'
    'gyro_Y'
    'gyro_Z'

'''
    *pWriteString += String(currTime) + ',';
    *pWriteString += String(gWriteData.write_send.component.temp1) + ',';
    *pWriteString += String(gWriteData.write_send.component.temp2) + ',';
    *pWriteString += String(gWriteData.write_send.component.temp3) + ',';
    *pWriteString += String(gWriteData.write_send.component.temp_10dof) + ',';
    *pWriteString += String(gWriteData.write_send.component.alt_press) + ',';
    *pWriteString += String(gWriteData.write_send.component.alt_strat) + ',';
    *pWriteString += String(gWriteData.write_send.component.alt_gps) + ',';
    *pWriteString += String(gWriteData.write_send.component.lat) + ',';
    *pWriteString += String(gWriteData.write_send.component.lat) + ',';
    *pWriteString += String(gWriteData.write_send.component.accel_x) + ',';
    *pWriteString += String(gWriteData.write_send.component.accel_y) + ',';
    *pWriteString += String(gWriteData.write_send.component.accel_z) + ',';
    *pWriteString += String(gWriteData.write_send.component.poll_flags) + ',';
    *pWriteString += String(*(gWriteData.write_only.pressure)) + ',';
    *pWriteString += String(gWriteData.write_only.orientation.roll) + ',';
    *pWriteString += String(gWriteData.write_only.orientation.pitch) + ',';
    *pWriteString += String(gWriteData.write_only.orientation.heading) + ',';
    *pWriteString += String(gWriteData.write_only.accel->x) + ',';
    *pWriteString += String(gWriteData.write_only.accel->y) + ',';
    *pWriteString += String(gWriteData.write_only.accel->z) + ',';
    *pWriteString += String(gWriteData.write_only.mag->x) + ',';
    *pWriteString += String(gWriteData.write_only.mag->y) + ',';
    *pWriteString += String(gWriteData.write_only.mag->z) + ',';
    *pWriteString += String(gWriteData.write_only.gyro->x) + ',';
    *pWriteString += String(gWriteData.write_only.gyro->y) + ',';
    *pWriteString += String(gWriteData.write_only.gyro->z) + ',';
'''