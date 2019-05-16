#import libraries and setup GPIO
from random import randint
import datetime
import time
from time import sleep
import matplotlib
import spidev
import RPi.GPIO as IO
IO.setmode(IO.BCM)
IO.setup(18, IO.OUT)

#Global variables
minutes = 1
timer = time.time()
switch_time = time.time() + 60 *minutes
status = "High"

Debug = False

#set up communtion for adc
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

#read moisture sensor
def poll_sensor(channel):
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    r = spi.xfer2([1,cbyte,0])
    return ((r[1] & 31) << 6) + (r[2] >> 2)


while True:
    #
    writeData2 = open('sampleText2.txt', 'a')
    
    timer+= time.time()
    if Debug == True:
        x = datetime.datetime.now()
        y = randint(0,1)
        writeData2.write(str(x)+','+str(y) + '\n')
        writeData2.flush()
    else:
        #light timer logic
         if (timer > switch_time):
            

             #switch status
             if(status == "High"):
                 IO.output(18, 1)
                 status = "Low"
                 IO.output(18, 0)
                 print("go Low")
                 y = IO.input(18)
             elif(status == "Low"):
                 IO.output(18, 0) 
                 status = "High"
                 IO.output(18, 1)
                 #y = IO.input(18)
                
                 print(status)
             #apparently 95000000000 is about 1 minute times however many you want
             switch_time = timer + 95000000000 * minutes
             #x = datetime.datetime.now()
             #writeData2.write(str(x) + ',' + str(y) + '\n')
             #writeData2.flush()
             #console = (str(x) + ' , ' + str(y))
             #print console
    y = IO.input(18)
    x = datetime.datetime.now()
    #write light status to CSV file
    writeData2.write(str(x) + ',' + str(y) + '\n')
    writeData2.flush()
    console = (str(x) + ' , ' + str(y))
    print console
    #WRITE MOISTURE VALUES TO CSV FILE
    writeData = open('sampleText.txt', 'a')
    x = datetime.datetime.now()
    if Debug == True:
        y= randint(50, 100)
    else:
        channel = 0
        channeldata = poll_sensor(channel)


        voltage = round(((channeldata * 3300)/1024),0)
        moisture_level = round(channeldata * 1.2 - 900)
        y= int(moisture_level)

    writeData.write(str(x) + ',' + str(y) + '\n')
    writeData.flush()
    strand = (str(x) + ' , ' + str(y))
    print strand
    #sleep
    sleep(5)

