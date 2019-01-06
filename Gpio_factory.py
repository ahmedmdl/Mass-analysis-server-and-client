import RPi.GPIO as GPIO
import time
from threading import Timer

DEFAULT_KEY_DELAY = 300
DEFAULT_REPEAT_DELAY = 1.0
DEFAULT_REPEAT_RATE = 1.0
DEFAULT_DEBOUNCE_TIME = 10

class KeypadFactory():

    def keypad_gen(self,row,col):
        arr = []
        for y in range(0,row):
           arr.append([i for i in range(y*col +1, y*col +col +1)])
        return arr
        
    def create_keypad(self,
                      row= None, col= None,
                      row_pins= None, col_pins= None,
                      key_delay= DEFAULT_KEY_DELAY,
                      repeat= False, repeat_delay= None, repeat_rate= None,
                      gpio_mode= GPIO.BCM):

        if row is None or col is None:
            print("input Not correct")
            return 0

        keypad = self.keypad_gen(row,col)
            
        return Keypad(keypad, row_pins, col_pins, key_delay, repeat, repeat_delay, repeat_rate, gpio_mode)

class Keypad():
    def __init__(self,
                 keypad,
                 row_pins, col_pins,
                 key_delay=DEFAULT_KEY_DELAY,
                 repeat=False, repeat_delay=None, repeat_rate=None,
                 gpio_mode=GPIO.BCM):
        self._handlers = []
        
        self._keypad = keypad
        self._row_pins = row_pins
        self._col_pins = col_pins
        
        self._key_delay = key_delay
        self._repeat = repeat
        self._repeat_delay = repeat_delay
        self._repeat_rate = repeat_rate
        self._repeat_timer = None
        if repeat:
            self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY
            self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
        else:
            if repeat_delay is not None:
                self._repeat = True
                self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
            elif repeat_rate is not None:
                self._repeat = True
                self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY

        self._last_key_press_time = 0
        self._first_repeat = True

        GPIO.setmode(gpio_mode)

        self._setRowsAsInput()
        self._setColumnsAsInput()

    def registerKeyPressHandler(self, handler):
        self._handlers.append(handler)

    def unregisterKeyPressHandler(self, handler):
        self._handlers.remove(handler)

    def clearKeyPressHandlers(self):
        self._handlers = []

    def _repeatTimer(self):
        self._repeat_timer = None
        self._onKeyPress(None)

    def _onKeyPress(self,channel):
        currTime = self.getTimeInMillis()
        if currTime < self._last_key_press_time + self._key_delay:
            return

        keyPressed = self.getKey(c,channel)
        if keyPressed is not None:
            with open('Pi_dump.txt','w') as f:
                x = 'r'+ str(keyPressed[0])
                f.write(x)
                sleep(0.1)
                x = 'c'+ str(keyPressed[1])
                f.write(x)                
            for handler in self._handlers:
                handler(keyPressed)
            self._last_key_press_time = currTime
            if self._repeat:
                self._repeat_timer = Timer(self._repeat_delay if self._first_repeat else 1.0/self._repeat_rate, self._repeatTimer)
                self._first_repeat = False
                self._repeat_timer.start()
        else:
            if self._repeat_timer is not None:
                self._repeat_timer.cancel()
            self._repeat_timer = None
            self._first_repeat = True

    def _setRowsAsInput(self):
        # Set all rows as input
        for i in range(len(self._row_pins)):
            GPIO.setup(self._row_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self._row_pins[i], GPIO.BOTH, callback=self._onKeyPress, bouncetime=DEFAULT_DEBOUNCE_TIME)

    def _setColumnsAsInput(self):
        # Set all columns as output low
        for j in range(len(self._col_pins)):
            GPIO.setup(self._col_pins[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getKey(self,channel):

        keyVal = None
        print("channel %d" % channel)
        # Scan rows for pressed key
        rowVal = None
        for i in range(len(self._row_pins)):
            tmpRead = GPIO.input(self._row_pins[i])
            if tmpRead == 0:
                rowVal = i
                break

        # Scan columns for pressed key
        colVal = None
        for i in range(len(self._col_pins)):
            tmpRead = GPIO.input(self._col_pins[i])
            if tmpRead == 0:
                colVal = i
                break

        # Determine pressed key, if any
        if colVal is not None:
            keyVal = self._keypad[rowVal][colVal]

        return keyVal

    def cleanup(self):
        if self._repeat_timer is not None:
            self._repeat_timer.cancel()
        GPIO.cleanup()

    def getTimeInMillis(self):
        return time.time() * 1000
""""

    ROW_PINS = [4, 17, 18, 27, 22]
    COL_PINS = [9, 10, 24, 23]
    kp = rpi_gpio.KeypadFactory().create_keypad(row= , col= , row_pins= ROW_PINS, col_pins= COL_PINS, repeat= True, repeat_rate= 5, key_delay= 100)
    def printkey(key):
        print(key)
    kp.registerKeyPressHandler(printkey)
    i = raw_input('')
    kp.cleanup()
"""""
