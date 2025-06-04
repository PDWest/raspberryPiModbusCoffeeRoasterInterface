 
import smbus
import time 
 
class nodeLynkDevs:
    
  # PCA9531 address, 0x60(96)
 
  
  def __init__(self, device):  #Device = TempHum, PWM
    self.bus = smbus.SMBus(1)
    if device == 'TempHum':
      self.HCPA_5V_U3_address = 0x28  #(40)
    elif device == 'PWM':
      frequencyPreScalerAddress = 0x01
      LED_selector_register = 0x05 #05
      Output_Selector = 10 #Output zero blinks at PWM rate 
      self.CurrentDuty = 0
      self.PCA9531_address = 0x60
      self.PWM_Register0 = 0x02      
      
      # Select frequency prescaler 0 register, 0x01(01)
      # The period of BLINK0 = (PSC0 + 1) / 152.
      # Max period is PCS0 = 0xFF
      #PCS0 =	0x4B #75 Period of blink = 0.5 sec
      PCS0 =	0xFF
      self.bus.write_byte_data(self.PCA9531_address, frequencyPreScalerAddress, PCS0)      
      self.bus.write_byte_data(self.PCA9531_address, LED_selector_register, Output_Selector)
      self.bus.write_byte_data(self.PCA9531_address, self.PWM_Register0, 255) #Turn off by setting DutyWord to 0
      #self.setPWM(self.CurrentDuty)
    else:
      print('Invalid device=', device,'passed to init in nodeLynkDevs')

  def readTempHum(self, TorH):
    self.bus.write_byte(self.HCPA_5V_U3_address, 0x80)
    time.sleep(0.5)

    # Read data back, 4 bytes
    # humidity msb, humidity lsb, cTemp msb, cTemp lsb
    data = self.bus.read_i2c_block_data(self.HCPA_5V_U3_address, 4)    
    # Convert the data to 14-bits
    if TorH == 'H':
      return int(10.0*((((data[0] & 0x3F) * 256) + data[1]) / 16384.0 * 100.0))
    else:
      cTemp = (((data[2] * 256) + (data[3] & 0xFC)) / 4) / 16384.0 * 165.0 - 40.0
      return int(10.0*((cTemp * 1.8) + 32))   #We prefer F
 
  def setPWM(self, Duty):
    #DutyWord = int((1.0-Duty/100.0) * 255)
    DutyWord = int((Duty/100.0) * 255) 
    self.bus.write_byte_data(self.PCA9531_address, self.PWM_Register0, DutyWord)
    self.CurrentDuty = Duty
  
  def readPWM(self):
    return self.CurrentDuty

    
    
