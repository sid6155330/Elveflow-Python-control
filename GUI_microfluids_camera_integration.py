#!/usr/bin/env python
__author__ = "Siddharth Rawat"
__copyright__ = ""
__credits__ = ["None"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Siddharth Rawat, Shuji Kojima, Adam Micolich"
__email__ = "siddharth.rawat@unsw.edu.au"
__status__ = "Production"

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


from tkinter.ttk import Progressbar
###################################### MF parameters ##################################################
import sys
from email.header import UTF8

sys.path.append('C:/Users/z5295082/Desktop/Microfluidics_Camera_application/DLL64')#add the path of the library here
sys.path.append('C:/Users/z5295082/Desktop/Microfluidics_Camera_application/Python_64')#add the path of the LoadElveflow.py



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
root.title("Elveflow & ASI Camera Control with Python")
C = Canvas(root,height=1000, width=1600)
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


def asi_set_gain():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox3 = Text(root, height=1, width=5)
textBox3.place(x=1100, y=250)  # replace values with required


def asi_Exposure():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox4 = Text(root, height=1, width=8)
textBox4.place(x=1200, y=250)  # replace values with required

def asi_Gamma():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox5 = Text(root, height=1, width=5)
textBox5.place(x=1300, y=250)  # replace values with required

def asi_Brightness():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox6 = Text(root, height=1, width=5)
textBox6.place(x=1410, y=250)  # replace values with required

def asi_Flip():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox7 = Text(root, height=1, width=5)
textBox7.place(x=1100, y=310)  # replace values with required

def flow_rate_set_seq():
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
textBox8 = Text(root, height=1, width=5)
textBox8.place(x=1080, y=720)  # replace values with required


def set_valve_seq():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox9 = Text(root, height=1, width=5)
textBox9.place(x=1220, y=720)  # replace values with required

def time_interval_seq():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox10 = Text(root, height=1, width=5)
textBox10.place(x=1220, y=850)  # replace values with required

def total_acquisition_time_seq():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox11 = Text(root, height=1, width=5)
textBox11.place(x=1350, y=850)  # replace values with required

def set_pressure():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox12 = Text(root, height=1, width=5)
textBox12.place(x=100, y=690)  # replace values with required

def set_pressure_seq():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox13 = Text(root, height=1, width=5)
textBox13.place(x=1080, y=780)  # replace values with required

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
buttonCommit7 = Label(root, height=3, width=23, text="ASI Camera Properties ", font='Helvetica 18 bold')
buttonCommit7.place(x=1000, y=100)

####### ASI Camera Properties Label 
buttonCommit8 = Label(root, height=3, width=26, text="Camera Properties ", font='Helvetica 12 bold')
buttonCommit8.place(x=1130, y=170)

####### ASI gain Label 
buttonCommit9 = Label(root, height=2, width=8, text="Gain ", font='Helvetica 9 bold')
buttonCommit9.place(x=1090, y=215)

####### ASI exposure Label 
buttonCommit10 = Label(root, height=2, width=12, text="Exposure (\u00B5S)", font='Helvetica 9 bold')
buttonCommit10.place(x=1180, y=215)

####### ASI Gamma Label 
buttonCommit11 = Label(root, height=2, width=8, text="Gamma ", font='Helvetica 9 bold')
buttonCommit11.place(x=1300, y=215)


####### ASI Brightness Label 
buttonCommit12 = Label(root, height=2, width=8, text="Brightness", font='Helvetica 9 bold')
buttonCommit12.place(x=1410, y=215)

####### ASI Flip Label 
buttonCommit13 = Label(root, height=2, width=8, text="Flip", font='Helvetica 9 bold')
buttonCommit13.place(x=1090, y=270)

####### Sequential flow Label 
buttonCommit14 = Label(root, height=3, width=30, text="Sequential Flow & Image Acquisition ", font='Helvetica 18 bold')
buttonCommit14.place(x=1000, y=500) 

####### Initialization _sequence 1 
buttonCommit15 = Label(root, height=2, width=10, text="STEP 1: \n Initialization", font='Helvetica 12 bold')
buttonCommit15.place(x=900, y=610)

####### Initialization _sequence 2
buttonCommit15 = Label(root, height=2, width=20, text="STEP 2: \n Flow Reagent 1,2 & 3", font='Helvetica 12 bold')
buttonCommit15.place(x=850, y=700)

###### Initialization _sequence 3
buttonCommit16 = Label(root, height=2, width=15, text=  " SET FLOW RATE \n (40-1000 \u00B5L/min)", font='Helvetica 9 bold')
buttonCommit16.place(x=1040, y=680)


###### Initialization _sequence 4
buttonCommit17 = Label(root, height=2, width=15, text=  " SET VALVE \n (1-12)", font='Helvetica 9 bold')
buttonCommit17.place(x=1180, y=680)



####### Initialization _sequence 5
buttonCommit18 = Label(root, height=2, width=20, text="STEP 3: \n Start Image Acquisition", font='Helvetica 12 bold')
buttonCommit18.place(x=850, y=830)

####### Initialization _sequence 6
buttonCommit19 = Label(root, height=2, width=20, text="TIME INTERVAL \n b/w FRAMES (sec.)", font='Helvetica 9 bold')
buttonCommit19.place(x=1170, y=810)

####### Initialization _sequence 7
buttonCommit20 = Label(root, height=2, width=20, text="TOTAL ACQUISITION \n  TIME (min.)", font='Helvetica 9 bold')
buttonCommit20.place(x=1300, y=810)

####### Set pressure label
buttonCommit21 = Label(root, height=2, width=15, text="SET PRESSURE \n (0-2000 mBar)", font='Helvetica 9 bold')
buttonCommit21.place(x=60, y=650)


####### Set pressure label seq
buttonCommit22 = Label(root, height=2, width=15, text="SET PRESSURE \n (0-2000 mBar)", font='Helvetica 9 bold')
buttonCommit22.place(x=1040, y=745)

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
    Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
    Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib loaded')
    OB1_Destructor(Instr_ID.value)
my_btn = Button( root, text="Load Calibration", command= load_calib).place(x=195, y=400)


def new_calib():
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
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
    increment = int(textBox12.get("1.0","end-1c"))  # convert to int
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

%matplotlib 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import tkinter as tk
from tkinter import ttk


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

#root.title("Pressure/Flow rate Vs. Time Plot")
#cache_frame_data=False save_count=MAX_FRAMES
plt.tight_layout()
#plt.style.use('dark_background')
plt.show() 



######################## ASI Camera display and properties

from PIL import Image
import os
import time




 
#### Initialize camera
def initialize_camera():
    #filename="C:/Users/z5295082/Desktop/python-zwoasi-master"
    import zwoasi as asi
    import os
    asi.init(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/x64/ASICamera2.dll")
    num_cameras = asi.get_num_cameras()
    camera = asi.Camera(0)
    camera_info = camera.get_camera_property()
    # Use minimum USB bandwidth permitted
    camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])
    # Set some sensible defaults. They will need adjusting depending upon
    # the sensitivity, lens and lighting conditions used.
    camera.disable_dark_subtract()
    
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_B, 99)
    camera.set_control_value(asi.ASI_WB_R, 75)
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))

       
my_btn12 = Button(root, text="Initalize ASI \n Camera", command=initialize_camera).place(x=1000, y= 200)


def save_image_8bit():


    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images")
    print('Capturing a single 8-bit mono image')
    filename_img = 'image_mono.tiff'
    #filename = 'image_mono.txt'
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"8bit_"+str(date_string)+".tiff")

    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application")

my_btn13 = Button(root, text="Save Image\n 8bit", command=save_image_8bit).place(x=1000, y= 250)



def save_image_16bit():


    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images")
    print('Capturing a single 8-bit mono image')
    filename_img = 'image_mono.tiff'
    #filename = 'image_mono.txt'
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")

    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application")

my_btn13 = Button(root, text="Save Image\n 16bit", command=save_image_16bit).place(x=1000, y= 300)

################## STEP1

def step1():
    #Initalize OB1
    OB1_Initialization('COM8'.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))
    
    #Load calibration
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
    Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib loaded')
    
    #Initalize MUX
    error = MUX_DRI_Initialization("ASRL7::INSTR".encode('ascii'), byref(Instr_ID))
    print('error:%d' % error)
    print("MUX DRI ID: %d" % Instr_ID.value)
    print('error:%d' % error)
    print("MUX ID: %d" % Instr_ID.value)
     
    #MUX all valves on
    valve_state = (c_int32 * 16)(0)
    for i in range(0, 16):
        valve_state[i] = c_int32(1)
    MUX_Set_all_valves(Instr_ID.value, valve_state, 16)
    
    #MUX home valve
    Answer=(c_char*40)()
    error=MUX_DRI_Send_Command(Instr_ID.value, 0, Answer,40)  # length is set to 40 to contain the whole Serial Number
    print('Answer', Answer.value)

my_btn18 = Button(root, text="Initalize OB1 & MUX", command=step1).place(x=1200, y= 610)


############### STEP 2

from tkinter import *
from tkinter import *
import tkinter as tk
from threading import Thread

def scanning1(): 
    set_channel = int(1)  # convert to int
    set_channel = c_int32(set_channel)  # convert to c_int32
    increment = int(textBox13.get("1.0","end-1c"))  # convert to int
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
        if data_sens.value > int(textBox8.get("1.0","end-1c")):

          increment = increment - 0.1
        else:
          increment = increment + 0.1
        #time.sleep(0.1)
        if stop == 1:   
         break   #Break while loop when stop = 1

def start_thread1():
        # Assign global variable and initialize value
    global stop
    stop = 0

        # Create and launch a thread 
    t = Thread (target = scanning1)
    t.start()

def stop1():
    # Assign global variable and set value to stop
    global stop
    stop = 1
    Calib = (c_double * 1000)()
    set_pressure = float(0)
    set_pressure = c_double(set_pressure)  # convert to c_double
    error=OB1_Set_Press(Instr_ID.value, 1, set_pressure, byref(Calib), 1000)
    
start1 = Button(root, text="Start flow",command=start_thread1).place(x=1310, y=710)
stop1 = Button(root, text="Stop flow",command=stop1).place(x=1310, y=740)

def MUX_set_valve_seq():
    valve2 = c_double()
    Valve2 = int((textBox9.get("1.0","end-1c")))  # convert to int
    Valve2 = c_int32(Valve2)  # convert to c_int32
    MUX_DRI_Set_Valve(Instr_ID.value, Valve2,0)  # you can select valve rotation way, either shortest, clockwise or counter clockwise (only for MUX Distribution and Recirculation)
my_btn14 = Button(root, text="MUX Set Valve", command=MUX_set_valve_seq).place(x=1200, y=750)


####################################### Step 3


def initialize_camera_seq():
    #filename="C:/Users/z5295082/Desktop/python-zwoasi-master"
    import zwoasi as asi
    import os
    asi.init(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/x64/ASICamera2.dll")
    num_cameras = asi.get_num_cameras()
    camera = asi.Camera(0)
    camera_info = camera.get_camera_property()
    # Use minimum USB bandwidth permitted
    camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])
    # Set some sensible defaults. They will need adjusting depending upon
    # the sensitivity, lens and lighting conditions used.
    camera.disable_dark_subtract()
    
    camera.set_control_value(asi.ASI_GAIN, 300)
    camera.set_control_value(asi.ASI_EXPOSURE, 30000)
    camera.set_control_value(asi.ASI_WB_B, 99)
    camera.set_control_value(asi.ASI_WB_R, 75)
    camera.set_control_value(asi.ASI_GAMMA, 50)
    camera.set_control_value(asi.ASI_BRIGHTNESS,50)
    camera.set_control_value(asi.ASI_FLIP, 0)

       
my_btn15 = Button(root, text="Initalize ASI \n Camera", command=initialize_camera_seq).place(x=1080, y= 830)






def save_image_8bit_as():

    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images")
    print('Capturing a single 8-bit mono image')
    filename_img = 'image_mono.tiff'
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"8bit_"+str(date_string)+".tiff")
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application")
    root.after(int(textBox10.get("1.0","end-1c"))*1000,save_image_8bit_as)
    root.after(int(textBox11.get("1.0","end-1c"))*60000,root.destroy)


my_btn16 = Button(root, text="Sequential Image \n Acquisition (8 bit)", command=save_image_8bit_as).place(x=1450, y= 810)


def save_image_16bit_as():

    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images")
    print('Capturing a single 16-bit mono image')
    filename_img = 'image_mono.tiff'
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW16)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
    os.chdir(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application")
    root.after(int(textBox10.get("1.0","end-1c"))*1000,save_image_16bit_as)
    root.after(int(textBox11.get("1.0","end-1c"))*60000,root.destroy)


my_btn17 = Button(root, text="Sequential Image \n Acquisition (16 bit)", command=save_image_16bit_as).place(x=1445, y= 860)


#################### Progress bars


from tkinter import *
from tkinter.ttk import Progressbar
import time


def pressure_bar():
    set_channel = int(1)  # convert to int
    set_channel = c_int32(set_channel)  # convert to c_int32
    get_pressure = c_double(0)
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
    pb1['value'] = get_pressure.value
    txt1['text']=pb1['value'],'mBar'
    
    root.update_idletasks()
    root.after(0,pressure_bar)

pb1 = Progressbar(
    root,
    orient = VERTICAL,
    length = 100,
    mode = 'determinate', maximum=200
    )

pb1.place(x=200, y=710)

txt1 = Label(
    root,
    text = '0%',
    bg = '#345',   
    fg = '#fff')

txt1.place(x=180 ,y=680 )

pressure_bar()


def flowrate_bar():
    set_channel = int(1)  # convert to int 
    set_channel = c_int32(set_channel)  # convert to c_int32
    data_sens = c_double(0)
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
    pb2['value'] = data_sens.value
    txt2['text']=pb2['value'],'\u00B5L/min'
    root.update_idletasks()
    root.after(0,flowrate_bar)

pb2 = Progressbar(
    root,
    orient = VERTICAL,
    length = 100,
    mode = 'determinate', maximum=1000
    )

pb2.place(x=300, y=710)

txt2 = Label(
    root,
    text = '0%',
    bg = '#345',   
    fg = '#fff')

txt2.place(x=280 ,y=680 )

flowrate_bar()


root.mainloop()
