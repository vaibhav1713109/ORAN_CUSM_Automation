#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : Main_Script.py                                                                      #
# @brief  : This script will call the corresponding functions and operations related to Duplex Types TDD/FDD. #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)            #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################


import re 

# import FDD_Config
# import TDD_Config

from  Script.FDD_Config import FDD
from Script.TDD_Config import TDD
import VXT_Script

import Rest_API_Script
from Rest_API_Script import *

import Generate_SCP
from Generate_SCP import*

import Generate_PCAP_ORB
from Generate_PCAP_ORB import*

import VSA_Constellation
from VSA_Constellation import VSA_Function



# opening the requirement text file in read mode
req = open("C:\ORAN_AUTOMATION1\Script_V1\Requirement.txt", "r")

# reading the file data
data = req.read()

# replacing end splitting the text
# when newline ('\n') is seen.
data_into_list = data.split("\n")

#Assign the requirement to each variables

dup_type = re.sub(' +', '', str(data_into_list[0].split("-")[1]))
#print(dup_type)
band_count = int(data_into_list[1].split("-")[1])
bands = list(data_into_list[2].split("-")[1].split("/"))
phase_comp = data_into_list[3].split("-")[1]
eAxID = re.sub(' +', '', str(data_into_list[4].split("-")[1]))
Base_Folder_Path = re.sub(' +', '', str(data_into_list[5].split("-")[1]))
DL_Center_Freq = data_into_list[6].split("-")[1]
UL_Center_Freq = data_into_list[7].split("-")[1]
Power_Value = int(data_into_list[8].split("-")[1])*(-1)
VXT_Add = str(data_into_list[9].split("-")[1])
Ext_Gain = int(data_into_list[10].split("-")[1])*(-1)
prach_count = int(data_into_list[11].split("-")[1])
formats = list(data_into_list[12].split("-")[1].split("/"))


#close the file
req.close()

'''
#Check for the Duplex type. If matches the requirement, then calls corresponding functions else shows the error
if (dup_type == 'FDD'):
    FDD_Config.FDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
elif (dup_type == 'TDD'):
    TDD_Config.TDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
else:
    print("Please check the Duplex Type given in the requirement")
    
'''
sub_folder = Base_Folder_Path + "/PRACH"
if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
try:
	for i in range (0, prach_count):
		Generate_SCP.ST3_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, formats[i])
		Generate_PCAP_ORB.PRACH(bands, eAxID, sub_folder, formats[i])
		Rest_API_Script.load_play_record_pcap(sub_folder)
		Rest_API_Script.Stop_Player()
		Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
		VSA_Constellation.VSA_Function_PRACH(sub_folder, formats[i])
	print("Script completed Successfully. Please find the results in : ", Base_Folder_Path)
except:
	Rest_API_Script.Stop_Player()
	VXT_Script.RF_OFF(VXT_Add)
	print("Exception Occurred. Player stopped and RF made off")
