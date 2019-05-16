### Project: "Smart Pot" 132 final project
### Description: Touch screen GUI for Raspberry PI
### app monitors moisture and light state of a potted plant.
### Features: Touchscreen GUI, Current data on screen, view plotted historical data by day and month

import Tkinter as tk
import ttk
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
style.use('ggplot')
import datetime
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

#set plot font size
matplotlib.rcParams.update({'font.size': 6})


# Setup graph figure for moisture sensor
f, a = plt.subplots(figsize = (2.75,3))


# Setup graph figure for light IO
g, b =plt.subplots(figsize = (2.75,3))


#Animation moisture function
def animate(i):
    pullData = open("sampleText.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    global a
    desiredval = frame.getmoist()

    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            x = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            # x = matplotlib.dates.date2num(x)
            xList.append((x))
            yList.append(int(y))
            #print str(x)
            #print str(y)

    a.clear() 
    a.plot_date(xList, yList, 'b')  
    a.axhline(desiredval, color = 'k')
    a.set_xlim([(datetime.now() - timedelta(minutes = 1)), datetime.now()])
    a.set_ylim([0,100])

    
    frame.setmoist(y)
    if desiredval > (int(y)+10):
        GPIO.output(23, 1)
    elif desiredval < (int(y)-10):
        GPIO.output(23, 0)
        

    


#Animation Light function
def animatelight(i):
    pullData = open("sampleText2.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    global a
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            x = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            # x = matplotlib.dates.date2num(x)
            xList.append((x))
            yList.append(int(y))
            #print str(x)
            #print str(y)

    b.clear()
    b.plot_date(xList, yList, 'b', color='green')      
    b.set_xlim([(datetime.now() - timedelta(minutes = 1)), datetime.now()])
    b.set_ylim([-0.5,1.5])

    frame.setstate(y)

#button function for switching light
def lightswitch():
    if GPIO.input(18) == 1:
        GPIO.output(18, 0)
    else:
        GPIO.output(18, 1)
    

# class for creating the window
class SmartPot(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        global moistValueCur; moistValueCur = tk.IntVar()
        global photoValueCur; photoValueCur = tk.IntVar()

        #styling
        tk.Tk.wm_title(self, "Smart Pot")

        # variable containing the frame
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary containing the various frames
        self.frames = {}

        global frame; frame = HomePage(container, self)

        self.frames[HomePage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        # defaults Home Page to be the first visible
        self.show_frame(HomePage)

    # method for moving a frame to the front of the container
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# Sets up the Home Page
class HomePage(tk.Frame, SmartPot):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Smart Pot", font='Arial, 16')
        label.grid(row=0, column=0, columnspan=5, sticky='nsew')


        #variable labels for Desired Values
        self.moistValueCur = moistValueCur
        self.photoValueCur = photoValueCur


        #Label for current moisture
        moistLabel = tk.Label(self, text = "Moisture Level")
        moistLabel.grid(row=1, column=0, sticky='nsew')

        #Label for current photo state
        photoLabel = tk.Label(self, text = "Light State", padx=20)
        photoLabel.grid(row=1, column=1, sticky='nsew')

        #Label for current moisture value
        global moistValueCurrent; moistValueCurrent = tk.Label(self, text='0%', background= 'white', font='Arial, 12', padx=10, pady=5)
        moistValueCurrent.config(relief='sunken')
        moistValueCurrent.grid(row=2, column=0, sticky="nsew")
        moistValueCurrent.config(width = 8)

        #Label for current photo state value
        global photoValueCurrent; photoValueCurrent = tk.Label(self, text="0 state", background= 'white', font='Arial, 12', padx=10, pady=5)
        photoValueCurrent.config(relief='sunken')
        photoValueCurrent.grid(row=2, column=1, sticky="nsew")

        #Heading label for desired value
        desiredLabel = tk.Label(self, text="Desired Values", padx=10)
        desiredLabel.grid(row=3, column=0, columnspan=1, sticky='sew')

        #Label for desired moisure
        moistValueDesired = tk.Label(self, textvariable=(self.moistValueCur), background= 'white', font='Arial, 14', padx=10, pady=5)
        moistValueDesired.config(relief='sunken')
        moistValueDesired.grid(row=4, column=0, sticky="nsew")

        #Slider for Moisture
        global moistDesiredSet; moistDesiredSet = tk.Scale(self, from_=0, to=100, orient='horizontal', variable= self.moistValueCur)
        moistDesiredSet.grid(row=5, column=0, sticky='nsew')

        #Label for light i/o button value
        photoValueDesired = tk.Label(self, text='Light Switch', padx = 10)
        photoValueDesired.grid(row=3, column=1, sticky="sew")

        #I/O button for light
        photoDesiredSet = tk.Button(self, text = 'ON/OFF', command = lightswitch)
        photoDesiredSet.grid(row=4, rowspan=2, column=1, sticky='nsew')
        photoDesiredSet.config(width = 5)

        #Label for light plot
        photoHeartbeat = tk.Label(self, text = "Light Monitor")
        photoHeartbeat.grid(row=1, column=3, sticky='nsew')

        #Label for moisture plot
        moistHeartbeat = tk.Label(self, text = "Moisture Monitor")
        moistHeartbeat.grid(row=1, column=4, sticky='nsew')


        #basic plot funtions for embedding a photo and moisture monitor graph
        photoplot = FigureCanvasTkAgg(g, self)
        photoplot.draw()
        photoplot.get_tk_widget().grid(row=2, rowspan=6, column=3, sticky="nsew", padx=2, pady=10)

        moistplot = FigureCanvasTkAgg(f, self)
        moistplot.draw()
        moistplot.get_tk_widget().grid(row=2, rowspan=6, column=4, sticky="nsew", padx=2, pady=10)

    #class function for getting desired moisture value for line graph
    def getmoist(self):
        return moistDesiredSet.get()

    #class function for getting current moisture for label update
    def setmoist(self, val):
        moistValueCurrent['text'] = val + '%'

    #class function for getting current photo state
    def setstate(self, val):
        photoValueCurrent['text'] = val






#create new instance of GUI class
window = SmartPot()

print moistValueCur.get()

#animation moisture plot
ani = animation.FuncAnimation(f, animate, interval=1000)

#animate light plot
ani2 = animation.FuncAnimation(g, animatelight, interval=1000)

window.mainloop()

