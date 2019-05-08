from random import randint
import datetime
from time import sleep
import matplotlib



while True:
    writeData = open('sampleText.txt', 'w')
    x = datetime.datetime.now()
    y= randint(50, 65)
    writeData.write(str(x) + ',' + str(y))
    writeData.flush()
    strand = (str(x) + ' , ' + str(y))
    print strand
    sleep(60)