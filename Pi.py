import Gpio_factory as GP

ROW_PINS = [4, 17, 18, 27, 22]
COL_PINS = [9, 10, 24, 23]

kp = GP.KeypadFactory().create_keypad(row=5 , col=4, row_pins= ROW_PINS, col_pins= COL_PINS, repeat= True, repeat_rate= 5, key_delay= 100)
def printkey(key):
    print(key)
kp.registerKeyPressHandler(printkey)
try:
  while(True):
    time.sleep(0.2)
    print('hi')
except Exception as e: 
     print(e)
     kp.cleanup()
