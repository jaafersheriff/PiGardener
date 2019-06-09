import subprocess
import time
import datetime
import math

def still():
    command = "raspistill -o ./stills/pic" + str(int(math.floor(time.time()))) + ".jpg -th 0:0:0 -awb sun"
    subprocess.call(command, shell=True)
    print "Still"

while True:
    now = datetime.datetime.now()
    if((now.time().hour >= 21 or now.time().hour < 9) and int(math.floor(time.time() % 3600)) == 3599):
        still()
    time.sleep(1)

