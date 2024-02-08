import sys
from email.header import UTF8
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/DLL64')#add the path of the library here
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/Python/Python_64')#add the path of the LoadElveflow.py

from ctypes import *

from array import array

from Elveflow64 import *

#
# Initialization of OB1 ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
#
Instr_ID=c_int32()
print("Instrument name and regulator types are hardcoded in the Python script")
#see User Guide to determine regulator types and NIMAX to determine the instrument name
error=OB1_Initialization('COM8'.encode('ascii'),0,0,0,0,byref(Instr_ID))
#all functions will return error codes to help you to debug your code, for further information refer to User Guide
print('error:%d' % error)
print("OB1 ID: %d" % Instr_ID.value)

#add one digital flow sensor with water calibration, all information to declare sensors are described in the User Guide
error=OB1_Add_Sens(Instr_ID, 1, 4, 1, 0, 7, 0)
#(CustomSens_Voltage_5_to_25 only works with CustomSensors and OB1 from 2020 and after)
print('error add digit flow sensor:%d' % error)

#
# Set the calibration type
#

Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
repeat = True
while repeat == True:
    answer = input('select calibration type (default, load, new ) : ')
    # answer='default'#test purpose only
    Calib_path = 'C:\\Users\\Public\\Desktop\\Calibration\\Calib.txt'
    if answer == 'default':
        error = Elveflow_Calibration_Default(byref(Calib), 1000)
        # for i in range (0,1000):
        # print('[',i,']: ',Calib[i])
        repeat = False
    if answer == 'load':
        error = Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
        # for i in range (0,1000):
        # print('[',i,']: ',Calib[i])
        repeat = False

    if answer == 'new':
        OB1_Calib(Instr_ID.value, Calib, 1000)
        # for i in range (0,1000):
        # print('[',i,']: ',Calib[i])
        error = Elveflow_Calibration_Save(Calib_path.encode('ascii'), byref(Calib), 1000)
        print('calib saved in %s' % Calib_path.encode('ascii'))
        repeat = False



set_channel = int(1)  # convert to int
set_channel = c_int32(set_channel)  # convert to c_int32
set_pressure = float(10)
set_pressure = c_double(set_pressure)  # convert to c_double
error = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)
get_pressure=c_double()
error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000)#Acquire_data=1 -> read all the analog values
print('error: ', error)
print('ch',set_channel.value,': ',get_pressure.value)

data_sens = c_double()
error = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1,
                          byref(data_sens))  # Acquire_data=1 -> read all the analog values
print('Press or Flow ch', set_channel.value, ': ', data_sens.value)



