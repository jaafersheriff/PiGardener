import subprocess
import time
import datetime
import math

import os
import subprocess
import sys

CAPTURE_TIME = 3600

def still():
    filename = "./stills/pic" + str(int(math.floor(time.time()))) + ".jpg"
    command = "raspistill -o " + filename + " -th 0:0:0 -awb sun -n"
    subprocess.call(command, shell=True)
    print "Still: " + filename

while True:
    now = datetime.datetime.now()
    if((now.time().hour >= 21 or now.time().hour < 9) and int(math.floor(time.time() % CAPTURE_TIME)) == CAPTURE_TIME - 1):
        # turn off fan and wait for 5 seconds for it to stop spinning
        os.system("echo raspberry | sudo -S ~/uhubctl/uhubctl -a 0 -p 1 -l 1-1.4")
        time.sleep(5)

        # capture frame 
        still()

        # turn fan back on 
        os.system("echo raspberry | sudo -S ~/uhubctl/uhubctl -a 1 -p 1 -l 1-1.4")

    time.sleep(1)

