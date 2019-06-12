import subprocess
import time
import datetime
import math

CAPTURE_TIME = 5

def still():
    filename = "./stills/pic" + str(int(math.floor(time.time()))) + ".jpg"
    command = "raspistill -o " + filename + " -th 0:0:0 -awb sun -n"
    subprocess.call(command, shell=True)
    print "Still: " + filename

while True:
    now = datetime.datetime.now()
    if((now.time().hour >= 21 or now.time().hour < 9) and int(math.floor(time.time() % CAPTURE_TIME)) == CAPTURE_TIME - 1):
        still()
    time.sleep(1)

