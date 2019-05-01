### Project: "Smart Pot" 132 final project
### Description: Touch screen GUI for Raspberry PI
### app monitors moisture and light levels of a potted plant.
### Features: Touchscreen GUI, Current data on screen, view plotted historical data by day and month

from Tkinter import *

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

    def setupGUI(self):
        a1 = Label(self.master, text='Photo Level')
        a1.grid(row = 1, column = 1, columnspan = 2, sticky="W")

        a2 = Label(self.master, text='Moisture Level')
        a2.grid(row= 1, column = 3, columnspan = 2, sticky = 'W')

        b1 = Label(self.master, text = 'Current')
        b1.grid(row = 2, column = 1, columnspan = 2, sticky = 'W')

        b2 = Label(self.master, text = 'Current')
        b2.grid(row = 2, column = 3, columnspan = 2, sticky = 'W')

        a3 = Scale(self.master, orient=HORIZONTAL, length = 100, from_=1.0, to=100)
        a3.grid(row = 3, column = 1, columnspan = 2, sticky = 'W')

        b3 = Scale(self.master, orient=HORIZONTAL, length = 100, from_=1.0, to=100)
        b3.grid(row = 3, column = 3, columnspan = 2, sticky = 'W')

    def currentMoisture(self):
        pass

    def currentPhoto(self):
        pass

window = Tk()
t = GUI(window)
t.setupGUI()
window.mainloop()

