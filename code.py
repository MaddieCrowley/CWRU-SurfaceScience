import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
#from matplotlib.lines import Line2D
import itertools
from datetime import datetime
import nidaqmx
from time import sleep
"""
Surface Science Code
"""

def start():
    global startEV,stopEV,stepEV,aMode,save,interval,settleTime
    startEV=float(input("Start eV value "))
    stopEV=float(input("Stop eV value "))
    stepEV=float(input("Step eV value "))
    interval=int(input("Time between points in milliseconds "))
    settleTime=int(input("Time between setting voltage and measurement in milliseconds "))
    aMode=bool(input("Alignment Mode (True or False) "))
    save=bool(input("Save data (True or False) "))

start()

def acq():
    for cnt in itertools.count():
        t = startEV+stepEV*cnt
        with nidaqmx.Task() as anOt, nidaqmx.Task() as anIn:    #Uses nidaqmx to assign channels as analogue out and analogue in
            anOt.ao_channels.add_ao_voltage_chan("Dev1/ao0",min_val=0,max_val=10)
            anIn.ai_channels.add_ai_voltage_chan("Dev1/ai0")

            anOt.write(0.00293*t)#Sets the DAQ output voltage. TBH, I have no idea what this multiplicative constant is, but its in the LabView code, so here it is. 
            sleep(settleTime/1000)
            y=anIn.read()
        if t >= stopEV+stepEV:
            if save:
                vals=np.array([xdata[:],ydata[:]])
                now = datetime.now()
                current_time = now.strftime("%d_%m_%Y--%H-%M-%S")
                #print(current_time)
                np.savetxt(current_time+".csv",(vals[:][:]), delimiter=',')
            break
        yield t,y



def init():
    ax.set_ylim(-10,10)
    ax.set_xlim(startEV,stopEV)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata,ydata)
    return line,
    #line = Line2D(xdata, ydata)
    #ax.add_line(line)

    
fig, ax = plt.subplots()
line,=ax.plot([],[],lw=2)

xdata,ydata=[],[]

def update(data):
    t,y=data
    xdata.append(t)
    ydata.append(y)
    lastt = xdata[-1]
    #if lastt>=xdata[0] + stopEV:
    line.set_data(xdata, ydata)
    return line,



ani = animation.FuncAnimation(fig,update,acq,interval=interval,save_count=100,init_func=init,repeat=aMode)

plt.show()
    
