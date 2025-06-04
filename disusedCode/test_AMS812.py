# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HCPA_5V_U3
# This code is designed to work with the HCPA-5V-U3_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HCPA-5V-U3_I2CS#tabs-0-product_tabset-2



from smbus2 import SMBus, i2c_msg
import time




# Get I2C bus
bus = SMBus(1)

# AMS5812 address, 0x78
# Send start command, 0x
#bus.write_byte(0x78, 0x8)
#bus.write_quick(0x78)
#time.sleep(1)

# Read 4 bytes from address 78
#write = i2c_msg.write(0x78, [0x80])
#msg = i2c_msg.read(0x78, 4)
#bus.i2c_rdwr(msg)
#data = list(msg)  # data = [1, 2, 3, ...]
#print("Number of elements read from i2c =", len(data))
##print("msg =",msg)
##print("data=",data)
#for value in msg:
    #print(value)


# Read a block of 16 bytes from address 80, offset 0
block = bus.read_byte_data(0x78,0)
# Returned value is a list of 16 bytes
print(block)


# data = bus.read_i2c_block_data(0x78, 0x00, 4)

# Convert the data
pres = ((data[0] & 0xFF) * 256) + data[1]
temp = ((data[2] * 256) + (data[3] & 0xFF))
pres = ((pres - 3277.0) / ((26214.0) / 100.0)) - 100.0
cTemp = ((temp - 3277.0) / ((26214.0) / 110.0)) - 25.0
fTemp = (cTemp * 1.8 ) + 32


# Output data to screen
print ("Pressure =", pres, "mbar") # pressure
print("Temp =", fTemp,"F","  or", cTemp, "C")

print("from the tempHum sensor...")
#data = bus.read_i2c_block_data(0x28, 4)
msg = i2c_msg.read(0x28, 4)
bus.i2c_rdwr(msg)
data = list(msg) 

# Convert the data to 14-bits
humidity = (((data[0] & 0x3F) * 256) + data[1]) / 16384.0 * 100.0
cTemp = (((data[2] * 256) + (data[3] & 0xFC)) / 4) / 16384.0 * 165.0 - 40.0
fTemp = (cTemp * 1.8) + 32

# Output data to screen
print("Relative Humidity: ",humidity)
print("Temperature (C):",cTemp)
print("Temperature (F):",fTemp)
