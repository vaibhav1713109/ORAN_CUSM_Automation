#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#################################################################################################



import re
import sys
import clr
import os

###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(dir_name)
# print(parent)
sys.path.append(parent)

###############################################################################
## Related Imports
###############################################################################
from Script import Rest_API_Script
from Script import Generate_SCP
from Script import Generate_PCAP_ORB
from Script import VSA_Constellation
from Script import VXT_Script
from Script.M_Plane_conf import *
from Script.BLER_Automation import*
from Script.PN_Sequence import *
from Script.M_Plane_conf import *



def Base_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = "\Base_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Base_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Result = VXT_Script.Constellation_check_DL_TDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'
    # input('Check VXT configuration...')
    
    
def Extended_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = "\Extended_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Extended_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    # VXT_Script.Constellation_check_DL_TDD_repeat(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Result = VXT_Script.Constellation_check_DL_TDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'


def Base_UL(bands, eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add):
    folder_name = "\Base_UL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Base_UL_TDD(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.UL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Rest_API_Script.Stop_Player()
    Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
    VSA_Constellation.VSA_Function(sub_folder)
    #BLER_Automation.BLER_Script(sub_folder)
    #PN_Sequence.PN23_Sequence(sub_folder)
    
def No_Compression_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = r"\No_Compression_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Result = VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'
    
    
def Compression_Static_9bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = "\Compression_Static_9bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 9
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Result = VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'
    
def Compression_Static_12bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = "\Compression_Static_12bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 12
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Result = VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'
    
def Compression_Static_14bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    folder_name = "\Compression_Static_14bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 14
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Result = VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    if Result[0] and Result[1]:
        return 'Pass'
    else:
        return 'Fail'
    
def No_Compression_UL(bands, eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add):
    folder_name = r"\No_Compression_UL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Compression_TDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.UL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Rest_API_Script.Stop_Player()
    Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
    VSA_Constellation.VSA_Function(sub_folder)
    #BLER_Automation.BLER_Script(sub_folder)
    #PN_Sequence.PN23_Sequence(sub_folder)
    
def Compression_Static_9bit_UL(bands, eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add):
    folder_name = "\Compression_Static_9bit_UL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 9
    Generate_SCP.Compression_TDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.UL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Rest_API_Script.Stop_Player()
    Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
    VSA_Constellation.VSA_Function(sub_folder)
    #BLER_Automation.BLER_Script(sub_folder)
    #PN_Sequence.PN23_Sequence(sub_folder)
    
def Compression_Static_12bit_UL(bands, eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add):
    folder_name = "\Compression_Static_12bit_UL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 12
    Generate_SCP.Compression_TDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.UL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Rest_API_Script.Stop_Player()
    Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
    VSA_Constellation.VSA_Function(sub_folder)
    #BLER_Automation.BLER_Script(sub_folder)
    #PN_Sequence.PN23_Sequence(sub_folder)
    
def Compression_Static_14bit_UL(bands, eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add):
    folder_name = "\Compression_Static_14bit_UL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 14
    Generate_SCP.Compression_TDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    Generate_PCAP_ORB.UL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    Rest_API_Script.Stop_Player()
    Generate_PCAP_ORB.Generate_ORB(sub_folder, eAxID)
    VSA_Constellation.VSA_Function(sub_folder)
    #BLER_Automation.BLER_Script(sub_folder)
    #PN_Sequence.PN23_Sequence(sub_folder)
    
#def ST3_NR_PRACH(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add):

    



def TDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):
    
    Rest_API_Script.sync_creation()
    #a = input("Please enter once sync done and Carrier added successfully")
    
    for i in range(0,band_count):
        bands[i] = re.sub(' +', '', str(bands[i]))
        band_name = "TDD_"+str(bands[i])+"_"+str(Power_Value)+"_"+str(eAxID)
        band_folder = os.path.join(Base_Folder_Path, band_name)
        if not (os.path.exists(band_folder)):
            os.mkdir(band_folder)
        time.sleep(200)    
        a = input("Please enter once sync done and DL and UL Carrier added successfully")
        MPlnaeConfig = MPlaneConfiguration()
        if MPlnaeConfig.CheckSync():
            Base_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
            Extended_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
            No_Compression_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
            if MPlnaeConfig.ChangeCompression(9) != True:
                print('Compression format not changed!!')
                return False
            Compression_Static_9bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
            if MPlnaeConfig.ChangeCompression(12) != True:
                print('Compression format not changed!!')
                return False
            Compression_Static_12bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq,Power_Value, VXT_Add, Ext_Gain)
            if MPlnaeConfig.ChangeCompression(14) != True:
                print('Compression format not changed!!')
                return False
            Compression_Static_14bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq,Power_Value, VXT_Add, Ext_Gain)
            # Base_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
            # No_Compression_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
            # a = input("Please enter once UL Carrier bitwidth changed to 9 bit successfully")
            # Compression_Static_9bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
            # a = input("Please enter once UL Carrier bitwidth changed to 12 bit successfully")
            # Compression_Static_12bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
            # a = input("Please enter once UL Carrier bitwidth changed to 14 bit successfully")
            # Compression_Static_14bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
            # VXT_Script.RF_OFF()
            # ST3_NR_PRACH(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add)
        else:
            pass
