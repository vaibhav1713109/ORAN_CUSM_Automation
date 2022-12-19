#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : TDD_Config.py                                                                       #
# @brief  : This Script will call corresponding functions and Operation related to TDD Conformance Test Cases.#
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @author : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)                   #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################



import re
import sys
import clr
import os.path
import Rest_API_Script
from Rest_API_Script import *

import Generate_SCP
from Generate_SCP import*

import Generate_PCAP_ORB
from Generate_PCAP_ORB import*

import VSA_Constellation
from VSA_Constellation import VSA_Function

import VXT_Script
from VXT_Script import*

import BLER_Automation
from BLER_Automation import*

import PN_Sequence
from PN_Sequence import*



def Base_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = "\Base_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Base_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    VXT_Script.Constellation_check_DL_TDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    # input('Check VXT configuration...')
    Rest_API_Script.Stop_Player()
    
    
def Extended_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = "\Extended_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Extended_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    # VXT_Script.Constellation_check_DL_TDD_repeat(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    VXT_Script.Constellation_check_DL_TDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()


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
    
def No_Compression_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = r"\No_Compression_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 16
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    
    
def Compression_Static_9bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = "\Compression_Static_9bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 9
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    
def Compression_Static_12bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = "\Compression_Static_12bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 12
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    
def Compression_Static_14bit_DL(bands, eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val):
    folder_name = "\Compression_Static_14bit_DL"
    sub_folder = band_folder+folder_name
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    bit_width = 14
    Generate_SCP.Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val)
    Generate_PCAP_ORB.DL(bands, eAxID, sub_folder, bit_width)
    Rest_API_Script.load_play_record_pcap(sub_folder)
    VXT_Script.Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain)
    Rest_API_Script.Stop_Player()
    
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

    



def TDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain, scs_val):
    
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
        Base_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val)
        Extended_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val)
        No_Compression_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val)
        a = input("Please enter once DL Carrier bitwidth changed to 9 bit successfully")
        Compression_Static_9bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain,scs_val)
        a = input("Please enter once DL Carrier bitwidth changed to 12 bit successfully")
        Compression_Static_12bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq,Power_Value, VXT_Add, Ext_Gain,scs_val)
        a = input("Please enter once DL Carrier bitwidth changed to 14 bit successfully")
        Compression_Static_14bit_DL(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq,Power_Value, VXT_Add, Ext_Gain,scs_val)
        Base_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
        No_Compression_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
        a = input("Please enter once UL Carrier bitwidth changed to 9 bit successfully")
        Compression_Static_9bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
        a = input("Please enter once UL Carrier bitwidth changed to 12 bit successfully")
        Compression_Static_12bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
        a = input("Please enter once UL Carrier bitwidth changed to 14 bit successfully")
        Compression_Static_14bit_UL(bands[i], eAxID, phase_comp, band_folder, UL_Center_Freq, Power_Value, VXT_Add)
        VXT_Script.RF_OFF()
        # ST3_NR_PRACH(bands[i], eAxID, phase_comp, band_folder, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add)