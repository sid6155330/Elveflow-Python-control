
import sys
from email.header import UTF8
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/DLL64')#add the path of the library here
sys.path.append('C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/Python/Python_64')#add the path of the LoadElveflow.py

from ctypes import *

from array import array

from Elveflow64 import *

import time
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

Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
Calib_path = 'C:Users/z5295082/Desktop/Calib.txt'
error = Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)

set_channel = int(1)  # convert to int
set_channel = c_int32(set_channel)  # convert to c_int32


increment = 0.1  # convert to int


data_sens=c_double(0)
get_pressure = c_double(0)

repeat=True
while repeat:
    set_pressure = float(13)
    set_pressure = c_double(set_pressure)  # convert to c_double
    error = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)
    error1 = OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
    print('pressure in ch', set_channel.value, ': ', get_pressure.value)
    data_sens = c_double()
    error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
    print('Flow ch', set_channel.value, ': ', data_sens.value)
    #time.sleep(0.5)


#while data_sens.value <= 100:
 #   set_pressure = float(11+increment)
  #  set_pressure = c_double(set_pressure)  # convert to c_double
   # error = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)
#
 #   error1= OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
  #  print('pressure in ch', set_channel.value, ': ', get_pressure.value)
   # #time.sleep(0.6)
    #data_sens = c_double()
    #error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
    #print('Flow ch', set_channel.value, ': ', data_sens.value)






#while data_sens.value <= 100:
    #set_pressure = float(11+increment)
    #set_pressure = c_double(set_pressure)  # convert to c_double
    #error = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)

   # error1= OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib), byref(get_pressure), 1000)
    #print('pressure in ch', set_channel.value, ': ', get_pressure.value)
    #time.sleep(0.6)
    #data_sens = c_double()
   # error2 = OB1_Get_Sens_Data(Instr_ID.value, set_channel, 1, byref(data_sens))
   # print('Flow ch', set_channel.value, ': ', data_sens.value)
   # if data_sens.value >= 100:

       # increment = increment-0.1

#increment += 1






set_pressure = c_double(float(0))
error3 = OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib), 1000)

error4=OB1_Destructor(Instr_ID.value)
