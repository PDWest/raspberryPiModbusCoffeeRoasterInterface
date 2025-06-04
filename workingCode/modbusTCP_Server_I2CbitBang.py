#!/usr/bin/env python
# See e.g. https://umodbus.readthedocs.io/en/latest/
# scripts/examples/simple_tcp_server.py
# Note: this code works with Artisan and runs from my conda MachineLearning env
import logging
import time
from socketserver import TCPServer
from collections import defaultdict

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

# Local Imports
from max31856 import MAX31856 as MAX31856
#from nodeLynkDevs import nodeLynkDevs as nodeLynkDevs

import RPi.GPIO as GPIO
import pigpio
import time
from subprocess import check_output

import Adafruit_GPIO

MAX31856_J_TYPE = 0x2 # Read J Type Thermocouple
MAX31856_K_TYPE = 0x3 # Read K Type Thermocouple

# Create Thermocouple Objects
SPI_PORT   = 0
SPI_DEVICE = 0
TC_1 = MAX31856(tc_type=MAX31856_K_TYPE, avgsel=0x02,hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))
SPI_DEVICE = 1
TC_2 = MAX31856(tc_type=MAX31856_K_TYPE, avgsel=0x02,hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))
PRESSURE_SENSOR_SDA = 2
PRESSURE_SENSOR_SCL = 3
PRESSURE_SENSOR_I2C_ADDRESS = 0x78


# *** Set up the pigpio connection


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




logging.basicConfig(
        filename='simpletest.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)



# Add stream handler to logger 'uModbus'.
# log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresss against their values.
# data_store = defaultdict(int)
# Artisan Ports Configuration settings:
# Slave = 1 for input 1,2,3 and = 0 for input 4,5,6
# register = input number
# function = 4
# tenths of a degree.  Need to configure the Artisan Ports tab with:
# Divider = 1/10, 
# Mode and Decode blank
# endian both unchecked
# Artisan Device, Extra Devices tab, MODBUS 34, Lable 1=PWM

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ("0.0.0.0", 1502), RequestHandler)  #This might not be the best IP to use...

@app.route(slave_ids=[1], function_codes=[3, 4], addresses=list(range(0, 6)))  #I'm not clear on the correct number for this range...
def read_data_store(slave_id, function_code, address):
	print("SENDING: slave_id=",slave_id,"function_code=",function_code,"address=",address,end='')
	if address == 1:
		TC1 = TC_1.read_temp_f_4_Artisan()
		print("temp=", TC1)
		return TC1
	elif address == 2:      
		TC2 = TC_2.read_temp_f_4_Artisan()
		print("temp=", TC2)
		return TC2
	#elif address == 2:      
		#TC2 = TC_2.read_temp_f_4_Artisan()
		#print("temp=", TC2)
		#return TC2	
	
	elif address == 3:  #Pressure Sensor
		(count, data) =  handler.bb_i2c_zip(PRESSURE_SENSOR_SDA, [4, PRESSURE_SENSOR_I2C_ADDRESS, 2, 6, 4, 3, 0]) #{start read 4bytes end done}
		pres = ((data[0] & 0xFF) * 256) + data[1]
		# temp = ((data[2] * 256) + (data[3] & 0xFF))
		pres = 10*max(0, int(((pres - 3277)/55.16))) #Multiply by 10 here and then divide by 10 on the Artisan side
		#cTemp = ((temp - 3277.0) / ((26214.0) / 110.0)) - 25.0
		#fTemp = (cTemp * 1.8 ) + 32	
		#print("Burner pressure=", pres, "count=",count)
		pres = int(pres * 1.167 + 1.0445) #cal factor.  Need to understand the multiplier here!! 	
		return pres
	else:
		return 0

	#elif address == 4:
		#print("returning gas pressure=", gasPressure.readGasPressure
	#elif address == 4:
		#print("returning amb temp=", TempHum.readTempHum('T'))
		#return TempHum.readTempHum('T')
	#elif address == 5:
		#print("returning amb humidity=",TempHum.readTempHum('H'))
		#return TempHum.readTempHum('H')
	#else:
		#return 0

	#Remember we'll need extra registers for ambient temp and humidity
#    print("In read_data_store", slave_id, function_code, address)
#    if address == 1:
#        return   int(10*TC_1.read_temp_f())
#    elif address == 2:
#        return int(10*TC_2.read_temp_f())
#    elif address == 3:
#        return PWM
#    if address == 7:
#        return   int(10*TC_1.read_temp_f())
#    elif address == 8:
#        return int(10*TC_2.read_temp_f())    
#    else:
#        return 0    



@app.route(slave_ids=[1], function_codes=[6, 16], addresses=list(range(0, 10)))
def write_data_store(slave_id, function_code, address, value):
	"""" Set value for address. """
	print("RECEIVING: slave_id=",slave_id,"function_code=",function_code,"address=",address," value=",value)
	if ((function_code == 6) and (address == 4)):
		PWM.setPWM(value)


if __name__ == '__main__':
	try:
		print("about to start the app")
		app.serve_forever()
	finally:
		app.shutdown()
		app.server_close()
