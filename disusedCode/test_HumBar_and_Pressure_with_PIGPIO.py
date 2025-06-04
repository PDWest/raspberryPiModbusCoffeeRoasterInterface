# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HCPA_5V_U3
# This code is designed to work with the HCPA-5V-U3_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HCPA-5V-U3_I2CS#tabs-0-product_tabset-2

import time
import pigpio

# The pigs daemon needs to be starte, e.g.
# sudo pigpiod -s 2 -b 200 -f
# as described at: https://abyz.me.uk/rpi/pigpio/pigpiod.html
# to ensure it's running try the command
# >pigs t
# and verify that it returns an integer

#I2C_ADDR=0x13

# This command should show devices on i2c bus
# i2cdetect -q -y -a 1 0x03 0x7f



# Get I2C bus
#bus = smbus.SMBus(1)
# HCPA_5V_U3 address, 0x28(40)
# Send start command, 0x80(128)
pi = pigpio.pi() # Connect to local Pi.
tempHumHandle = pi.i2c_open(1, 0x28)
data = []
(b, data) = pi.i2c_read_i2c_block_data(tempHumHandle, 0x80, 4)


#bus.write_byte(0x28, 0x80)

#time.sleep(0.5)

# HCPA_5V_U3 address, 0x28(40)
# Read data back, 4 bytes
# humidity msb, humidity lsb, cTemp msb, cTemp lsb
#data = bus.read_i2c_block_data(0x28, 4)
print("Frist, read the temp hum sensor **********")

# Convert the data to 14-bits
humidity = (((data[0] & 0x3F) * 256) + data[1]) / 16384.0 * 100.0
cTemp = (((data[2] * 256) + (data[3] & 0xFC)) / 4) / 16384.0 * 165.0 - 40.0
fTemp = (cTemp * 1.8) + 32

# Output data to screen
print("i2c Handle:", tempHumHandle)
print("Relative Humidity: ",humidity)
print("Temperature (C):",cTemp)
print("Temperature (F):",fTemp)

#Now, try to read the pressure sensor

# data = bus.read_i2c_block_data(0x78, 4)
pressureHandle = pi.i2c_open(1, 0x78)
#data = [0, 0, 0, 0]
#(b, data) = pi.i2c_read_device(pressureHandle, 4)
#data[0] = pi.i2c_read_byte(pressureHandle)
#data[1] = pi.i2c_read_byte(pressureHandle)
#data[2] = pi.i2c_read_byte(pressureHandle)
#data[3] = pi.i2c_read_byte(pressureHandle)
data = []
(b, data) = pi.i2c_read_device(pressureHandle, 4)
print("b=",b,"data=", data)
# Convert the data
pres = ((data[0] & 0xFF) * 256) + data[1]
temp = ((data[2] * 256) + (data[3] & 0xFF)) / 32
#pressure = (pres - 1638.0) / (13107.0 / 10.0)
pressure = (pres - 3277)/55.16
cTemp = ((temp * 200.0) / 2048) - 50.0
fTemp = (cTemp * 1.8 ) + 32
# Note, the calculations at 
#    https://github.com/ControlEverythingCommunity/AMS5812-0001-D/blob/master/Arduino/AMS5812.ino
# look a bit different

print("Next, read the pressure sensor **********")

# Output data to screen
print("i2c Handle:", pressureHandle)
print("Number of bytes read:", b, "and they were", data[0], data[1], data[2], data[3])
print ("Pressure =", pressure, "mbar") # pressure
print("Temp =", fTemp,"F")

pi.i2c_close(pressureHandle)
pi.i2c_close(tempHumHandle)
pi.stop()