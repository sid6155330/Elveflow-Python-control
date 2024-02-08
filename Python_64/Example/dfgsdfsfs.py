# tested with Python 3.6.10 (IDE Notepad++ v8.5.4)
# add python_xx and python_xx/DLL to the project path
# coding: utf8

import sys
from email.header import UTF8

sys.path.append(
    'C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/DLL64')  # add the path of the library here
sys.path.append(
    'C:/Users/z5295082/Desktop/Elveflow_software_SDK/ESI_V3_08_02/ESI_V3_08_02/SDK_V3_08_02/DLL/Python/Python_64')  # add the path of the LoadElveflow.py

from ctypes import *

from array import array

from Elveflow64 import *

#
# Initialization of OB1 ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
#
Instr_ID = c_int32()
print("Instrument name and regulator types are hardcoded in the Python script")
# see User Guide to determine regulator types and NIMAX to determine the instrument name
error = OB1_Initialization('COM8'.encode('ascii'), 0, 0, 0, 0, byref(Instr_ID))
# all functions will return error codes to help you to debug your code, for further information refer to User Guide
print('error:%d' % error)
print("OB1 ID: %d" % Instr_ID.value)

# add one digital flow sensor with water calibration, all information to declare sensors are described in the User Guide
error = OB1_Add_Sens(Instr_ID, 1, 4, 1, 0, 7, 0)
# (CustomSens_Voltage_5_to_25 only works with CustomSensors and OB1 from 2020 and after)
print('error add digit flow sensor:%d' % error)

# add one analog flow sensor
# error=OB1_Add_Sens(Instr_ID, 1, 5, 0, 0, 7, 0)
# (CustomSens_Voltage_5_to_25 only works with CustomSensors and OB1 from 2020 and after)
# print('error add analog flow sensor:%d' % error)


#
# Set the calibration type
#

Calib = (c_double * 1000)()  # always define array this way, calibration should have 1000 elements
Calib_path = 'C:\\Users\\Public\\Desktop\\Calibration\\Calib.txt'
error= Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)


