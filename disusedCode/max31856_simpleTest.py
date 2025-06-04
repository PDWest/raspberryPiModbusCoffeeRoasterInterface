"""
Copyright (c) 2019 John Robinson
Author: John Robinson
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# Global Imports
import logging
import time
import Adafruit_GPIO

MAX31856_J_TYPE = 0x2 # Read J Type Thermocouple
MAX31856_K_TYPE = 0x3 # Read K Type Thermocouple


# Local Imports
from max31856 import MAX31856 as MAX31856
import RPi.GPIO as GPIO

logging.basicConfig(
    filename='simpletest.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)


# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX31856(tc_type=MAX31856_K_TYPE, avgsel=0x0,hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))
SPI_DEVICE = 1
sensor2 = MAX31856(tc_type=MAX31856_K_TYPE, avgsel=0x0,hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    temp = sensor.read_temp_f()
    #internal = sensor.read_internal_temp_c()
    print('Thermocouple1 Temperature: {0:0.3F}*C'.format(temp))
    print('    Internal1 Temperature: {0:0.3F}*C'.format(internal))
    temp = sensor2.read_temp_f()
    internal = sensor2.read_internal_temp_c()
    print('Thermocouple2 Temperature: {0:0.3F}*C'.format(temp))
    print('    Internal2 Temperature: {0:0.3F}*C'.format(internal))
    time.sleep(1.0)