import subprocess
import time
import datetime
import math

piccount = 0
def still():
    global piccount
    piccount += 1
    command = "raspistill -o ./stills/pic" + str(int(math.floor(time.time()))) + ".jpg -th 0:0:0 -awb sun"
    subprocess.call(command, shell=True)

while True:
    now = datetime.datetime.now()
    if((now.time().hour > 17 or now.time().hour < 5) and int(math.floor(time.time() % 1801)) == 1800):
        still()
    time.sleep(1)

