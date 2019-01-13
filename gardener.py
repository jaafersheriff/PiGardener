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
    # 16 hours behind means 9:00 is 16:00 and 21:00 is 05:00
    schedule.every().day.at("17:00").do(led.turnOn)
    schedule.every().day.at("05:00").do(led.turnOff)
    # TODO - check time to see where we're at and then turn on/off
    pump.turnOff()
    led.turnOn()
    while True:
        schedule.run_pending()
        time.sleep(1)

s = threading.Thread(target = start)
s.daemon = True
s.start()

time.sleep(4)
 
while True:
    time.sleep(5)
    print("next: " + str(schedule.next_run()))
