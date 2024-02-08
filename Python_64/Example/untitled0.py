from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
  
# plot function is created for  
# plotting the graph in  
# tkinter window 
def plot(): 
  
    # the figure that will contain the plot 
    fig = Figure(figsize = (5, 5), 
                 dpi = 100) 
  
    # list of squares 
    y = [i**2 for i in range(101)] 
  
    # adding the subplot 
    plot1 = fig.add_subplot(111) 
  
    # plotting the graph 
    plot1.plot(y) 
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = window)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   window) 
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
# the main Tkinter window 
window = Tk() 
  
# setting the title  
window.title('Plotting in Tkinter') 
  
# dimensions of the main window 
window.geometry("500x500") 
  
# button that displays the plot 
plot_button = Button(master = window,  
                     command = plot, 
                     height = 2,  
                     width = 10, 
                     text = "Plot") 
  
# place the button  
# in main window 
plot_button.pack() 
window.mainloop()






def animate(i):
    Calib = (c_double * 1000)()
    set_channel=int(1)#convert to int
    set_channel=c_int32(set_channel)#convert to c_int32
    get_pressure=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000)#Acquire_data=1 -> read all the analog values
    x_vals.append(next(index))
    y_vals.append(get_pressure.value)
    plt.cla()
    plt.plot(x_vals, y_vals)    
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
plt.show()


def start_thread1():
        # Assign global variable and initialize value
    global stop
    stop = 0

        # Create and launch a thread 
    t = Thread (target = animate)
    t.start()

def stop1():
        # Assign global variable and set value to stop
    global stop
    stop = 1
    
start1 = Button(root, text="Start Plot",command=start_thread1).place(x=700, y=600)
stop1 = Button(root, text="Stop Plot",command=stop1).place(x=750, y=700)


#######################


%matplotlib 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 



plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []

index =count()
def animate(i):
    Calib = (c_double * 1000)()
    set_channel=int(1)#convert to int
    set_channel=c_int32(set_channel)#convert to c_int32
    get_pressure=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000)#Acquire_data=1 -> read all the analog values
    x_vals.append(next(index))
    y_vals.append(get_pressure.value)
    plt.cla()
    plt.plot(x_vals, y_vals)    
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
plt.show()


#####################################


%matplotlib 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 



plt.style.use('fivethirtyeight')
x_vals = []
y1_vals = []
y2_vals = []

index =count()
def animate(i):
    Calib = (c_double * 1000)()
    set_channel=int(1)#convert to int
    set_channel=c_int32(set_channel)#convert to c_int32
    get_pressure=c_double()
    data_sens=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000)#Acquire_data=1 -> read all the analog values
    error1=OB1_Get_Sens_Data(Instr_ID.value,set_channel, 1,byref(data_sens))#Acquire_data=1 -> read all the analog values
    
    
    #ax1 = plt.subplots() 
    x_vals.append(next(index))
    y1_vals.append(get_pressure.value)
    y2_vals.append(data_sens.value)
    plt.cla()
    plt.plot(x_vals, y1_vals)
    plt.plot(x_vals, y2_vals)
    
    
    #plt.cla()
    #ax1.set_xlabel('Time (Sec.)' , fontsize=18) 
    #ax1.set_ylabel('Pressure (mBar)', fontsize=18, color = 'red') 
    #ax1.plot(x_vals, y1_vals, color = 'red') 
    #ax1.tick_params(axis ='y', labelcolor = 'red') 
  
    # Adding Twin Axes
    #ax2 = ax1.twinx() 
    #ax2.set_ylabel('Flow rate (\u00B5L/min)', color = 'blue') 
    #ax2.plot(x_vals, y2_vals, color = 'blue') 
    #ax2.tick_params(axis ='y', labelcolor = 'blue') 
    #x_vals.append(next(index))
    #y_vals.append(get_pressure.value)
    #plt.cla()
    #plt.plot(x_vals, y_vals) 
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
plt.show()

##################

%matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


df = pd.DataFrame({'date': pd.date_range(start = '2020-01-01', end = '2020-04-01', freq = 'D')})
df['ETH'] = 2*df.index + 300 + 100*np.random.randn(len(df))
df['BTC'] = 5*df.index + 13000 + 200*np.random.randn(len(df))


def update(i):
    ax1.cla()
    ax2.cla()

    line1 = ax1.plot(df.loc[:i, 'date'], df.loc[:i, 'ETH'], label = 'ETH Price', color = 'red')
    line2 = ax2.plot(df.loc[:i, 'date'], df.loc[:i, 'BTC'], label = 'BTC Price', color = 'blue')

    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, frameon = True, loc = 'upper left', bbox_to_anchor = (1.15, 1))

    ax1.set_ylim(0.9*df['ETH'].min(), 1.1*df['ETH'].max())
    ax2.set_ylim(0.9*df['BTC'].min(), 1.1*df['BTC'].max())

    ax1.tick_params(axis = 'x', which = 'both', top = False)
    ax1.tick_params(axis = 'y', which = 'both', right = False, colors = 'red')
    ax2.tick_params(axis = 'y', which = 'both', right = True, labelright = True, left = False, labelleft = False, colors = 'blue')

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation = 45)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('ETH Coin Value (USD)')
    ax2.set_ylabel('BTC Coin Value (USD)')

    ax1.yaxis.label.set_color('red')
    ax2.yaxis.label.set_color('blue')

    ax2.spines['left'].set_color('red')
    ax2.spines['right'].set_color('blue')

    plt.tight_layout()


fig, ax1 = plt.subplots(figsize = (6, 4))
ax2 = ax1.twinx()

ani = FuncAnimation(fig = fig, func = update, frames = len(df), interval = 100)

plt.show()


#####################Final
%matplotlib 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 



plt.style.use('fivethirtyeight')
x_vals = []
y1_vals = []
y2_vals = []

index =count()
def animate(i):
    Calib = (c_double * 1000)()
    set_channel=int(1)#convert to int
    set_channel=c_int32(set_channel)#convert to c_int32
    get_pressure=c_double()
    data_sens=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000)#Acquire_data=1 -> read all the analog values
    error1=OB1_Get_Sens_Data(Instr_ID.value,set_channel, 1,byref(data_sens))#Acquire_data=1 -> read all the analog values
    x_vals.append(next(index))
    y1_vals.append(get_pressure.value)
    plt.cla()
    plt.plot(x_vals, y1_vals)    
ani = FuncAnimation(plt.gcf(), animate, interval=1000,cache_frame_data=False)
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
plt.show()

#################
filename="C:/Users/z5295082/Desktop/python-zwoasi-master"
import zwoasi as asi
import os
asi.init(r"C:/Users/z5295082/Desktop/ASICameraPythonDemoByAster-main/ASI_SDK/lib/x64/ASICamera2.dll")
num_cameras = asi.get_num_cameras()
camera = asi.Camera(0)
camera_info = camera.get_camera_property()

camera.set_control_value(asi.ASI_GAIN, 300)
camera.set_control_value(asi.ASI_EXPOSURE, 30000)
camera.set_control_value(asi.ASI_WB_B, 99)
camera.set_control_value(asi.ASI_WB_R, 75)
camera.set_control_value(asi.ASI_GAMMA, 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)

print('Capturing a single 8-bit mono image')
filename = 'image_mono.jpg'
camera.set_image_type(asi.ASI_IMG_RAW8)
camera.capture(filename=filename)
print('Saved to %s' % filename)
#save_control_values(filename, camera.get_control_values())