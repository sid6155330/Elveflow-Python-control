from tkinter import *
from tkinter import *
import tkinter as tk
from threading import Thread

def scanning():
    while True:
        print ("hello")
        if stop == 1:   
         break   #Break while loop when stop = 1

def start_thread():
        # Assign global variable and initialize value
    global stop
    stop = 0

        # Create and launch a thread 
    t = Thread (target = scanning)
    t.start()

def stop():
        # Assign global variable and set value to stop
    global stop
    stop = 1

root = tk.Tk()
root.title("Title")
root.geometry("500x500")

app = Frame(root)
app.grid()

start = Button(app, text="Start Scan",command=start_thread)
stop = Button(app, text="Stop",command=stop)

start.grid()
stop.grid()
root.mainloop()





def b1():
    global running

    running = True
    
    loop()
    
def loop():    
    set_channel = int(1)  # convert to int
    set_channel = c_int32(set_channel)  # convert to c_int32
    increment = 5  # convert to int
    data_sens = c_double(0)
    get_pressure = c_double(0)
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    
    #repeat =True
    data_sens = c_double(0)
    
    while data_sens.value <= 1500:
        set_pressure = float(increment)
        set_pressure = c_double(set_pressure)  # convert to c_double
        error0 = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)
        error1 = OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
        print('pressure in ch', set_channel.value, ': ', get_pressure.value)
        data_sens = c_double()
        error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
        print('Flow ch', set_channel.value, ': ', data_sens.value)
        if data_sens.value > int(textBox2.get("1.0","end-1c")):
            increment = increment - 0.1
        else:
            increment = increment + 0.1
    if running:
        root.after(100, loop)  # funcion's name without ()
    else:
        print('STOP')
        
def b2(): 
    global running
    
    running = False
    
# --- main ---

running = True
but1 = Button(root, text="flow2", command= b1).pack(pady=20, padx=20)
but2 = Button(root, text="flow2 off", command= b2).pack(pady=20, padx=20)