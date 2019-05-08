from random import randint
import datetime
from time import sleep
import matplotlib
import spidev

from time import sleep
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

def poll_sensor(channel):
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    r = spi.xfer2([1,cbyte,0])
    return ((r[1] & 31) << 6) + (r[2] >> 2)


while True:
    writeData = open('sampleText.txt', 'w')
    x = datetime.datetime.now()
    if Debug == True:
        y= randint(50, 65)
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
    sleep(60)