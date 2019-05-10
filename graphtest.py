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
import matplotlib.pyplot as plt

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("sampleText.txt","r").read()
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

    plt.clear()
    plt.plot(xList, yList)
    plt.show()

# Setup graph figure
f = Figure(figsize=(2,2), dpi=100)
a = f.add_subplot
# pullData = open("sampleText.txt","r").read()
# dataList = pullData.split('\n')
# xList = []
# yList = []
# for eachLine in dataList:
#     if len(eachLine) > 1:
#         x, y = eachLine.split(',')
#         x = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
#         x = matplotlib.dates.date2num(x)
#         print str(x)
#         print str(y)
#         xList.append(int(x))
#         yList.append(int(y))

       


ani = animation.FuncAnimation(f, animate, interval=1000)
