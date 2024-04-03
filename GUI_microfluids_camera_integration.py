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
import cv2 as cv
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
import sys
from email.header import UTF8
from tkinter.ttk import Progressbar
import itertools
color_iteration = itertools.cycle(('blue', 'green', 'orange', 'red', 'yellow'))

import zwoasi as asi

##################### Path, Ports, Channel, Serial numbers etc. ###############

sys.path.append('C:/Users/z5295082/Desktop/Microfluidics_Camera_application/DLL64')#Add the path of the library here
sys.path.append('C:/Users/z5295082/Desktop/Microfluidics_Camera_application/Python_64')#Add the path of the LoadElveflow.py
Calib_path = ('C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt') #Load calibration path/ new calibration path
camera_path =r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/x64/ASICamera2.dll" #ZWO ASI camera DLL path
folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/' #Your captured images will be saved here
main_folder=r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application" # main folder
KDC101_Kinesis_folder= r"C:\Program Files\Thorlabs\Kinesis"
Autofocus_temp_images =r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/Autofocus_temp"



ob1_com_port =str("COM3") #COM port to which OB1 is connected to. Refer to Elveflow SDK userguide for this!
ob1_channel_number=1 #OB1 channel number e.g, 1,2,3 or 4 
mux_com_port =str("ASRL7::INSTR") #COM port to which MUX Distributor is connected to. Refer to Elveflow SDK userguide for this!
ELL9K_com_port=str("COM10") #COM port to which Thorlabs ELL9K is connected to. Identify the port with ELLO software
KDC101_serial_num=b"27005335" # serial number of your Thorlabs KDC101
###############################################################################

## Initialize in the begenning 
import zwoasi as asi
import os
asi.init(camera_path)
num_cameras = asi.get_num_cameras()
print (num_cameras)
camera = asi.Camera(0)
#camera1 = asi.Camera(0)
camera.set_control_value(asi.ASI_FAN_ON, 1)
camera.set_control_value(asi.ASI_COOLER_ON,1)



from ctypes import *
from array import array
from Elveflow64 import *
import time

# Initialization of OB1 ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
Instr_ID = c_int32()
print("Instrument name and regulator types are hardcoded in the Python script")
# see User Guide to determine regulator types and NIMAX to determine the instrument name
error = OB1_Initialization(ob1_com_port.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))
# all functions will return error codes to help you to debug your code, for further information refer to User Guide
print('error:%d' % error)
print("OB1 ID: %d" % Instr_ID.value)
# add one digital flow sensor with water calibration, all information to declare sensors are described in the User Guide
error = OB1_Add_Sens(Instr_ID, 1, 4, 1, 0, 7, 0)
print('error add digit flow sensor:%d' % error)


########################## Setting up canvas and background art ###############

root = tk.Tk()
root.title("Elveflow & ASI Camera Control with Python")
C = tk.Canvas(root,height=1200, width=1800)
#URL = 'https://i.pinimg.com/originals/0f/19/b2/0f19b29838a5f696f6691e8dcde89ba2.png'
#my_page = urlopen(URL)
#imgURL = io.BytesIO(my_page.read())
#filename1= ImageTk.PhotoImage(Image.open(imgURL))
#background_label = Label(root, image=filename1)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
#root.configure(bg="black")
#root.configure(background='SystemButtonFace')
root.config(background='#fafafa')
C.create_oval(1700,450, 1730,480,fill="green")
C.pack()

#################### Text Boxes and labels ####################################
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

def asi_roi_width():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox14 = Text(root, height=1, width=5)
textBox14.place(x=1200, y=310)  # replace values with required

def asi_roi_height():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox15 = Text(root, height=1, width=5)
textBox15.place(x=1300, y=310)  # replace values with required

def KDC101_increment():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox16 = Text(root, height=1, width=5)
textBox16.place(x=1410, y=480)  # replace values with required

def KDC101_Focus1():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox17 = Text(root, height=1, width=10)
textBox17.place(x=1225, y=915)  # replace values with required

def KDC101_Focus2():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox18 = Text(root, height=1, width=10)
textBox18.place(x=1315, y=915)  # replace values with required


def asi_WB_blue():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox19 = Text(root, height=1, width=5)
textBox19.place(x=1410, y=310)  # replace values with required

def asi_WB_red():
    inputValue = textBox.get("1.0", "end-1c") 
    print(inputValue)
textBox20 = Text(root, height=1, width=5)
textBox20.place(x=1480, y=310)  # replace values with required

# def pressure_lock():
#     inputValue = textBox.get("1.0", "end-1c") 
#     print(inputValue)
# textBox21 = Text(root, height=1, width=5)
# textBox21.place(x=1420, y=730)  # replace values with required

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
buttonCommit10 = Label(root, height=2, width=12, text="Exposure (ms)", font='Helvetica 9 bold') #\u00B5
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


####### Set new_calib_label
buttonCommit23 = Label(root, height=5, width=25, text="NB: THE WINDOW WILL \n FREEZE FOR ~3min \n DURING THIS STEP", font='Helvetica 9 bold')
buttonCommit23.place(x=23, y=478)

####### ASI ROI Label (width)
buttonCommit24 = Label(root, height=2, width=15, text="ROI_width \n (multiples of 8)", font='Helvetica 9 bold')
buttonCommit24.place(x=1180, y=270)

####### ASI ROI Label (height)
buttonCommit25 = Label(root, height=2, width=15, text="ROI_height \n (multiples of 8)", font='Helvetica 9 bold')
buttonCommit25.place(x=1280, y=270)


###### Thorlabs  Elliptek ELL9K Label 
buttonCommit26 = Label(root, height=3, width=23, text="THORLABS ELL9K Control ", font='Helvetica 18 bold')
buttonCommit26.place(x=1000, y=340)

###### Thorlabs  Elliptek KDC101 Label 
buttonCommit27 = Label(root, height=3, width=23, text="THORLABS KDC101 Control ", font='Helvetica 18 bold')
buttonCommit27.place(x=1400, y=340)

##### Thorlabs KDC101 increment Label
buttonCommit28 = Label(root, height=4, width=15, text="Step Size\n (1 unit Step \n = 28 \u00B5m )", font='Helvetica 9 bold')
buttonCommit28.place(x=1380, y=400)
 
##### Thorlabs KDC101 increment LED Label
buttonCommit29 = Label(root, height=1, width=15, text="STATE", font='Helvetica 9 bold')
buttonCommit29.place(x=1660, y=420)

##### Thorlabs KDC101 Focus1 Label
buttonCommit30 = Label(root, height=2, width=15, text="Focus 1\n (490nm)", font='Helvetica 9 bold')
buttonCommit30.place(x=1210, y=875)

##### Thorlabs KDC101 Focus2 Label
buttonCommit31 = Label(root, height=2, width=15, text="Focus 2\n (660nm)", font='Helvetica 9 bold')
buttonCommit31.place(x=1295, y=875)


##### Thorlabs asi WB_blue Label
buttonCommit32 = Label(root, height=2, width=10, text="WB_Blue", font='Helvetica 9 bold')
buttonCommit32.place(x=1400, y=270)

##### Thorlabs asi WB_red Label
buttonCommit33 = Label(root, height=2, width=10, text="WB_Red", font='Helvetica 9 bold')
buttonCommit33.place(x=1470, y=270)

####### note for flow lock label
buttonCommit34 = Label(root, height=5, width=30, text="NB: To create a statioinay chamber \n with NO FLUID FLOW, please set the \n flow rate to 'Zero' ", font='Helvetica 9 bold')
buttonCommit34.place(x=1430, y=680)



####### Set pressure label Lock
# buttonCommit34 = Label(root, height=2, width=15, text="PRESSURE LOCK \n (0-2000 mBar)", font='Helvetica 9 bold')
# buttonCommit34.place(x=1380, y=680)


############################### OB1 ###########################################



def initialize_OB1():
    OB1_Initialization(ob1_com_port.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))

my_btn5 = Button(root, text="Initialize OB1", command=initialize_OB1).place(x=200, y=200)

def destruct_OB1():
    OB1_Destructor(Instr_ID.value)

my_btn4 = Button(root, text="Destruct OB1", command=destruct_OB1).place(x=200, y=300)





def load_calib():
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    #Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
    Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib loaded')
my_btn = Button( root, text="Load Calibration", command= load_calib).place(x=195, y=400)

  
def realcallback():
    print('Firing now!')


def new_calib():
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    #Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
    OB1_Calib(Instr_ID.value, Calib, 1000)
    Elveflow_Calibration_Save(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib saved in %s' % Calib_path.encode('ascii')) 
my_btn1 = Button(root, text="New Calibration", command= new_calib).place(x=195, y=500)



        
######################## Start Flow and Stop Flow #############################

from tkinter import *
from tkinter import *
import tkinter as tk
from threading import Thread

def scanning():
    set_channel = int(ob1_channel_number)  # convert to int
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


################################# MUX #########################################

def MUX_start():
    error = MUX_DRI_Initialization(mux_com_port.encode('ascii'), byref(Instr_ID))
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

#################### Pressure vs Time, dynamic plots ##########################

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
    set_channel=int(ob1_channel_number)#convert to int
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

######################## ASI Camera Capture and Properties ####################

from PIL import Image
import os
import time

#### Initialize camera
def initialize_camera():
    #filename="C:/Users/z5295082/Desktop/python-zwoasi-master"
    import zwoasi as asi
    #asi.init(r"C:/Users/z5295082/Desktop/Microfluidics_Camera_application/x64/ASICamera2.dll")
    #asi.init(camera_path)
    #num_cameras = asi.get_num_cameras()
    #camera = asi.Camera(0)
    #camera_info = camera.get_camera_property()
    # Use minimum USB bandwidth permitted
    #camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])
    # Set some sensible defaults. They will need adjusting depending upon
    # the sensitivity, lens and lighting conditions used.
    #camera.disable_dark_subtract()

       
my_btn12 = Button(root, text="Initalize ASI \n Camera", command=initialize_camera).place(x=1000, y= 200)


def save_image_8bit():


    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    #folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(folder)
    print('Capturing a single 8-bit mono image')
    filename_img = 'image_mono.tiff'
    #filename = 'image_mono.txt'
    camera = asi.Camera(0)
    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
       
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values()) 
    os.rename(folder+filename_img, folder+"8bit_"+str(date_string)+".tiff")

    os.chdir(main_folder)

my_btn13 = Button(root, text="Save Image\n 8bit", command=save_image_8bit).place(x=1000, y= 250)



def save_image_16bit():


    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    #folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    #import zwoasi as asi
    import os
    os.chdir(folder)
    print('Capturing a single 16-bit mono image')
    filename_img = 'image_mono.tiff'
    #filename = 'image_mono.txt'
    camera = asi.Camera(0)
    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
    
    camera.set_image_type(asi.ASI_IMG_RAW16)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")

    os.chdir(main_folder)

my_btn13 = Button(root, text="Save Image\n 16bit", command=save_image_16bit).place(x=1000, y= 300)

############################ STEP1 ############################################

def step1():
    #Initalize OB1
    OB1_Initialization(ob1_com_port.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))
    
    #Load calibration
    Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
    #Calib_path = 'C:\\Users\\z5295082\\Desktop\\Microfluidics_Camera_application\\Calib1.txt'
    Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
    print('calib loaded')
    
    #Initalize MUX
    error = MUX_DRI_Initialization(mux_com_port.encode('ascii'), byref(Instr_ID))
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


################################# STEP 2 ######################################

from tkinter import *
from tkinter import *
import tkinter as tk
from threading import Thread

def scanning1(): 
    set_channel = int(ob1_channel_number)  # convert to int
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


####################################### Step 3 ################################




# def initialize_camera_seq():
#     #filename="C:/Users/z5295082/Desktop/python-zwoasi-master"
#     #import zwoasi as asi
#     #asi.init(camera_path)
#     #num_cameras = asi.get_num_cameras()
#     #camera = asi.Camera(0)
#     camera.set_control_value(asi.ASI_FAN_ON, 1)
#     asi.init(camera_path)
#     num_cameras = asi.get_num_cameras()
#     camera = asi.Camera(0)


#     #camera_info = camera.get_camera_property()
    
#     # Use minimum USB bandwidth permitted
#     #camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])
    
#     # Set some sensible defaults. They will need adjusting depending upon
#     # the sensitivity, lens and lighting conditions used.
#     #camera.disable_dark_subtract()
   
                 
# my_btn15 = Button(root, text="Initalize ASI \n Camera", command=initialize_camera_seq).place(x=1080, y= 830)




def save_image_8bit_as():

    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    #folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    import zwoasi as asi
    import os
    os.chdir(folder)
    print('Capturing a single 8-bit mono image')
    filename_img = 'image_mono.tiff'
    camera = asi.Camera(0)

    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
    
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=filename_img)
    
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"8bit_"+str(date_string)+".tiff")
    os.chdir(main_folder)
    root.after(int(textBox10.get("1.0","end-1c"))*1000,save_image_8bit_as)
    root.after(int(textBox11.get("1.0","end-1c"))*60000,root.destroy) 


my_btn16 = Button(root, text="Sequential Image \n Acquisition (8 bit)", command=save_image_8bit_as).place(x=1450, y= 810)



def save_image_16bit_as():

    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    #folder = r'C:/Users/z5295082/Desktop/Microfluidics_Camera_application/saved_images/'
    #import zwoasi as asi
    import os
    os.chdir(folder)
    print('Capturing a single 16-bit mono image')
    filename_img = 'image_mono.tiff'
    camera = asi.Camera(0)
   
    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
    #camera.set_control_value(asi.ASI_MONO_BIN,4)
    camera.set_image_type(asi.ASI_IMG_RAW16)
    camera.capture(filename=filename_img)
    #save_control_values(filename, camera.get_control_values())
    os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
    os.chdir(main_folder)
    

    root.after(int(textBox10.get("1.0","end-1c"))*1000,save_image_16bit_as)   
    root.after(int(textBox11.get("1.0","end-1c"))*60000,root.destroy)


my_btn17 = Button(root, text="Sequential Image \n Acquisition (16 bit)", command=save_image_16bit_as).place(x=1445, y= 860)


 


def save_image_16bit_slot_stage():
    
    
    #import zwoasi as asi
    import os
    import elliptec   
    
    start_time = time.time()
    ############### Autofocus+ capture (490nm)
    #Move to slider slot 2 (illuminatin: 490nm, filter =535nm)
    ELL9K_slot3() 
    time.sleep(2)   
    #Home first before moving stage
    KDC101() 
    time.sleep(5)
    ##Move Stage to Focus 1  Move stage to a diffrent focus for 490 nm  
    KDC101_Move_to_Focus1()
    time.sleep(5)
    Autofocus2()
    time.sleep(5) # Very crucial otherwise the camera will capture a frame during the stage moving
    ## Capture image
    
    
    date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
    filename_img = 'image_mono.tiff'
    #camera = asi.Camera(0)
    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
    camera.set_image_type(asi.ASI_IMG_RAW16)
    os.chdir(folder)
    print('Capturing a single 16-bit 488nm mono image')
    filename_img = 'image_mono.tiff'
    camera.capture(filename=filename_img)    
    os.rename(folder+filename_img, folder+"16bit_Alexa_488_"+str(date_string)+".tiff")
    os.chdir(main_folder)
    
    ############### Autofocus+ capture (660nm)
    ELL9K_slot4() 
    time.sleep(2) 
    #Home first before moving stage
    KDC101() 
    time.sleep(5)
    ##Move Stage to Focus 2  Move stage to a diffrent focus for 660 nm  
    KDC101_Move_to_Focus2()
    time.sleep(5)
    Autofocus2()
    time.sleep(5) # Very crucial otherwise the camera will capture a frame during the stage moving
    camera.set_roi(start_x=None, start_y=None, width=int(textBox14.get("1.0","end-1c")), height=int(textBox15.get("1.0","end-1c")), bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, int(textBox3.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_EXPOSURE, int(textBox4.get("1.0","end-1c"))*1000)
    camera.set_control_value(asi.ASI_WB_B, int(textBox19.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_WB_R, int(textBox20.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_GAMMA, int(textBox5.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_BRIGHTNESS,int(textBox6.get("1.0","end-1c")))
    camera.set_control_value(asi.ASI_FLIP, int(textBox7.get("1.0","end-1c")))
    camera.set_image_type(asi.ASI_IMG_RAW16)    
    os.chdir(folder)
    print('Capturing a single 16-bit 647nm mono image')
    filename_img_660 = 'image_mono_660.tiff'
    camera.capture(filename=filename_img_660)    
    os.rename(folder+filename_img_660, folder+"16bit_Alexa_647_"+str(date_string)+".tiff")
    os.chdir(main_folder)
        
    
    
    dead_time=round((time.time() - start_time))
    print("--- Autofocusing & Image acquisition took %s seconds ---" % (time.time() - start_time))
    
    # If the autofocusing  & imaging time exceeds the user defined time interval
    user_interval=int(textBox10.get("1.0","end-1c"))

    if dead_time> user_interval:
        new_time=dead_time
    else:
        new_time=(user_interval-(dead_time))
        
    
    root.after(new_time*1000 ,save_image_16bit_slot_stage)
    root.after(int(textBox11.get("1.0","end-1c"))*60000,root.destroy)

my_btn26 = Button(root, text="Sequential Image \n Acquisition (16 bit) \n Alexa 488 + 647", command=save_image_16bit_slot_stage).place(x=1445, y= 910)


#################################### Progress bars ############################


from tkinter import *
from tkinter.ttk import Progressbar
import time


def pressure_bar():
    set_channel = int(ob1_channel_number)  # convert to int
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
    set_channel = int(ob1_channel_number)  # convert to int 
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

############################### ELL9K #########################################
# Make sure Pyserial library is installed
# using this library: https://github.com/roesel/elliptec

def ELL9K_home():
    import elliptec
    controller = elliptec.Controller(ELL9K_com_port)
    sl = elliptec.Slider(controller)
    # Home the slider before usage
    sl.home()
my_btn18 = Button(root, text="Home ELL9K \n Slider", command=ELL9K_home).place(x=1000, y= 450)

def ELL9K_slot1():
    import elliptec
    controller = elliptec.Controller(ELL9K_com_port)
    s2 = elliptec.Slider(controller)
    # Home the slider before usage
    s2.home()
    s2.set_slot(1)
my_btn19 = Button(root, text="Move to \n Slot1", command=ELL9K_slot1).place(x=1100, y= 410)

def ELL9K_slot2():
    import elliptec
    controller = elliptec.Controller(ELL9K_com_port)
    s3 = elliptec.Slider(controller)
    # Home the slider before usage
    s3.home()
    s3.set_slot(2)
my_btn20= Button(root, text="Move to \n Slot2", command=ELL9K_slot2).place(x=1100, y= 460)
    
def ELL9K_slot3():
    import elliptec
    controller = elliptec.Controller(ELL9K_com_port)
    sl = elliptec.Slider(controller)
    # Home the slider before usage
    sl.home()
    sl.set_slot(3)
my_btn21= Button(root, text="Move to \n Slot3", command=ELL9K_slot3).place(x=1180, y= 410)

def ELL9K_slot4():
    import elliptec
    controller = elliptec.Controller(ELL9K_com_port)
    sl = elliptec.Slider(controller)
    # Home the slider before usage
    sl.home()
    sl.set_slot(4)
my_btn22= Button(root, text="Move to \n Slot4", command=ELL9K_slot4).place(x=1180, y= 460)


################### Thorlabs KDC101 ###########################################
# Using this library:https://github.com/Thorlabs/Motion_Control_Examples/tree/main/Python/KCube/KDC101
import time
import os
import sys
from ctypes import *


def KDC101():
    """
    KDC101():
    ------

    Performs all actions of the KDC101
    :return: None
    """

    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)

    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")

    # Set constants
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number

    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))
        
        
        #lib.CC_Home(serial_num)
        #time.sleep(1)
        

        # Set up the device to convert real units to device units
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)

        # Apply these values to the device
        #lib.CC_SetMotorParazmsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2) 
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        print (dev_pos)
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)

        print(f'Position after homing: {real_pos.value}')

        # set a new position in device units
        new_pos_real = c_double(0.0)  # in real units
        new_pos_dev = c_int()
        lib.CC_GetDeviceUnitFromRealValue(serial_num,
                                          new_pos_real,
                                          byref(new_pos_dev),
                                          0)

        print(f'{new_pos_real.value} in Device Units: {new_pos_dev.value}')

        # Move to new position as an absolute move.
        lib.CC_SetMoveAbsolutePosition(serial_num, new_pos_dev)
        time.sleep(0.25)
        lib.CC_MoveAbsolute(serial_num)

        # Close the device
        #lib.CC_Close(serial_num)
        #lib.TLI_UninitializeSimulations()

    return
my_btn23= Button(root, text="Home \n KDC101", command=KDC101).place(x=1500, y= 440)


if __name__ == "__KDC101__":
    KDC101()




def KDC101_Current_Pos():
    
    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)
    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number
    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)       
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2)
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)

        #print(f'Just Current Position: {real_pos.value}')
        Real_Pos=real_pos.value
    return Real_Pos
      




def KDC101_Move_Up():
    """
    KDC101_Move_Up():
    ------

    Performs all actions of the KDC101
    :return: None
    """
    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)

    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")

    # Set constants
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number

    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))

        C.create_oval(1700,450, 1730,480,fill=next(color_iteration))
        
        # Set up the device to convert real units to device units
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)

        # Apply these values to the device
        #lib.CC_SetMotorParazmsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2)
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)
        
        #print(f'Current Position: {real_pos.value}')

        # set a new position in device units
        new_pos_real = c_double(real_pos.value+float(textBox16.get("1.0","end-1c")))  # in real units
        new_pos_dev = c_int()
        lib.CC_GetDeviceUnitFromRealValue(serial_num,
                                          new_pos_real,
                                          byref(new_pos_dev),
                                          0)
        print(f'New Position {new_pos_real.value} in Device Units: {new_pos_dev.value}')
        
        # Move to new position as an absolute move.
        lib.CC_SetMoveAbsolutePosition(serial_num, new_pos_dev)
        time.sleep(0.25)
        lib.CC_MoveAbsolute(serial_num)

    
        # Close the device
        #lib.CC_Close(serial_num)
        #lib.TLI_UninitializeSimulations()
   
    return 
my_btn24= Button(root, text="Move Up", command=KDC101_Move_Up ).place(x=1580, y= 420)


def KDC101_Move_Down():
    """
    KDC101_Move_Down():
    ------

    Performs all actions of the KDC101
    :return: None
    """

    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)

    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")

    # Set constants
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number

    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))
        C.create_oval(1700,450, 1730,480,fill=next(color_iteration))

        # Set up the device to convert real units to device units
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)

        # Apply these values to the device
        #lib.CC_SetMotorParazmsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2)
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        #print (dev_pos)
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)

        #print(f'Current Position : {real_pos.value}')

        # set a new position in device units
        new_pos_real = c_double(real_pos.value-float(textBox16.get("1.0","end-1c")))  # in real units 
        new_pos_dev = c_int()
        lib.CC_GetDeviceUnitFromRealValue(serial_num,
                                          new_pos_real,
                                          byref(new_pos_dev),
                                          0)

        print(f'New Position: {new_pos_real.value} in Device Units: {new_pos_dev.value}')

        # Move to new position as an absolute move.
        lib.CC_SetMoveAbsolutePosition(serial_num, new_pos_dev)
        time.sleep(0.25)
        lib.CC_MoveAbsolute(serial_num)

        # Close the device
        #lib.CC_Close(serial_num)
    #lib.TLI_UninitializeSimulations()

    return 
my_btn25= Button(root, text="Move Down", command=KDC101_Move_Down).place(x=1580, y= 460)

#asi.init(camera_path) 
def Autofocus():
       
          
    blur=5
    focus_score_current= 0.1 #starting value
    import zwoasi as asi      
    #asi.init(camera_path)     
    #num_cameras = asi.get_num_cameras()
    #camera = asi.Camera(0)
    camera_info = camera.get_camera_property()
    print('Capturing a single 16-bit mono image')
    filename_img = 'image_mono.tiff'
    camera.set_roi(start_x=None, start_y=None, width=512, height=512, bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, 200) # Change accordingly
    camera.set_control_value(asi.ASI_EXPOSURE,1000*1000) # Change accordingly (x*1000= x000 micro sec.)
    camera.set_control_value(asi.ASI_WB_B, 99) # Change accordingly
    camera.set_control_value(asi.ASI_WB_R, 99) # Change accordingly
    camera.set_control_value(asi.ASI_GAMMA, 50) # Change accordingly
    camera.set_control_value(asi.ASI_BRIGHTNESS,0) # Change accordingly
    camera.set_control_value(asi.ASI_FLIP, 0) # Change accordingly      
    camera.set_image_type(asi.ASI_IMG_RAW16)    
    
    camera.capture(filename='image_mono.tiff')
    time.sleep (1)
    img = cv2.imread('image_mono.tiff', cv2.IMREAD_GRAYSCALE)
    image_filtered = cv2.medianBlur(img, blur) 
    laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
    focus_score_1= laplacian.var()
    
    KDC101_Move_Up()
    KDC101_Move_Up()
    
    camera.capture(filename='image_mono.tiff')
    time.sleep (1)
    img = cv2.imread('image_mono.tiff', cv2.IMREAD_GRAYSCALE)
    image_filtered = cv2.medianBlur(img, blur) 
    laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
    focus_score_2= laplacian.var()
    
    if focus_score_2 > focus_score_1:
        while True:  
            print('The Sample is Above Focus, Moving Lens Up! ')
            KDC101_Move_Up()
            
            date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
            
            ### Uncomment if you would like to save images too while Autofocussing
            # os.chdir(folder)
            # filename_img = 'image_mono.tiff'
            # camera.capture(filename=filename_img)
            # os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
            # os.chdir(main_folder)
            
            camera.capture(filename=filename_img)
            time.sleep (1)
            focus_score_previous = focus_score_current
            KDC101_Current_Pos()   
            im1 = cv2.imread('image_mono.tiff', cv2.IMREAD_GRAYSCALE)
            Position=KDC101_Current_Pos()
            ###### variance of Laplacian (https://www.zaber.com/articles/autofocus-example)
            
            image_filtered = cv2.medianBlur(im1, blur) 
            laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
            focus_score_current = laplacian.var()
            
            print('Focus Score Current',focus_score_current)
            print('Focus Score Previous',focus_score_previous)
            

            
            if focus_score_current < focus_score_previous:
              #camera.close() 
              KDC101_Move_Down()
              break 
           
    else:
        while True:    
            print('The Sample is Below Focus, Moving Lens Down! ')
            KDC101_Move_Down()
            
            date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
            
            ### Uncomment if you would like to save images too while Autofocussing
            # os.chdir(folder)
            # filename_img = 'image_mono.tiff'
            # camera.capture(filename=filename_img)
            # os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
            # os.chdir(main_folder)
            
            camera.capture(filename=filename_img)
            time.sleep (1)
            focus_score_previous = focus_score_current
            KDC101_Current_Pos()   
            im1 = cv2.imread('image_mono.tiff', cv2.IMREAD_GRAYSCALE)
            Position=KDC101_Current_Pos()
            ###### variance of Laplacian (https://www.zaber.com/articles/autofocus-example)
            
            image_filtered = cv2.medianBlur(im1, blur) 
            laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
            focus_score_current = laplacian.var()
            
            print('Focus Score Current',focus_score_current)
            print('Focus Score Previous',focus_score_previous)
            
 
            
            if focus_score_current < focus_score_previous:
              KDC101_Move_Up()
              #camera.close() 
              break 
        
my_btn27= Button(root, text="Autofocus", command=Autofocus).place(x=1680, y= 500)



def Autofocus2():
    
          
    blur=5
    focus_score_current= 0.1 #starting value
    import zwoasi as asi      
    #asi.init(camera_path)     
    #num_cameras = asi.get_num_cameras()
    #camera = asi.Camera(0)
    #camera_info = camera.get_camera_property()
        
    
    camera.set_roi(start_x=None, start_y=None, width=512, height=512, bins=None, image_type=None)
    camera.set_control_value(asi.ASI_GAIN, 300) # Change accordingly
    camera.set_control_value(asi.ASI_EXPOSURE, 1000*1000) # Change accordingly (x*1000= x000 micro sec.)
    camera.set_control_value(asi.ASI_WB_B, 99) # Change accordingly
    camera.set_control_value(asi.ASI_WB_R, 99) # Change accordingly
    camera.set_control_value(asi.ASI_GAMMA, 50) # Change accordingly
    camera.set_control_value(asi.ASI_BRIGHTNESS,0) # Change accordingly
    camera.set_control_value(asi.ASI_FLIP, 0) # Change accordingly      
    camera.set_image_type(asi.ASI_IMG_RAW16)    
    
    
    filename_img = 'image_mono1.tiff'
    camera.capture(filename='image_mono1.tiff')
    time.sleep (1)
    img = cv2.imread('image_mono1.tiff', cv2.IMREAD_GRAYSCALE)
    image_filtered = cv2.medianBlur(img, blur) 
    laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
    focus_score_1= laplacian.var()
    
    KDC101_Move_Up()
    KDC101_Move_Up()
    
    camera.capture(filename='image_mono2.tiff')
    time.sleep (1)
    img = cv2.imread('image_mono2.tiff', cv2.IMREAD_GRAYSCALE)
    image_filtered = cv2.medianBlur(img, blur) 
    laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
    focus_score_2= laplacian.var()
    
    if focus_score_2 > focus_score_1:
        while True:  
            print('The Sample is Above Focus, Moving Lens Up! ')
            KDC101_Move_Up()
            
            date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
            
            ### Uncomment if you would like to save images too while Autofocussing
            # os.chdir(folder)
            # filename_img = 'image_mono.tiff'
            # camera.capture(filename=filename_img)
            # os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
            # os.chdir(main_folder)
            
            camera.capture(filename='image_mono3.tiff')
            focus_score_previous = focus_score_current
            KDC101_Current_Pos()   
            im1 = cv2.imread('image_mono3.tiff', cv2.IMREAD_GRAYSCALE)
            Position=KDC101_Current_Pos()
            ###### variance of Laplacian (https://www.zaber.com/articles/autofocus-example)
            
            image_filtered = cv2.medianBlur(im1, blur) 
            laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
            focus_score_current = laplacian.var()
            
            print('Focus Score Current',focus_score_current)
            print('Focus Score Previous',focus_score_previous)
            

            
            if focus_score_current < focus_score_previous:
              #camera.close() 
              KDC101_Move_Down()
              break 
           
    else:
        while True:    
            print('The Sample is Below Focus, Moving Lens Down! ')
            KDC101_Move_Down()
            
            date_string = (time.strftime("%Y-%m-%d-%H_%M_%S"))
            
            ### Uncomment if you would like to save images too while Autofocussing
            # os.chdir(folder)
            # filename_img = 'image_mono.tiff'
            # camera.capture(filename=filename_img)
            # os.rename(folder+filename_img, folder+"16bit_"+str(date_string)+".tiff")
            # os.chdir(main_folder)
            
            camera.capture(filename='image_mono4.tiff')
            time.sleep (1)
            focus_score_previous = focus_score_current
            KDC101_Current_Pos()   
            im1 = cv2.imread('image_mono4.tiff', cv2.IMREAD_GRAYSCALE)
            Position=KDC101_Current_Pos()
            ###### variance of Laplacian (https://www.zaber.com/articles/autofocus-example)
            
            image_filtered = cv2.medianBlur(im1, blur) 
            laplacian = cv2.Laplacian(image_filtered, cv.CV_64F)
            focus_score_current = laplacian.var()
            
            print('Focus Score Current',focus_score_current)
            print('Focus Score Previous',focus_score_previous)
            

            
            if focus_score_current < focus_score_previous:
              KDC101_Move_Up()
              #camera.close() 
              break 


def KDC101_Move_to_Focus1():

    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)

    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")

    # Set constants
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number

    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))

        C.create_oval(1700,450, 1730,480,fill=next(color_iteration))
        
        # Set up the device to convert real units to device units
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)

        # Apply these values to the device
        #lib.CC_SetMotorParazmsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2)
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)
        
        #print(f'Current Position: {real_pos.value}')
        f1_pos=float((textBox17.get("1.0","end-1c")))/0.028

        # set a new position in device units
        new_pos_real = c_double(real_pos.value+float(f1_pos))  # in real units
        new_pos_dev = c_int()
        lib.CC_GetDeviceUnitFromRealValue(serial_num,
                                          new_pos_real,
                                          byref(new_pos_dev),
                                          0)
        print(f'New Position {new_pos_real.value} in Device Units: {new_pos_dev.value}')
        
        # Move to new position as an absolute move.
        lib.CC_SetMoveAbsolutePosition(serial_num, new_pos_dev)
        time.sleep(0.25)
        lib.CC_MoveAbsolute(serial_num)

    
        # Close the device
        #lib.CC_Close(serial_num)
        #lib.TLI_UninitializeSimulations()
   
    return 

def KDC101_Move_to_Focus2():

    if sys.version_info < (3, 8):
        os.chdir(KDC101_Kinesis_folder)
    else:
        os.add_dll_directory(KDC101_Kinesis_folder)

    lib: CDLL = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")

    # Set constants
    serial_num = c_char_p(KDC101_serial_num) #Add your device Serial number

    # Open the device
    if lib.TLI_BuildDeviceList() == 0:
        lib.CC_Open(serial_num)
        lib.CC_StartPolling(serial_num, c_int(200))

        C.create_oval(1700,450, 1730,480,fill=next(color_iteration))
        
        # Set up the device to convert real units to device units
        STEPS_PER_REV = c_double(1919.64186)  # for the PRM1-Z8
        gbox_ratio = c_double(1.0)  # gearbox ratio
        pitch = c_double(2.0)

        # Apply these values to the device
        #lib.CC_SetMotorParazmsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        lib.CC_SetMotorParamsExt(serial_num, STEPS_PER_REV, gbox_ratio, pitch)
        
        # Get the device's current position in dev units
        lib.CC_RequestPosition(serial_num)
        time.sleep(0.2)
        dev_pos = c_int(lib.CC_GetPosition(serial_num))
        
        # Convert device units to real units
        real_pos = c_double()
        lib.CC_GetRealValueFromDeviceUnit(serial_num,
                                          dev_pos,
                                          byref(real_pos),
                                          0)
        
        #print(f'Current Position: {real_pos.value}')
        f1_pos=float((textBox18.get("1.0","end-1c")))/0.028

        # set a new position in device units
        new_pos_real = c_double(real_pos.value+float(f1_pos))  # in real units
        new_pos_dev = c_int()
        lib.CC_GetDeviceUnitFromRealValue(serial_num,
                                          new_pos_real,
                                          byref(new_pos_dev),
                                          0)
        print(f'New Position {new_pos_real.value} in Device Units: {new_pos_dev.value}')
        
        # Move to new position as an absolute move.
        lib.CC_SetMoveAbsolutePosition(serial_num, new_pos_dev)
        time.sleep(0.25)
        lib.CC_MoveAbsolute(serial_num)

    
        # Close the device
        #lib.CC_Close(serial_num)
        #lib.TLI_UninitializeSimulations()
   
    return 








# def flow_lock():
#     set_channel = int(ob1_channel_number)  # convert to int
#     set_channel = c_int32(set_channel)  # convert to c_int32
#     pressure_value = float(textBox21.get("1.0","end-1c"))  # convert to float
#     data_sens = c_double(0)
#     get_pressure = c_double(0)
#     Calib = (c_double * 1000)()
#     pressure_value = c_double(pressure_value)  # convert to c_double
#     OB1_Set_Press(Instr_ID.value, set_channel, pressure_value, byref(Calib), 1000)
#     OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
#     print('pressure in ch', set_channel.value, ': ', get_pressure.value)

# my_btn28= Button(root, text="Lock Flow", command=flow_lock).place(x=1480, y= 730)


#root.update()  
root.mainloop()



