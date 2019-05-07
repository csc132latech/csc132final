### Project: "Smart Pot" 132 final project
### Description: Touch screen GUI for Raspberry PI
### app monitors moisture and light levels of a potted plant.
### Features: Touchscreen GUI, Current data on screen, view plotted historical data by day and month

import Tkinter as tk
import random
#from time import *
#import spidev

Demo = True # Use True to activate elements for testing without input data

# class for creating the window
class SmartPot(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # variable containing the frame
        container = tk.Frame(self)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary containing the various frames
        self.frames = {}

        frame = HomePage(container, self)

        self.frames[HomePage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        # defaults Home Page to be the first visible
        self.show_frame(HomePage)

    # method for moving a frame to the front of the container
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

# Sets up the Home Page
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Smart Pot")
        label.grid(row=0, column=0, sticky='nsew')

        moistLabel = tk.Label(self, text = "Moisture Level")
        moistLabel.grid(row=1, column=0, sticky='nsew')

        photoLabel = tk.Label(self, text = "Light Level")
        photoLabel.grid(row=1, column=1, sticky='nsew')

        previousdayLabel = tk.Label(self, text = "Previous Day Plot")
        previousdayLabel.grid(row=2, column=1, sticky='nsew')

        sevendayLabel = tk.Label(self, text = "Seven Day Plot")
        sevendayLabel.grid(row=2, column=2, sticky='nsew')
   
    
    #function for changing listed moisture sensor value
    def currentMoisture(self, channel):
        moisture_level = 0
        if Demo == True:
            moisture_level = random.randint(50, 65)
        else:
            #acutal sensor calculation    
            # spi = spidev.SpiDev()
            # spi.open(0,0)
            # spi.max_speed_hz = 250000

            # assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

            # if channel:
            #     cbyte = 0b11000000
            # else:
            #     cbyte = 0b10000000

            # r = spi.xfer2([1,cbyte,0])
            # return ((r[1] & 31) << 6) + (r[2] >> 2)

            # try:
            #     while True:
            #         channel = 0
            #         channeldata = poll_sensor(channel)


            #         voltage = round(((channeldata * 3300)/1024),0)
            #         moisture_level = round(voltage/280)
            #         #print moisture_level

            #         sleep(2)

            # finally:
            #     spi.close()
            #     #print "/n All cleaned up."
        return moisture_level

    #function for changing listed moisture sensor value
    def currentPhoto(self):
        photo_level = 0
        if Demo == True:
            # demo number generation
            photo_level = random.randint(0, 1000)
        else:
            # actual sensor calculation

        return photo_level

#create new instance of GUI class
window = SmartPot()
window.mainloop()

