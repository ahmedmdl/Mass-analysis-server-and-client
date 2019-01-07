import Gpio_factory as GP
import time

ROW_PINS = [18, 4]
COL_PINS = [10, 9]

kp = GP.KeypadFactory().create_keypad(row=2 , col=2, row_pins= ROW_PINS, col_pins= COL_PINS, repeat= True, repeat_rate= 5, key_delay= 100)
def printkey(key):
    print(key)
kp.registerKeyPressHandler(printkey)
try:
  while(True):
    time.sleep(0.2)
except Exception as e: 
     print(e)
     kp.cleanup()
