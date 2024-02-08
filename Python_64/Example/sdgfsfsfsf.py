# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 13:02:48 2024

@author: z5295082
"""
%matplotlib 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []



index =count()
def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))
    plt.cla()
    plt.plot(x_vals, y_vals)



ani = FuncAnimation(plt.gcf(), animate, interval=1000)
# cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
plt.show()

from tkinter import *

def press(*args):
    print('press')
    global pressed
    pressed = True
    master.after(0, loop)

def release(*args):
    print('release')
    global pressed
    pressed = False

def loop():
    if pressed:
        print('loop')
        # Infinite loop without delay is bad idea.
        master.after(250, loop)

master = Tk()
pressed = False

b = Button(master, text="OK")
b.bind("<Button-1>", press)
b.bind("<ButtonRelease-1>", release)
b.pack()
mainloop()



##########################


def flow2():
    set_channel = int(1)  # convert to int
    set_channel = c_int32(set_channel)  # convert to c_int32
    increment = 10  # convert to int
    data_sens = c_double(0)
    get_pressure = c_double(0)
    Calib = (c_double * 1000)()
    
    repeat= True
    while repeat:
        answer=input('what to do (flow, or exit) : ')
        if answer=='flow':
            while data_sens.value <= 1500:
                set_pressure = float(increment)
                set_pressure = c_double(set_pressure)  # convert to c_double
                error0 = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)

                error1 = OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
                print('pressure in ch', set_channel.value, ': ', get_pressure.value)

                data_sens = c_double()
                error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
                print('Flow ch', set_channel.value, ': ', data_sens.value)
                if data_sens.value > 100:

                    increment = increment - 0.1
                else:
                    increment = increment + 0.1

                time.sleep(0.1)
        if answer == 'exit':
           repeat=False
    #error=OB1_Destructor(Instr_ID.value)
my_btn3x = Button(root, text="FLOW2", command= flow).pack(pady=20, padx=20)





###############


# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

running = True

# Define a function to print the text in a loop
def print_text():
   if running:
      print("Hello World")

   win.after(1000, print_text)

# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False

canvas = Canvas(win, bg="skyblue3", width=600, height=60)
canvas.create_text(150, 10, text="Click the Start/Stop to execute the Code", font=('', 13))
canvas.pack()

# Add a Button to start/stop the loop
start = ttk.Button(win, text="Start", command=on_start)
start.pack(padx=10)

stop = ttk.Button(win, text="Stop", command=on_stop)
stop.pack(padx=10)

# Run a function to print text in window
win.after(1000, print_text)

win.mainloop()

################
import tkinter as tk  # PEP8: `import *` is not preferred
import time

# --- functions ---  # PEP8: all functions before main code

def b1():
    global running

    running = True
    
    loop()
    
def loop():    
    print('MY MAIN CODE')
    
    if running:
        # repeat after 100ms (0.1s)
        top.after(100, loop)  # funcion's name without ()
    else:
        print('STOP')
        
def b2(): 
    global running
    
    running = False
    
# --- main ---

running = True

top = tk.Tk()

but1 = tk.Button(top, text="On",  command=b1)   # PEP8: inside `()` use `=` without spaces
but2 = tk.Button(top, text="Off", command=b2)
but1.pack()
but2.pack()

top.mainloop()