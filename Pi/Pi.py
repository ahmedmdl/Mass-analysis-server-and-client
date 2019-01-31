import Gpio_factory as GP
import time

ROW_PINS = [18, 4, 27]
COL_PINS = [10, 9, 25]
ROW_No = 3
COL_No = 3

kp = GP.KeypadFactory().create_keypad(row= 3 , col= 3, row_pins= [18, 4, 3], col_pins= [10, 9, 2], repeat= True, repeat_rate= 5, key_delay= 100)

def printkey(key):
   print(key,"key")
   with open('Pi_dump.txt','w') as f:  
     f.write(str(key))
     
kp.registerKeyPressHandler(printkey)

try:
  while(True):
    time.sleep(0.2)
except Exception as e: 
     print(e)
     kp.cleanup()
