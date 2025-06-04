# raspberryPiModbusCoffeeRoasterInterface



We use a Raspberry Pi W to acquire data from our coffee roaster over WiFi using a modbus protocol.  Note that we have two primary folders, disusedCode and workingCode.  This is because we originally had a nice clean method for accessing the I2C bus on the raspberry Pi, but when we got our gas pressure sensor, it had a hardwired address that was outside of the space accessible by the original I2C driver.  This pushed us to a less elegant bit bang approach.  Thus, I have tried to preserve the original, cleaner, code in the disUsed directory, while putting the current working and used code in the working directory.



Also of note is that we have an I2C temp/humidity sensor that is also disused which we had intended to use as an ambient conditions sensor.  It is disabled because there seems to be no way in Artisan to set it up as a 'one shot' measurement if used under modbus--we'd need to query it each time we read the temp. 



