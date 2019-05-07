### Project: "Smart Pot" 132 final project
### Description: Touch screen GUI for Raspberry PI
### app monitors moisture and light levels of a potted plant.
### Features: Touchscreen GUI, Current data on screen, view plotted historical data by day and month

import Tkinter as tk
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from matplotlib.figure import Figure
import datetime
from time import sleep
import spidev

   
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

Demo = True # Use True to activate elements for testing without input data

# class for creating the window
class SmartPot(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # variable containing the frame
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

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
        label = tk.Label(self, text = "Smart Pot", font='Arial, 16')
        label.grid(row=0, column=0, columnspan=5, sticky='nsew')

        moistLabel = tk.Label(self, text = "Moisture Level", padx=10)
        moistLabel.grid(row=1, column=0, sticky='nsew')

        photoLabel = tk.Label(self, text = "Light Level", padx=20)
        photoLabel.grid(row=1, column=1, sticky='nsew')

        moistValueCurrent = tk.Label(self, text="0%", background= 'white', font='Arial, 12', padx=10, pady=5)
        moistValueCurrent.config(relief='sunken')
        moistValueCurrent.grid(row=2, column=0, sticky="nsew")

        photoValueCurrent = tk.Label(self, text="0 lux", background= 'white', font='Arial, 12', padx=10, pady=5)
        photoValueCurrent.config(relief='sunken')
        photoValueCurrent.grid(row=2, column=1, sticky="nsew")

        desiredLabel = tk.Label(self, text="Desired Values", padx=10)
        desiredLabel.grid(row=3, column=0, columnspan=2, sticky='sew')

        moistValueDesired = tk.Label(self, text="0%", background= 'white', font='Arial, 12', padx=10, pady=5)
        moistValueDesired.config(relief='sunken')
        moistValueDesired.grid(row=4, column=0, sticky="nsew")

        photoValueDesired = tk.Label(self, text="0 lux", background= 'white', font='Arial, 12', padx=10, pady=5)
        photoValueDesired.config(relief='sunken')
        photoValueDesired.grid(row=4, column=1, sticky="nsew")

        photoHeartbeat = tk.Label(self, text = "Photo Monitor")
        photoHeartbeat.grid(row=1, column=3, sticky='nsew')

        moistHeartbeat = tk.Label(self, text = "Moisture Monitor")
        moistHeartbeat.grid(row=1, column=4, sticky='nsew')


        # test graph values
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        # basic plot funtions for embedding a photo and moisture monitor graph
        photoplot = FigureCanvasTkAgg(f, self)
        photoplot.draw()
        photoplot.get_tk_widget().grid(row=2, rowspan=6, column=3, sticky="nsew", padx=10, pady=10)

        moistplot = FigureCanvasTkAgg(f, self)
        moistplot.draw()
        moistplot.get_tk_widget().grid(row=2, rowspan=6, column=4, sticky="nsew", padx=10, pady=10)
   
    


    #function for changing listed moisture sensor value
def currentMoisture(channel):
    datetime_current = datetime.datetime.now()
    if Demo == True:
        moisture_level = random.randint(50, 65)
        poll_update = {datetime_current: moisture_level}
        return poll_update
    
    else:
        assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

        if channel:
            cbyte = 0b11000000
        else:
            cbyte = 0b10000000

        r = spi.xfer2([1,cbyte,0])
        return ((r[1] & 31) << 6) + (r[2] >> 2)

        try:    
            channel = 0
            channeldata = poll_sensor(channel)


            voltage = round(((channeldata * 3300)/1024),0)
            moisture_level = round(voltage/280)
            #print moisture_level

            sleep(2)

        finally:
            spi.close()
            #print "/n All cleaned up."
        moisture_level = moisture_level * 10
        return moisture_level

            #function for changing listed moisture sensor value


# def currentPhoto(self):
#     photo_level = 0
#     if Demo == True:
#         # demo number generation
#         photo_level = random.randint(0, 1000)
#         return photo_level
#     else:
#         pass
#         # actual sensor calculation

#         #return photo_level

#create new instance of GUI class
window = SmartPot()
window.mainloop()

