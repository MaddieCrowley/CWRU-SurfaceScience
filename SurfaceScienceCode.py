import matplotlib.pyplot as plt #Handles ploting
import numpy as np #Handles mathematics
import matplotlib.animation as animation #Handles the repetitive graphing without a new figure/plot
import itertools #Handles the production of different values to be plotted on each data point collection
from datetime import datetime #Handles the date and time for production of the save file names
import nidaqmx #Handles communication with the National Instruments DAQ
from time import sleep #Handles waiting between setting voltage and reading the value off of the DAQ
"""
Surface Science Code
"""

def start(): #Sets up the user interface to allow users to change settings without needing to edit the code directly
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
        t = startEV+stepEV*cnt #Generates the eV value to be sent to the DAQ for each count of the iteration
        with nidaqmx.Task() as anOt, nidaqmx.Task() as anIn:    #Uses nidaqmx to assign channels as analogue out and analogue in
            anOt.ao_channels.add_ao_voltage_chan("Dev1/ao0",min_val=0,max_val=10)
            anIn.ai_channels.add_ai_voltage_chan("Dev1/ai0")

            anOt.write(0.00293*t)#Sets the DAQ output voltage. The multiplicative constant relates the voltage output of the DAQ to the corresponding energy of the detector 
            sleep(settleTime/1000) #Waits for a period of milliseconds before reading the voltage from the DAQ
            y=anIn.read()
        if t >= stopEV+stepEV:
            if save: #If the user has decided to save the data, then this stores the data into a convient variable and writes it to a file with the current date and time as the title
                vals=np.array([xdata[:],ydata[:]]) 
                now = datetime.now()
                current_time = now.strftime("%d_%m_%Y--%H-%M-%S")
                np.savetxt(current_time+".csv",(vals[:][:]), delimiter=',')
            del xdata[:] #Deletes the old data to prevent the data arrays from growing past the final value
            del ydata[:]
            break #This halts the repetion from one point to the next, exiting the animation and stopping data collection when the t value reaches one step larger than the stop value
        yield t,y #Returns the values for both t (eV) and y (voltage)



def init(): #Sets up the plotting before the animation runs
    ax.set_ylim(-10,10)
    ax.set_xlim(startEV,stopEV) 
    line.set_data(xdata,ydata)
    return line,

    
fig, ax = plt.subplots() #Creates the plots and line object
line,=ax.plot([],[],lw=2)

xdata,ydata=[],[] #Creates the data arrays

def update(data): #Handles updating the data array after every iteration
    t,y=data
    xdata.append(t)
    ydata.append(y)
    line.set_data(xdata, ydata)
    return line,



ani = animation.FuncAnimation(fig,update,acq,interval=interval,save_count=100,init_func=init,repeat=aMode) #Sets up the animation to use the functions defined above

plt.show() #Shows the plot
    
