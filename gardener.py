import RPi.GPIO as GPIO
import RPI_ADC0832
import time
import atexit
import schedule
import datetime
import threading
import csv

ERROR_READ = 2

GPIO.setmode(GPIO.BCM)

def exit_handler():
    GPIO.cleanup()
atexit.register(exit_handler)

class WriteComponent: 
    pin = -1
    state = 0

    def __init__(self, pin): 
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.turnOff()

    def turnOn(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = 1

    def turnOff(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = 0

    def toggle(self):
        if (self.state == 0):
            self.turnOn()
        else:
            self.turnOff()

class ADCComponent:
    adc = None

    def __init__(self, cspin, clkpin, iopin):
        self.adc = RPI_ADC0832.ADC0832()
        self.adc.csPin = cspin
        self.adc.clkPin = clkpin
        self.adc.doPin = iopin
        self.adc.diPin = iopin

    def read(self):
        try:
            if(self.adc is not None):
                return 2.0 * self.adc.read_adc(0)/255.0
            return ERROR_READ
        except:
            return ERROR_READ
            

sensor = ADCComponent(17, 27, 22)
pump = WriteComponent(4)
led = WriteComponent(26)

def writeToCSV(wetness):
    if (wetness == ERROR_READ):
        return
    try:
        with open('sensor.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(wetness)])
    except:
        print("gardener error writing to csv")

def firewater():
    pump.turnOn()
    time.sleep(0.85)
    pump.turnOff()
    time.sleep(2)

def start():
    pump.turnOff()
    led.turnOn()
    time.sleep(0.1)
    led.turnOff()

    schedule.every().day.at("21:00").do(led.turnOn)
    schedule.every().day.at("09:00").do(led.turnOff)
    hour = datetime.datetime.now().hour
    if hour >= 21 or hour < 9:
        led.turnOn()
    else:
        led.turnOff()
    drystart = None
    while True:
        wetness = sensor.read()
        print(wetness)
        if (wetness <= 0.4 and drystart is None):
            writeToCSV(wetness)
            drystart = datetime.datetime.now()
        if (drystart is not None and (datetime.datetime.now() - drystart).seconds > 15):
            writeToCSV(sensor.read())
            while (sensor.read() <= 0.7):
                firewater()
                writeToCSV(sensor.read())
            drystart = None
        schedule.run_pending()
        time.sleep(2)

# start infinite job on thread
s = threading.Thread(target = start)
s.daemon = True
s.start()

# keep main thread alive 
writecount = 0
while True:
    time.sleep(1)
    writecount += 1
    if (writecount >= 100):
        writecount = 0
        writeToCSV(sensor.read())
