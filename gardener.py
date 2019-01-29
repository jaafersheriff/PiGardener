import RPi.GPIO as GPIO
import time
import atexit
import schedule
import datetime
import threading

GPIO.setmode(GPIO.BOARD)

def exit_handler():
    GPIO.cleanup()
atexit.register(exit_handler)

class Component: 
    pin = -1
    state = 0
    mode = GPIO.OUT

    def __init__(self, pin, mode):
        self.pin = pin
        self.mode = GPIO.OUT if mode == "out" else GPIO.IN
        GPIO.setup(pin, self.mode)
        self.turnOff()

    def turnOn(self):
        if(self.mode == GPIO.OUT):
            GPIO.output(self.pin, GPIO.LOW)
            self.state = 1

    def turnOff(self):
        if(self.mode == GPIO.OUT):
            GPIO.output(self.pin, GPIO.HIGH)
            self.state = 0

    def toggle(self):
        if (self.state == 0):
            self.turnOn()
        else:
            self.turnOff()
    
    def read(self):
        if(self.mode == GPIO.IN):
            return GPIO.input(self.pin)
        else:
            return 0

pump = Component(7, "out")
led = Component(37, "out")
sensor = Component(8, "in")

def start():
    pump.turnOff()

    # 16 hours behind means 9:00 is 16:00 and 21:00 is 05:00
    schedule.every().day.at("17:00").do(led.turnOn)
    schedule.every().day.at("05:00").do(led.turnOff)
    hour = datetime.datetime.now().hour
    if hour >= 17 or hour < 5:
        led.turnOn()
    else:
        led.turnOff()
    drystart = None
    drycounting = False
    while True:
        if (sensor.read() == 0 and not drycounting):
            drystart = datetime.datetime.now()
            drycounting = True
        if (drystart is not None and (datetime.datetime.now() - drystart).seconds > 2):
            pump.turnOn()
            time.sleep(1)
            pump.turnOff()
            drystart = None
            drycounting = False
            
        schedule.run_pending()
        time.sleep(1)

# start infinite job on thread
s = threading.Thread(target = start)
s.daemon = True
s.start()

# keep main thread alive 
while True:
    time.sleep(1)
