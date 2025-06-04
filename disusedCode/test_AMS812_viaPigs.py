#!/usr/bin/env python

# code from https://forums.raspberrypi.com/viewtopic.php?t=238245

import pigpio
import time
from subprocess import check_output

# GPIO and address Definiton

PRESSURE_SENSOR_SDA = 2
PRESSURE_SENSOR_SCL = 3
DEVICE_ADDRESS = 0x78

def i2c_init():

    SDA = PRESSURE_SENSOR_SDA
    SCL = PRESSURE_SENSOR_SCL

    # GPIO Pull Ups
    handler.set_pull_up_down(SDA, pigpio.PUD_UP)
    handler.set_pull_up_down(SCL, pigpio.PUD_UP)
    time.sleep(0.01)    

    try:
        #init i2c 
        handler.bb_i2c_open(SDA, SCL, 50000)
        print("BitBang handler opened on pins",SDA, SCL)
        return 0
        
    except:
        # reinit i2c
        handler.bb_i2c_close(SDA) 
        print("BitBang handler open failed on pins",SDA, SCL)
        return 1

try:
    # Check if pigpiod is up
    out = check_output(["sudo", "pidof", "pigpiod"]) 
    print("pigpiod is up: RC=", out)
except:
    # Start daemon
    print("starting pigpiod")
    out = check_output(["sudo", "pigpiod"]) 
    print("pigpiod is up: RC=", out)
    time.sleep(2)

handler = pigpio.pi()

if not handler.connected:
    exit()

for i in range(3):
    if i2c_init()==0:
        break
    else:
        time.sleep(1)
    

while True:
    try:
        start = time.clock()
        #(countPressure, dataPressure) = handler.bb_i2c_zip(PRESSURE_SENSOR_SDA, [4, DEVICE_ADDRESS, 2, 6, 2, 3, 0])
        (count, data) =  handler.bb_i2c_zip(PRESSURE_SENSOR_SDA, [4, DEVICE_ADDRESS, 2, 6, 4, 3, 0]) #{start read 4bytes end done}
                                                                  

                                                                   
        print("count:",count,"  data:",data,"  elapsed time (ms):",(time.clock() - start)*1000)
        pres = ((data[0] & 0xFF) * 256) + data[1]
        temp = ((data[2] * 256) + (data[3] & 0xFF))
        pres = int((pres - 3277)/55.16)
        cTemp = ((temp - 3277.0) / ((26214.0) / 110.0)) - 25.0
        fTemp = (cTemp * 1.8 ) + 32
        
        
        # Output data to screen
        print ("Pressure =", pres, "mbar") # pressure
        print("Temp =", fTemp,"F","  or", cTemp, "C")


    except:
        valuePressure = 0
        pressure = 0.0

    #print('Digital ' + str(valuePressure) + ' = ' + str(round(pressure * 1000,2)) + ' hPa')

    time.sleep(2)