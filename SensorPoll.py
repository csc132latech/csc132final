from random import randint
import datetime
import time
from time import sleep
import matplotlib
import spidev
import RPI.GPIO as IO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


minutes = 2
timer = time.time()
switch_time = time.time() + 60 *minutes
status = "High"

Debug = True

# spi = spidev.SpiDev()
# spi.open(0,0)
# spi.max_speed_hz = 250000

def poll_sensor(channel):
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    r = spi.xfer2([1,cbyte,0])
    return ((r[1] & 31) << 6) + (r[2] >> 2)


while True:
    writeData2 = open('sampleText2.txt', 'a')
    
    timer+= time.time()
    if (timer > switch_time):
        
        #switch status
        if(status == "High"):
            #RPI.GPIO(LOW)
            status = "Low"
            IO.output(18, IO.LOW)
            print("go Low")
        elif(status == "Low"):
            #RPI.GPIO(High)
            status = "High"
            IO.output(18, IO.HIGH)
            
            print(status)
        #apparently 95000000000 is about 1 minute times however many you want
        switch_time = timer + 95000000000 * minutes
        if (debug):
            print timer
            print switch_time
        x = datetime.datetime.now()
        y = IO.input(18)
        writeData2.write(str(x) + ',' + str(y) + '\n')
        writeData.flush()
        console = (str(x) + ' , ' + str(y))
        print console
    writeData = open('sampleText.txt', 'a')
    x = datetime.datetime.now()
    if Debug == True:
        y= randint(50, 195)
    else:
        channel = 0
        channeldata = poll_sensor(channel)


        voltage = round(((channeldata * 3300)/1024),0)
        moisture_level = round(voltage/280)
        y= moisture_level

    writeData.write(str(x) + ',' + str(y) + '\n')
    writeData.flush()
    strand = (str(x) + ' , ' + str(y))
    print strand
    sleep(5)

