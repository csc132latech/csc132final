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
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import datetime
from datetime import datetime


Demo = True # Use True to activate elements for testing without input data

# Setup graph figure
f = Figure(figsize=(2,2), dpi=100)
a = f.add_subplot

#Animation function
def animate(i):
    pullData = open("sampleText.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            x = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            x = matplotlib.dates.date2num(x)
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)


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


        # basic plot funtions for embedding a photo and moisture monitor graph
        photoplot = FigureCanvasTkAgg(f, self)
        photoplot.draw()
        photoplot.get_tk_widget().grid(row=2, rowspan=6, column=3, sticky="nsew", padx=10, pady=10)

        moistplot = FigureCanvasTkAgg(f, self)
        moistplot.draw()
        moistplot.get_tk_widget().grid(row=2, rowspan=6, column=4, sticky="nsew", padx=10, pady=10)


            


#create new instance of GUI class
window = SmartPot()
ani = animation.FuncAnimation(f, animate, interval=1000)
window.mainloop()

