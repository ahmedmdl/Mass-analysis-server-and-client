import RPi.GPIO as GPIO
import time
from threading import Timer

DEFAULT_KEY_DELAY = 300
DEFAULT_REPEAT_DELAY = 1.0
DEFAULT_REPEAT_RATE = 1.0
DEFAULT_DEBOUNCE_TIME = 10

class KeypadFactory():
    
    #create keypad array
    def keypad_gen(self, row, col):
        arr = []
        for y in range(0, row):
           arr.append([i for i in range(y*col+1, y*col+col+1)])
        print(arr)
        return arr
        
    def create_keypad(self,
                      row= None, col= None,
                      row_pins= None, col_pins= None,
                      key_delay= DEFAULT_KEY_DELAY,
                      repeat= False, repeat_delay= None, repeat_rate= None,
                      gpio_mode= GPIO.BCM):

        #assert(row is None),"Incorrect keypad input, row is None"
        #assert(col is None),"Incorrect keypad input, col is None"
        #assert(row_pins is None),"Incorrect keypad input, row_pins is None"
        #assert(col_pins is None),"Incorrect keypad input, col_pins is None"
        #assert(row != len(row_pins)),"Incorrect keypad input, number of rows not equal to number of row pins "
        #assert(col != len(col_pins)),"Incorrect keypad input, number of col not equal to number of col pins "
        print(row,col,row_pins,col_pins)
        
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
        self._repeat_timer = None                    #all of these repeates are just to avoid switch bouncing
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
        if currTime < self._last_key_press_time + self._key_delay:    #ignore switch bouncing
            return

        if type(channel) is not int:
          return

        if 0 > channel > 40:
            raise ValueError("channel number value:%d is not within limits" % channel)
        print(channel,"ch")
        keyPressed = self.getKey(channel)
        
        if keyPressed is not None:
            if type(keyPressed) is not int:
                raise TypeError("keyPressed type:%s is not int" % type(keyPressed))
                           
            for handler in self._handlers:    #functions to be called on the 
                handler(keyPressed)

            #ignore switch bouncing
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
            GPIO.setup(self._row_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self._row_pins[i], GPIO.FALLING, callback=self._onKeyPress, bouncetime=DEFAULT_DEBOUNCE_TIME)#GPIO.BOTH

    def _setColumnsAsInput(self):
        # Set all columns as input
        for j in range(len(self._col_pins)):
            GPIO.setup(self._col_pins[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def getKey(self,channel):
        keyVal = None
        
        # Scan rows for pressed key
        rowVal = None
        for i in range(len(self._row_pins)):
            if channel == self._row_pins[i]:
                rowVal = i
                break
       #print(rowVal,"row")    
        if rowVal is None: 
            raise ValueError("rowVal is None")
        
        # Scan columns for pressed key
        colVal = None
        for i in range(len(self._col_pins)):
            tmpRead = GPIO.input(self._col_pins[i])
            print(tmpRead,"tmp")
            if tmpRead == 0:
                print(tmpRead,"tmp0")
                colVal = i
                break
            
        if colVal is None:
            raise ValueError("colVal is None")

        keyVal = self._keypad[rowVal][colVal]

        return keyVal

    def cleanup(self):
        if self._repeat_timer is not None:
            self._repeat_timer.cancel()
        GPIO.cleanup()

    def getTimeInMillis(self):
        return time.time() * 1000
