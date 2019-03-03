import RPi.GPIO as GPIO
import RPI_ADC0832
import time
import atexit
import schedule
import datetime
import threading
import csv

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
                return self.adc.read_adc(0)/255.0
            return 2 # Error! 
        except:
            return 2
            

sensor = ADCComponent(17, 27, 22)
pump = WriteComponent(4)
led = WriteComponent(26)

def writeToCSV():
    try:
        with open('sensor.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(sensor.read())])
    except:
        print("gardener error writing to csv")

def firewater():
    watertime = 3
    waternum = 8.0
    timer = datetime.datetime.now()
    while (datetime.datetime.now() - timer).seconds < watertime:
        pump.turnOn()
        time.sleep(t/b/2)
        pump.turnOff()
        time.sleep(t/b/2)

def start():
    pump.turnOff()
    led.turnOn()
    time.sleep(0.1)
    led.turnOff()

    # 16 hours behind means 9:00 is 16:00 and 21:00 is 05:00
    schedule.every().day.at("17:00").do(led.turnOn)
    schedule.every().day.at("05:00").do(led.turnOff)
    hour = datetime.datetime.now().hour
    if hour >= 17 or hour < 5:
        led.turnOn()
    else:
        led.turnOff()
    drystart = None
    while True:
        if (sensor.read() <= 0.2 and drystart is None):
            writeToCSV()
            drystart = datetime.datetime.now()
        if (drystart is not None and (datetime.datetime.now() - drystart).seconds > 15):
            writeToCSV()
            if (sensor.read() <= 0.2):
                writeToCSV()
                firewater()
                writeToCSV()
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
    if (writecount >= 1800):
        writecount = 0
        writeToCSV()
