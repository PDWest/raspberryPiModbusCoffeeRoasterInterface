# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9531
# This code is designed to work with the PCA9531_I2CPWM I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Open-Collectors?sku=PCA9531_I2CPWM#tabs-0-product_tabset-2

# To use this to drive the SSR, note:
# The PWM, pin0 is an open collector driver, so when on it's low.
# To drive the SSR, we connect the + side of the SSR to V+ (possibly the bus pull up pin)
# and connect the SSR - terminal to Pin0.  I don't believe a resistor is needed as the SSR
# presents, I think, as a TTL load.

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# PCA9531 address, 0x60(96)
PCA9531_address = 0x60
frequencyPreScalerAddress = 0x01
LED_selector_register = 0x05 #05
PWM_Register0 = 0x02


# Select frequency prescaler 0 register, 0x01(01)
# The period of BLINK0 = (PSC0 + 1) / 152.
# Max period is PCS0 = 0xFF
#PCS0 =	0x4B #75 Period of blink = 0.5 sec

PCS0 =	0xFF
bus.write_byte_data(PCA9531_address, frequencyPreScalerAddress, PCS0)


#		0xAA(170)	Output set to Blinking at PWM0
Output_Selector = 10 #Output zero blinks at PWM rate 
bus.write_byte_data(PCA9531_address, LED_selector_register, Output_Selector)
# PCA9531 address, 0x60(96)
# Select LED selector register, 0x06(06)
#		0xAA(170)	Output set to Blinking at PWM0
#bus.write_byte_data(0x60, 0x06, 0xAA)

# Select pulse width modulation 0 register, 0x02(02)
# Duty cycle = Duty/256
Duty = 	0.1 #Duty factor desired (e.g. 10% = 0.1)
DutyWord = int((1.0-Duty) * 256)

bus.write_byte_data(PCA9531_address, PWM_Register0, DutyWord)

while True:
    Duty = 0.0
    while Duty <= 1.0:
        Duty = Duty + 0.1
        DutyWord = int((1.0-Duty) * 256)
        bus.write_byte_data(PCA9531_address, PWM_Register0, DutyWord)
        time.sleep(10)
    
