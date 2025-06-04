# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HCPA_5V_U3
# This code is designed to work with the HCPA-5V-U3_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HCPA-5V-U3_I2CS#tabs-0-product_tabset-2

# This program shows how to access the ?? NCD Humidity Sensor via their quad multiplexor
# The MX is at 0x70
# and the Hum Temp sensor is at 0x28
# The Hum Temp sensor is plugged into the second I2C slot on the mux


import smbus2
import time

# Get I2C bus
bus = smbus2.SMBus(1)
muxAdr = 0x70
tempHumAdr = 0x28
AMS812_Adr = 0x78
startCommand = 0x80
muxPortNum = 0x1

bus.write_byte(muxAdr, muxPortNum)
#time.sleep(0.1)   #This needs to be as small as reliable


bus.write_byte(tempHumAdr, startCommand)
d = bus.read_i2c_block_data(tempHumAdr, 0, 4)

# h = pi.i2c_open(1, TempHumAdr)
#pi.i2c_write_device(h, [0xAC])
#(b, d) = pi.i2c_read_device(h, 4)

print(d[0], d[1], d[2], d[3])


# Convert the data
data = d
pres = ((data[0] & 0xFF) * 256) + data[1]
temp = ((data[2] * 256) + (data[3] & 0xFF)) / 32
pressure = (pres - 1638.0) / (13107.0 / 10.0)
cTemp = ((temp * 200.0) / 2048) - 50.0
fTemp = (cTemp * 1.8 ) + 32

# Output data to screen
print ("Pressure =", pressure, "mbar") # pressure
print("Temp =", fTemp,"F")

# Now, let's try to  add the AMS812 onto the second port

muxPortNum = 0x2
bus.write_byte(muxAdr, muxPortNum)
time.sleep(0.1)   #This needs to be as small as reliable
b = bus.read_byte_data(AMS812_Adr, 0)

#bus.write_byte(tempHumAdr, startCommand)
d = bus.read_i2c_block_data(AMS812_Adr, 0, 4)

# h = pi.i2c_open(1, TempHumAdr)
#pi.i2c_write_device(h, [0xAC])
#(b, d) = pi.i2c_read_device(h, 4)

print(d[0], d[1], d[2], d[3])


# Convert the data
data = d
pres = ((data[0] & 0xFF) * 256) + data[1]
temp = ((data[2] * 256) + (data[3] & 0xFF)) / 32
pressure = (pres - 1638.0) / (13107.0 / 10.0)
cTemp = ((temp * 200.0) / 2048) - 50.0
fTemp = (cTemp * 1.8 ) + 32

# Output data to screen
print ("Pressure =", pressure, "mbar") # pressure
print("Temp =", fTemp,"F")