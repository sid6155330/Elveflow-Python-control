from tkinter import *
import tkinter as tk
from tkinter import ttk 
#from PIL import ImageTK, Image
from PIL import Image, ImageDraw, ImageTk
from tkinter import filedialog
from collections import defaultdict
from tkinter import messagebox
import matplotlib.pyplot as plt
import cv2
import numpy as np
from urllib.request import urlopen
import io
from skimage.io import imread
from scipy import fftpack as fp
from scipy import fftpack
import webbrowser

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import time

###################################### MF parameters ##################################################
import sys
from email.header import UTF8
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/DLL64')#add the path of the library here
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/Python/Python_64')#add the path of the LoadElveflow.py



from ctypes import *
from array import array
from Elveflow64 import *
import time

# Initialization of OB1 ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
Instr_ID = c_int32()
print("Instrument name and regulator types are hardcoded in the Python script")
# see User Guide to determine regulator types and NIMAX to determine the instrument name
error = OB1_Initialization('COM8'.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))
# all functions will return error codes to help you to debug your code, for further information refer to User Guide
print('error:%d' % error)
print("OB1 ID: %d" % Instr_ID.value)
# add one digital flow sensor with water calibration, all information to declare sensors are described in the User Guide
error = OB1_Add_Sens(Instr_ID, 1, 4, 1, 0, 7, 0)
print('error add digit flow sensor:%d' % error)


########################## Setting up canvas and background art ##############################################

root = tk.Tk()
root.title("Elveflow Control with Python")
C = Canvas(root,height=1000, width=1500)
#URL = 'https://i.pinimg.com/originals/0f/19/b2/0f19b29838a5f696f6691e8dcde89ba2.png'
#my_page = urlopen(URL)
#imgURL = io.BytesIO(my_page.read())
#filename1= ImageTk.PhotoImage(Image.open(imgURL))
#background_label = Label(root, image=filename1)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
#root.configure(bg="black")
#root.configure(background='SystemButtonFace')

root.config(background='#fafafa')



C.pack()


#################### Text Boxes and labels ##################################
def set_valve():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)

##### Set valve text box (insert value)
textBox1 = Text(root, height=1, width=5)
textBox1.place(x=550, y=600)  # replace values with required

##### Set valve label
buttonCommit1 = Label(root, height=2, width=26, text=  " SET VALVE \n (1-12)", font='Helvetica 9 bold')
buttonCommit1.place(x=475, y=558)

def flow_rate_set():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)

##### set flow rate text box (insert value)
textBox2 = Text(root, height=1, width=5)
textBox2.place(x=100, y=605)  # replace values with required


def filepath_asi_set():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
##### set filepath for asi camera (insert location where you would like to save images)
textBox3 = Text(root, height=1, width=30)
textBox3.place(x=1100, y=230)  # replace values with required


#def asi_set_gain():
#    inputValue = textBox.get("1.0", "end-1c")
#    print(inputValue)
##### set filepath for asi camera (insert location where you would like to save images)
#textBox3 = Text(root, height=1, width=30)
#textBox3.place(x=1100, y=230)  # replace values with required

###### OB1 Label 
buttonCommit3 = Label(root, height=3, width=23, text="OB1 MK4 CONTROL ", font='Helvetica 18 bold')
buttonCommit3.place(x=80, y=100)

##### Set flow rate label
buttonCommit4 = Label(root, height=2, width=26, text=  " SET FLOW RATE \n (40-1000 \u00B5L/min)", font='Helvetica 9 bold')
buttonCommit4.place(x=25, y=567)

###### MUX Label 
buttonCommit5 = Label(root, height=3, width=23, text="MUX CONTROL ", font='Helvetica 18 bold')
buttonCommit5.place(x=490, y=100)

##### MUX set valve display
buttonCommit6 = Label(root, height=2, width=26, text=  "DISPLAY \n VALUE", font='Helvetica 9 bold')
buttonCommit6.place(x=480, y=660)

####### ASI Camera Label 
buttonCommit7 = Label(root, height=3, width=23, text="ASI Camera Display ", font='Helvetica 18 bold')
buttonCommit7.place(x=1000, y=100)

####### ASI Camera filepath Label 
buttonCommit8 = Label(root, height=3, width=26, text="Enter Filepath: Save images here ", font='Helvetica 9 bold')
buttonCommit8.place(x=1130, y=170)


############################### OB1 #########################################################
#################################


def initialize_OB1():
    OB1_Initialization('COM8'.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))

my_btn5 = Button(root, text="Initialize OB1", command=initialize_OB1).place(x=200, y=200)

def destruct_OB1():
    OB1_Destructor(Instr_ID.value)

my_btn4 = Button(root, text="Destruct OB1", command=destruct_OB1).place(x=200, y=300)





def load_calib():
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    Calib_path = 'C:\\Users\\z5295082\\Desktop\\Calib1.txt'
    Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib loaded')
    OB1_Destructor(Instr_ID.value)
my_btn = Button( root, text="Load Calibration", command= load_calib).place(x=195, y=400)


def new_calib():
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    Calib_path = 'C:\\Users\\z5295082\\Desktop\\Calib1.txt'
    OB1_Calib(Instr_ID.value, Calib, 1000)
    Elveflow_Calibration_Save(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib saved in %s' % Calib_path.encode('ascii'))
my_btn1 = Button(root, text="New Calibration", command= new_calib).place(x=195, y=500)





#def flow():
#    set_channel = int(1)  # convert to int
#    set_channel = c_int32(set_channel)  # convert to c_int32
#    increment = 10  # convert to int
#    data_sens = c_double(0)
#    get_pressure = c_double(0)
#    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
#    
#    repeat =True
#    data_sens = c_double(0) 
#    while data_sens.value <= 1500:
#            set_pressure = float(increment)
#            set_pressure = c_double(set_pressure)  # convert to c_double
#            error0 = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)
#
#            error1 = OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
#            print('pressure in ch', set_channel.value, ': ', get_pressure.value)
#
#            data_sens = c_double()
#            error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
#            print('Flow ch', set_channel.value, ': ', data_sens.value)
#            if data_sens.value > 100:
#
#                increment = increment - 0.1
#            else:
#                increment = increment + 0.1
#
#            time.sleep(0.1)
            
        
#my_btn3 = Button(root, text="FLOW", command= flow).pack(pady=20, padx=20)

######################################### flow on and off 

from tkinter import *
from tkinter import *
import tkinter as tk
from threading import Thread

def scanning():
    set_channel = int(1)  # convert to int
    set_channel = c_int32(set_channel)  # convert to c_int32
    increment = 1  # convert to int
    data_sens = c_double(0)
    get_pressure = c_double(0)
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements

    repeat =True
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
        #time.sleep(0.1)
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
    Calib = (c_double * 1000)()
    set_pressure = float(0)
    set_pressure = c_double(set_pressure)  # convert to c_double
    error=OB1_Set_Press(Instr_ID.value, 1, set_pressure, byref(Calib), 1000)
    
start = Button(root, text="Start flow",command=start_thread).place(x=175, y=600)
stop = Button(root, text="Stop flow",command=stop).place(x=250, y=600)










######################## MUX ####################################

def MUX_start():
    error = MUX_DRI_Initialization("ASRL7::INSTR".encode('ascii'), byref(Instr_ID))
    print('error:%d' % error)
    print("MUX DRI ID: %d" % Instr_ID.value)
    print('error:%d' % error)
    print("MUX ID: %d" % Instr_ID.value)
my_btn6 = Button(root, text="MUX Initialization", command=MUX_start,bg="#40E0D0").place(x=605, y=200)

def MUX_stop():
    error=MUX_Destructor(Instr_ID.value)
    print('error:%d' % error)
my_btn7 = Button(root, text="MUX Destruct", command=MUX_stop,bg="#40E0D0").place(x=610, y=300)


def MUX_home_valve():
    Answer=(c_char*40)()
    error=MUX_DRI_Send_Command(Instr_ID.value, 0, Answer,40)  # length is set to 40 to contain the whole Serial Number
    print('Answer', Answer.value)
my_btn9 = Button(root, text="MUX Home Valve", command=MUX_home_valve,bg="#40E0D0").place(x=605, y=400)



def MUX_all_valves_on():
    valve_state = (c_int32 * 16)(0)
    for i in range(0, 16):
        valve_state[i] = c_int32(1)
    MUX_Set_all_valves(Instr_ID.value, valve_state, 16)
my_btn8 = Button(root, text="MUX All Valves On", command=MUX_all_valves_on,bg="#40E0D0").place(x=605, y=500)




def MUX_set_valve():
    valve2 = c_double()
    Valve2 = int((textBox1.get("1.0","end-1c")))  # convert to int
    Valve2 = c_int32(Valve2)  # convert to c_int32
    MUX_DRI_Set_Valve(Instr_ID.value, Valve2,0)  # you can select valve rotation way, either shortest, clockwise or counter clockwise (only for MUX Distribution and Recirculation)
my_btn10 = Button(root, text="MUX Set Valve", command=MUX_set_valve,bg="#40E0D0").place(x=612, y=600)


def MUX_get_valve():
    valve = c_int32(-1)
    error = MUX_DRI_Get_Valve(Instr_ID.value, byref(valve))  # get the active valve. it returns 0 if valve is busy.
    print('selected channel', valve.value)

    text_box = Text(
        root,
        height=1,
        width=5)
    text_box.place(x=550, y=700)
    #text_box.pack(expand=False)
    text_box.insert('end', str(valve.value))
    text_box.config(state='disabled')
my_btn11 = Button(root, text="MUX get Valve", command=MUX_get_valve, bg="#40E0D0").place(x=612, y=700)

#################### pressure vs time dynamic plots ###########################

#%matplotlib 
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
    y1_vals.append(data_sens.value)
    y2_vals.append(get_pressure.value)
    plt.cla()
    plt.plot(x_vals, y1_vals, label='Flow rate', linewidth=2)   
    plt.plot(x_vals, y2_vals, label='Pressure',linewidth=2) 
    #plt.plot(figsize = (15,8))
    plt.xlabel('Time(sec.)', fontsize=20)
    plt.ylabel('Flow rate \u00B5L/min) \n Pressure(mBar)', fontsize=20)
    plt.legend(loc='upper left')
    #plt.style.use('dark_background')
ani = FuncAnimation(plt.gcf(), animate, interval=100,cache_frame_data=False)
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
#plt.style.use('dark_background')
plt.show()


######################## ASI Camera display and properties
 
#### Initialize camera
def initialize_camera():
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

       
my_btn12 = Button(root, text="Initalize ASI \n Camera", command=initialize_camera).place(x=1000, y= 200)

def save_image():
    import zwoasi as asi
    import os
    print('Capturing a single 8-bit mono image')
    filename = 'image_mono.jpg'
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=(textBox3.get("1.0","end-1c")))
    print('Saved to %s' % filename)

my_btn13 = Button(root, text="Save Image", command=save_image).place(x=1000, y= 250)


#######################################




root.mainloop()