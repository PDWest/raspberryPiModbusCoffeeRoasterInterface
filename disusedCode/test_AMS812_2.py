# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HCPA_5V_U3
# This code is designed to work with the HCPA-5V-U3_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HCPA-5V-U3_I2CS#tabs-0-product_tabset-2




import time
import pigpio

pi = pigpio.pi()

h = pi.i2c_open(1, 0x78)

#pi.i2c_write_device(h, [0xAC])
time.sleep(0.05)
(b, d) = pi.i2c_read_device(h, 4)

print(d[0], d[1], d[2], d[3])

pi.i2c_close(h)

pi.stop()


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
