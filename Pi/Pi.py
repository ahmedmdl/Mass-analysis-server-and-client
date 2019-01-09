import Gpio_factory as GP
import time

ROW_PINS = [18, 4]
COL_PINS = [10, 9]
ROW_No = 2
COL_No = 2

kp = GP.KeypadFactory().create_keypad(row=ROW_No , col=COL_No, row_pins= ROW_PINS, col_pins= COL_PINS, repeat= True, repeat_rate= 5, key_delay= 100)

def printkey(key):
   print(key)
   with open('Pi_dump.txt','w') as f:  
     f.write(str(key))
     
kp.registerKeyPressHandler(printkey)

try:
  while(True):
    time.sleep(0.2)
except Exception as e: 
     print(e)
     kp.cleanup()
