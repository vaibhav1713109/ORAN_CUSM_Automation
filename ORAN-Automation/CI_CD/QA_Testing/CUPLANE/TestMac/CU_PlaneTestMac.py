#########################################################################################################
# * ---------------------------------------------------------------------------                         #
# *                              VVDN CONFIDENTIAL                                                      # 
# * ---------------------------------------------------------------------------                         #
# * Copyright (c) 2016 - 2023 VVDN Technologies Pvt Ltd.                                                #
# * All rights reserved                                                                                 #
# *                                                                                                     #
# * NOTICE:                                                                                             #
# *      This software is confidential and proprietary to VVDN Technologies.                            #
# *      No part of this software may be reproduced, stored, transmitted,                               #
# *      disclosed or used in any form or by any means other than as expressly                          #
# *      provided by the written Software License Agreement between                                     #
# *      VVDN Technologies and its license.                                                             #
# *                                                                                                     #
# * PERMISSION:                                                                                         #
# *      Permission is hereby granted to everyone in VVDN Technologies                                  #
# *      to use the software without restriction, including without limitation                          #
# *      the rights to use, copy, modify, merge, with modifications.                                    #
# *                                                                                                     #
# * ---------------------------------------------------------------------------                         # 
# *                                                                                                     #
# * @file     CU_TestMac.py                                                                            #
# * @part_of  CICD CU PLANE                                                                             #
# * @summary                                                                                            #
# * @author   <name>                                                                                    #
# * @Designer Sebu Mathew(sebu.mathew@vvdntech.in)                                                      #
# * @Lead     Manoj T (manoj.t@vvdntech.in)                                                             #
# *                                                                                                     #
#########################################################################################################

import pexpect
import sys,os
import threading
import time
import re
import paramiko
from configparser import ConfigParser
from VXT_control import *
from vxt_recall import *
from genrate_report import *
from fetch_BLER_Percentage import *
from RU_CONTROL.ru_control import *

#########################################################  Get arguments   ######################################################
#if len(sys.argv) < 3:
#    print("Usage: python CU_TestMac.py <tc_name> <dl_BW> <ul_BW> <bit_width> <Tx_layer> <Rx_layer> <Antna_ports>")
#    print("Example = python CU_TestMac.py tdd_qpsk1qpsk1 100 100 16 1 1 1")
#    sys.exit(555)


myarg = sys.argv[1]
print(myarg)
arglist = myarg.split(" ")
executing_tc = arglist[0]
dl_BW = arglist[1]
ul_BW = arglist[2]
ComprBit_width = arglist[3]
Tx_layer = arglist[4]
Rx_layer = arglist[5]
Antna_ports = arglist[6]

########################### identify State/Wfm Files  #################################

def identify_state_file_for_DL(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    state_file = {"dl_qpsk1_100_100_16_1_1_1":"dl_qpsk1_100_100_16_1_1_1.state",
                  "dl_64qam1_100_100_16_1_1_1":"dl_64qam1_100_100_16_1_1_1.state",
                  "dl_256qam1_100_100_16_1_1_1":"dl_256qam1_100_100_16_1_1_1.state"}
                  
    StateFile_Key = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts
    return state_file[StateFile_Key]
    
def identify_wfm_file_for_UL(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    wfm_file = {"ul_qpsk1_100_100_16_1_1_1":"ul_qpsk1_100_100_16_1_1_1.wfm",
                "ul_qpsk2_100_100_16_1_1_1":"ul_qpsk2_100_100_16_1_1_1.wfm",
                "ul_16qam1_100_100_16_1_1_1":"ul_16qam1_100_100_16_1_1_1.wfm",
                "ul_64qam1_100_100_16_1_1_1":"ul_64qam1_100_100_16_1_1_1.wfm"}
    
    WfmFile_Key = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts
    return wfm_file[WfmFile_Key]
    
def identify_state_wfm_file_for_TDD(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    StateWfm_file = {"tdd_qpsk1qpsk1_100_100_16_1_1_1":["dl_qpsk1_100_100_16_1_1_1.state","ul_qpsk1_100_100_16_1_1_1.wfm"],
                     "tdd_64qam164qam1_100_100_16_1_1_1":["dl_64qam1_100_100_16_1_1_1.state","ul_64qam1_100_100_16_1_1_1.wfm"]}
    
    StateWfm_Key = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts
    return StateWfm_file[StateWfm_Key]
    
def identify_ScreenShot_file_for_DL(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    ScrnShot_file = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts+".png"
    return ScrnShot_file

def identify_logfile_for_ch1(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    logfile_Ch1 = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts+"_ch1.txt"
    return logfile_Ch1
    
def identify_logfile_for_ch2(Exectng_Tc,BW_DL,BW_UL,BitWdth,TxLr,RxLr,AntnaPrts):
    logfile_Ch2 = Exectng_Tc+"_"+BW_DL+"_"+BW_UL+"_"+BitWdth+"_"+TxLr+"_"+RxLr+"_"+AntnaPrts+"_ch2.txt"
    return logfile_Ch2

########################### identify State/Wfm Files  #################################

#########################################################  Get arguments   #######################################################

#########################################################  Read ini     ######################################################

## Directory Path
cwd = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)

## For reading data from .ini file
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))
#configur.read('{}/inputs.ini'.format(cwd))
test_mac_ip = configur.get('CUPlane','test_mac_ip')
test_mac_username = configur.get('CUPlane','test_mac_username')
test_mac_password = configur.get('CUPlane','test_mac_password')  

#########################################################  Read ini     ######################################################

      
########################################## Test-mac Configuration codes ############################################################

class TestMac_Cfgns:
    def __init__(self, tc_name, bw_dl, bw_ul, bit_width, layer_tx, layer_rx, antna_ports):
        self.executing_tc = tc_name
        self.dl_BW = bw_dl
        self.ul_BW = bw_ul
        self.ComprBit_width = bit_width
        self.Tx_layer = layer_tx
        self.Rx_layer = layer_rx
        self.Antna_ports = antna_ports
        self.EnCompr = None
        self.ru_name = None
        self.FDD_TDD = None
        self.mu = None
        self.dl_cf = None
        self.ul_cf = None
        self.mac_radio = None
        
    def get_script_path(self):
        script_path = os.path.abspath(__file__)
        directory_name = os.path.dirname(script_path)
        return directory_name
        
    def get_minimum_Radio_info(self, BitWidth):
        try:
            script_path = self.get_script_path()
            script_path = os.path.dirname(os.path.dirname(script_path))
            file_name = f"{script_path}/inputs.ini"
            config = ConfigParser()
            config.read(file_name)
            self.ru_name = config.get('INFO', 'ru_name')
            dl_cf = config.get('INFO', 'tx_center_frequency')
            self.dl_cf = str(float(dl_cf)*1000000)
            ul_cf = config.get('INFO', 'rx_center_frequency')
            self.ul_cf = str(float(ul_cf)*1000000)
            duplex = config.get('INFO', 'duplex_scheme') 
            if 'FDD' in duplex:
                self.FDD_TDD = "0"
            else:
                self.FDD_TDD = "1"
                if self.dl_cf != self.ul_cf:
                    print("DL Center frequency should match with UL Center frequency in case of TDD")
                    return False
            scs = config.get('INFO', 'scs_value')
            if '15' in scs:
                self.mu = "0"
            else:
                self.mu = "1"
            self.mac_radio = config.get('INFO', 'ru_mac')
            if int(BitWidth) < 16:
                self.EnCompr = "1"
            else:
                self.EnCompr = "0"                
            return True
        except Exception as e:
            print(f"An error occurred while reading the ini file configurations: {e}")
            return False

    def read_xml_file(self, filename):
        parent_path = self.get_script_path()
        file_path = os.path.join(parent_path,filename)
        print(file_path)
        with open(file_path, 'r') as file:
            xml_object = file.read()
        return xml_object
        
    def get_config_from_dictionary(self, my_dict, my_key):
        if my_key in my_dict:
            return my_dict[my_key]
        else:
            return None
            
    def get_Slot_mu(self, numerology):
        numSlots = {"0":"10","1":"20"}
        slot = self.get_config_from_dictionary(numSlots,numerology)
        if not slot:
            print("Not able to identify the numSlots for the main cfg")
            return None
        return slot
        
    def get_period_dup(self, Duplex):
        period_duplex = {"0":"1","1":"10"}
        period = self.get_config_from_dictionary(period_duplex,Duplex)
        if not period:
            print("Not able to identify the nTddPeriod for the main cfg")
            return None
        return period
        
    def get_numPRB_mu_bw(self, numerology,bw):
        PRB_map = {"1_100":"273","1_90":"245","1_80":"217","1_70":"189","1_60":"162","1_50":"133","1_40":"106","1_30":"78",
                   "1_20":"51","1_10":"24","0_50":"270","0_40":"216","0_30":"160","0_20":"106","0_15":"79","0_10":"52","0_5":"25"}
        key = numerology+"_"+bw
        numPRB = self.get_config_from_dictionary(PRB_map,key)
        if not numPRB:
            print("Not able to identify the numSlots for the main cfg")
            return None
        return numPRB
        
    def get_cdmgrp_antennaport(self, ports):
        if int(ports) == 1:
            cdmgrp = "1" 
        elif int(ports) > 1:
            cdmgrp = "2"
        else:
            print("invalid Antenna Ports")
            cdmgrp = None
        return cdmgrp
        
    def get_UL_RBSize_mu_bw_modln(self, numerology):
        RB_Size_mu = {"0":"25","1":"51"}
        RB_Size = self.get_config_from_dictionary(RB_Size_mu,numerology)
        if not RB_Size:
            print("Not able to identify the RB_Size for the xran cfg")
            return None
        return RB_Size 
        
    def get_FFT_bw_mu(self, BW, numerology):
        FFT_map = {"100_1":"4096","90_1":"4096","80_1":"4096","70_1":"4096","60_1":"4096","50_1":"2048","40_1":"2048","30_1":"2048",
               "25_1":"1024","20_1":"1024","15_1":"1024","50_0":"4096","40_0":"4096","30_0":"4096","25_0":"2048","20_0":"2048",
               "15_0":"2048","10_0":"1024","5_0":"512"}
        key = BW+"_"+numerology
        FFT = self.get_config_from_dictionary(FFT_map,key)
        if not FFT:
            print("Not able to identify the numSlots for the main cfg")
            return None
        return FFT
        
    def get_frqPtA_CF(self, Fref, numerology, bw):
        GB_15KHz = {"5":0.2425,"10":0.3125,"15":0.3825,"20":0.4525,"25":0.5225,"30":0.5925,"35":0.5725,"40":0.5525,"45":0.7125,"50":0.6925}
        GB_30KHz = {"5":0.505,"10":0.665,"15":0.645,"20":0.805,"25":0.785,"30":0.945,"35":0.925,"40":0.905,"45":0.1065,"50":0.1045,
                    "60":0.825,"70":0.965,"80":0.925,"90":0.885,"100":0.845}
        if numerology == "0":
            GB = GB_15KHz
        else:
            GB = GB_30KHz
        freqPointA = (float(Fref)-(float(bw)/2))+(GB[bw]+0.015)
        return int(freqPointA)
        
    def get_tc_specific_cfg_files(self, executing):
        DL_TM1_1 = ['TM1_1_DL_main.cfg','TM1_1_DL_sub1.cfg','TM1_1_DL_sub2.cfg','TM1_1_DL_sub3.cfg']
        DL_TM3_1 = ['TM3_1_DL_main.cfg','TM3_1_DL_sub1.cfg','TM3_1_DL_sub2.cfg','TM3_1_DL_sub3.cfg']
        DL_TM3_1a = ['TM3_1a_DL_main.cfg','TM3_1a_DL_sub1.cfg','TM3_1a_DL_sub2.cfg','TM3_1a_DL_sub3.cfg']
        UL1_4 = ['4_UL1_main.cfg','4_UL1_sub1.cfg','4_UL1_sub2.cfg','4_UL1_sub3.cfg']
        UL2_4 = ['4_UL2_main.cfg','4_UL2_sub1.cfg','4_UL2_sub2.cfg','4_UL2_sub3.cfg']
        UL_16 = ['16_UL_main.cfg','16_UL_sub1.cfg','16_UL_sub2.cfg','16_UL_sub3.cfg']
        UL_64 = ['64_UL_main.cfg','64_UL_sub1.cfg','64_UL_sub2.cfg','64_UL_sub3.cfg']
        TDD_4_TM1_1 = ['4_TDD_main.cfg','TM1_1_DL_sub1.cfg','TM1_1_DL_sub2.cfg','TM1_1_DL_sub3.cfg',
                       '4_UL1_sub1.cfg','4_UL1_sub2.cfg','4_UL1_sub3.cfg']
        TDD_64_TM3_1 = ['64_TDD_main.cfg','TM3_1_DL_sub1.cfg','TM3_1_DL_sub2.cfg','TM3_1_DL_sub3.cfg',
                        '64_UL_sub1.cfg','64_UL_sub2.cfg','64_UL_sub3.cfg']
        
        test_case = {"dl_qpsk1":DL_TM1_1,"dl_64qam1":DL_TM3_1,"dl_256qam1":DL_TM3_1a,"ul_qpsk1":UL1_4,"ul_qpsk2":UL2_4,
                     "ul_16qam1":UL_16,"ul_64qam1":UL_64,"tdd_qpsk1qpsk1":TDD_4_TM1_1,"tdd_64qam164qam1":TDD_64_TM3_1}
        if executing in test_case:
            return test_case[executing]
        else:
            print("Not able to identify the config_files ... ")
            return None
        
    def read_all_configs(self, configs):
        try:
            parent_path = self.get_script_path()
            cfg_file_path = os.path.join(parent_path, "Test_macs_cfgs")
            obj_config_files = []        
            for config in configs:
                cfg_file = os.path.join(cfg_file_path, config)
                obj_config_files.append(self.read_xml_file(cfg_file))        
            return obj_config_files    
        except Exception as e:
            print(f"An error occurred while reading the configurations: {e}")
            return None

    def get_ru_Specific_configs(self, ru,mac, dl_prb, ul_prb, is_comp, bit_width):  # Dependency = Timing values for other RUs
        ru_specific_dict = {"mac_radio":mac}
        other_ru_params = {"is_comp":is_comp,"bit_width":bit_width,"dl_prb":dl_prb,"ul_prb":ul_prb}
        LPRU_Timing = {"Tadv_cp_dl":"125","T2a_min_cp_dl":"285","T2a_max_cp_dl":"429","T2a_min_cp_ul":"285","T2a_max_cp_ul":"429",
                       "T2a_min_up":"125","T2a_max_up":"375","Ta3_min":"130","Ta3_max":"170","T1a_min_cp_dl":"285","T1a_max_cp_dl":"470",
                       "T1a_min_cp_ul":"285","T1a_max_cp_ul":"429","T1a_min_up":"125","T1a_max_up":"350","Ta4_min":"110","Ta4_max":"180"}
                       
        BND1_Timing = {"Tadv_cp_dl":"125","T2a_min_cp_dl":"250","T2a_max_cp_dl":"481","T2a_min_cp_ul":"125","T2a_max_cp_ul":"356",
                       "T2a_min_up":"128","T2a_max_up":"437","Ta3_min":"144","Ta3_max":"211","T1a_min_cp_dl":"250","T1a_max_cp_dl":"481",
                       "T1a_min_cp_ul":"125","T1a_max_cp_ul":"356","T1a_min_up":"128","T1a_max_up":"437","Ta4_min":"144","Ta4_max":"211"}
                       
        ru_timing = {"LPRUB_4T4R":LPRU_Timing,"LPRUC_4T4R":LPRU_Timing,"LPRUD_4T4R":LPRU_Timing,"BND1_2T2R":BND1_Timing,
                     "BND28_4T4R":BND1_Timing,"VVDN_8T8R":LPRU_Timing}
                     
        timing = self.get_config_from_dictionary(ru_timing,ru)
        if not timing:
            print("Not able to identify the ru_timing configuration for xran.xml")
            return None
        ru_specific_dict.update(timing)
        ru_specific_dict.update(other_ru_params)
        return ru_specific_dict
        
    def format_config_files_dl_or_ul(self, cfg_objs, xran, main_cfg, sub_dl_or_ul):
        formatted_objs = []
        try:
            for cfg_obj in cfg_objs:
                if cfg_obj == cfg_objs[0]:
                    formatted_obj_file = cfg_obj.format(**xran)
                elif cfg_obj == cfg_objs[1]:
                    formatted_obj_file = cfg_obj.format(**main_cfg)
                else:
                    formatted_obj_file = cfg_obj.format(**sub_dl_or_ul)
                formatted_objs.append(formatted_obj_file)
        except Exception as e:
            print(f"An error occurred while formatting the configuration files: {e}")
            return None       
        return formatted_objs
        
    def format_config_files_tdd(self, cfg_objs, xran, main_cfg, sub_dl, sub_ul):
        formatted_objs = []
        try:
            for cfg_obj in cfg_objs:
                if cfg_obj == cfg_objs[0]:
                    formatted_obj_file = cfg_obj.format(**xran)
                elif cfg_obj == cfg_objs[1]:
                    formatted_obj_file = cfg_obj.format(**main_cfg)
                elif cfg_obj in cfg_objs[2:5]:
                    formatted_obj_file = cfg_obj.format(**sub_dl)
                else:
                    formatted_obj_file = cfg_obj.format(**sub_ul)
                formatted_objs.append(formatted_obj_file)
        except Exception as e:
            print(f"An error occurred while formatting the configuration files: {e}")
            return None
        return formatted_objs
        
    def cfg_file_creation_based_on_RU_and_TC(self, ru_name,FDD_TDD,mu,dl_cf,ul_cf,mac_radio,executing_tc,dl_BW,ul_BW,Tx_layer,Rx_layer,Antna_ports,EnCompr,ComprBit_width):
        if dl_BW != ul_BW:
            print("Test-mac currently not supporting different BW for UL and DL")
            return None
        if 'tdd' in executing_tc:
            if not int(FDD_TDD):
                print("The test_case you have opted only for duplex Type = TDD,Aborting")
                return None
        numSlots = self.get_Slot_mu(mu)
        if not numSlots:
            print("Not able to identify NumSlots") 
            return None
        period = self.get_period_dup(FDD_TDD)
        if not period:
            print("Not able to identify tddperiod")
            return None
        numPRB = self.get_numPRB_mu_bw(mu,dl_BW)
        if not numPRB:
            print("Not able to identify PRBNumber") 
            return None
        remaining_prb = str(int(numPRB) - 3)
        cdm_port = self.get_cdmgrp_antennaport(Antna_ports)
        if not cdm_port:
            print("Not able to identify cdmGrp") 
            return None
        oran_RBsize = self.get_UL_RBSize_mu_bw_modln(mu)
        if FDD_TDD:
            ul_BW = dl_BW
            dl_FFT = self.get_FFT_bw_mu(dl_BW,mu)
            ul_FFT = dl_FFT
            dl_frqPtA = self.get_frqPtA_CF(dl_cf,mu,dl_BW)
            ul_frqPtA = dl_frqPtA
        else:
            dl_FFT = self.get_FFT_bw_mu(dl_BW,mu)
            ul_FFT = self.get_FFT_bw_mu(ul_BW,mu)
            dl_frqPtA = self.get_frqPtA_CF(dl_cf,mu,dl_BW)
            ul_frqPtA = self.get_frqPtA_CF(ul_cf,mu,ul_BW)
        if all(variable is None for variable in (dl_BW, ul_BW, dl_FFT, ul_FFT,dl_frqPtA,ul_frqPtA)):
            print("Not able to identify dl_BW/ul_BW/dl_FFT/ul_FFT/dl_frqPtA/ul_frqPtA") 
            return None
        tc_cfgs = self.get_tc_specific_cfg_files(executing_tc)
        if not tc_cfgs:    
            print("Not able to identify cfg_files for the test case")
            return None    
        Config_names = tc_cfgs[1:]
        tc_cfgs.insert(0, 'xrancfg_sub6_automatic.xml')
        obj_configs = self.read_all_configs(tc_cfgs)
        if not obj_configs:    
            print("Not able to read all the files for the test case")
            return None
        
        xran_dict = self.get_ru_Specific_configs(ru_name,mac_radio,numPRB,oran_RBsize,EnCompr,ComprBit_width)
        
        if 'tdd' not in executing_tc:
            main_dict = {"slot":numSlots,"dl_frqPtA":dl_frqPtA,"ul_frqPtA":ul_frqPtA,"dl_BW":dl_BW,"ul_BW":ul_BW,"dl_FFT":dl_FFT,
                         "ul_FFT":ul_FFT,"Tx_Antna_layer":Tx_layer,"Rx_Antna_layer":Rx_layer,"FDD_TDD":FDD_TDD,"numerology":mu,
                         "period":period,"cfg1":Config_names[0],"cfg2":Config_names[1],"cfg3":Config_names[2]}
            if 'dl' in executing_tc:
                sub_dict = {"numPRB":numPRB,"numerology":mu,"Antna_ports":Antna_ports,"remaining_prb":remaining_prb,"cdm_port":cdm_port}
            else:
                sub_dict = {"numPRB":numPRB,"numerology":mu,"Antna_ports":Antna_ports,"oran_RBsize":oran_RBsize,"cdm_port":cdm_port}
            obj_formated_cfgs = self.format_config_files_dl_or_ul(obj_configs,xran_dict,main_dict,sub_dict)
        else:
            main_dict = {"slot":numSlots,"dl_frqPtA":dl_frqPtA,"ul_frqPtA":ul_frqPtA,"dl_BW":dl_BW,"ul_BW":ul_BW,"dl_FFT":dl_FFT,
                         "ul_FFT":ul_FFT,"Tx_Antna_layer":Tx_layer,"Rx_Antna_layer":Rx_layer,"numerology":mu,"dl_cfg1":Config_names[0],
                         "dl_cfg2":Config_names[1],"dl_cfg3":Config_names[2],"ul_cfg1":Config_names[3],"ul_cfg2":Config_names[4],
                         "ul_cfg3":Config_names[5]}
            sub_dl_dict = {"numPRB":numPRB,"numerology":mu,"Antna_ports":Antna_ports,"remaining_prb":remaining_prb,"cdm_port":cdm_port}
            sub_ul_dict = {"numPRB":numPRB,"numerology":mu,"Antna_ports":Antna_ports,"oran_RBsize":oran_RBsize,"cdm_port":cdm_port}
            obj_formated_cfgs = self.format_config_files_tdd(obj_configs,xran_dict,main_dict,sub_dl_dict,sub_ul_dict)
        cfg_files_dict = {k: v for k, v in zip(tc_cfgs, obj_formated_cfgs)}
        return cfg_files_dict

    def remove_files_in_directory(self, directory_path):
        try:
            files = os.listdir(directory_path)
            if not files:
                return True
            else:
                for fle in files:
                    file_path = os.path.join(directory_path, fle)
                    os.remove(file_path)
                return True
        except FileNotFoundError:
            print("The directory cfg_files doesn't exist in Test-mac Server.")
            return False

    def create_cfg_file(self, cfg_file_dict):
        try:
            parent_path = self.get_script_path()
            cfg_file_path = os.path.join(parent_path, "cfg_files")
            os.makedirs(cfg_file_path, exist_ok=True)
            cfg_files_empty = self.remove_files_in_directory(cfg_file_path)
            if not cfg_files_empty:
                return False
            for file_name, content in cfg_file_dict.items():
                with open(os.path.join(cfg_file_path, file_name), 'w') as file1:
                    file1.write(content)
                print(f"File '{file_name}' created successfully.")        
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def write_cfg_files_to_Testmac(self, cfg_files_to_move, tc, numerology):
        try:
            cfg_files = list(cfg_files_to_move.keys())
            xran_path = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1/"
            Additional_path1 = {"0": "mu0_20mhz/", "1": "mu1_100mhz"}
            tc_details = tc.split("_")

            if 'dl' in tc_details[0]:
                base_path = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/tests/nr5g/dl/"
                Additional_path2 = {"qpsk1": "1111", "64qam1": "3100", "256qam1": "3110"}
            elif 'ul' in tc_details[0]:
                base_path = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/tests/nr5g/ul/"
                Additional_path2 = {"qpsk1": "1111", "qpsk2": "4444", "16qam1": "2222", "64qam1": "3333"}
            else:
                base_path = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/tests/nr5g/fd/"
                Additional_path2 = {"qpsk1qpsk1": "1111", "64qam164qam1": "3100"}

            cfg_path = os.path.join(base_path, Additional_path1[numerology], Additional_path2[tc_details[1]])

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(test_mac_ip, username=test_mac_username, password=test_mac_password)
            for cfg_file in cfg_files:
                content = cfg_files_to_move[cfg_file]
                if cfg_file == cfg_files[0]:
                    destination = os.path.join(xran_path, cfg_file)
                else:
                    destination = os.path.join(cfg_path, cfg_file)
                command = f"sudo tee {destination} << EOF\n{content}\nEOF"
                stdin, stdout, stderr = ssh_client.exec_command(command)
                error = stderr.read().decode().strip()
                if error:
                    print(f'movement of file = {cfg_file} to the test-mac failed')
                    print(f"Error occurred: {error}")
                    return False
            return True
        except Exception as e:
            print(f"Error occurred while writing to the remote machine: {e}")
            return False
        finally:
            ssh_client.close()

    def main(self):
        is_obtained = self.get_minimum_Radio_info(self.ComprBit_width)
        if not is_obtained:
            print("not able to fetch minimum informations")
            return False
        ru_name = self.ru_name
        FDD_TDD = self.FDD_TDD
        mu = self.mu
        dl_cf = self.dl_cf
        ul_cf = self.ul_cf
        mac_radio = self.mac_radio
        executing_tc = self.executing_tc
        dl_BW = self.dl_BW
        ul_BW = self.ul_BW
        Tx_layer = self.Tx_layer
        Rx_layer = self.Rx_layer
        Antna_ports = self.Antna_ports
        EnCompr = self.EnCompr
        ComprBit_width = self.ComprBit_width        
        print(ru_name,FDD_TDD,mu,dl_cf,ul_cf,mac_radio)
        print(executing_tc,dl_BW,ul_BW,Tx_layer,Rx_layer,Antna_ports,EnCompr,ComprBit_width)
        
        cfg_files_to_create = self.cfg_file_creation_based_on_RU_and_TC(ru_name,FDD_TDD,mu,dl_cf,ul_cf,mac_radio,executing_tc,dl_BW,ul_BW,Tx_layer,Rx_layer,Antna_ports,EnCompr,ComprBit_width)
        if not cfg_files_to_create:
            print("Not able to obtain the cfg file objects after format")
            return False
        is_created = self.create_cfg_file(cfg_files_to_create)
        if not is_created:
            print("cfg files not created ... Aborting")
            return False
        is_moved = self.write_cfg_files_to_Testmac(cfg_files_to_create,executing_tc,mu)
        return True

########################################## Test-mac Configuration codes ############################################################


########################################## Test-mac Execution Commands ############################################################
class CU_planeError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

def is_ptp_sh_running():
    ps_output = os.popen("ps aux | grep '/home/vvdn/ptp.sh' | grep -v grep").read()
    if 'ptp.sh' in ps_output:
        return True
    return False

def open_terminal_ssh(test_mac_ip,test_mac_username,test_mac_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(test_mac_ip, username=test_mac_username, password=test_mac_password)
        chan = ssh.invoke_shell()
        return chan,ssh
    except Exception as e:
        print(f"Failed to Open ssh channel: {e}")
        return None

def close_terminal_ssh(channel,connection):
    channel.close()
    connection.close()

def send_and_recieve(channel, command, wait_string=None, timeout=None):
    try:
        if timeout or wait_string:
            if send_to_testmac(channel, command) != 0:
                return 5
            status = receive_until(channel,command, wait_string, timeout)
            print("status",status)
        else:
            print("Neither Check_string nor Timeout is Provided")    
            return 10

        return status
    except Exception as e:
        print(f"Failed to Open ssh channel: {e}")
        return None

def send_to_testmac(channel, command):
    try:
        channel.send(command + "\n")
        start_time = time.monotonic()
        while True:
            if time.monotonic() - start_time >= 0.1:
                break
            time.sleep(0.01) 
        return 0
    except paramiko.SSHException as e:
        print(f"Error sending command: {e}")
        return 5


def receive_until(channel,command, wait_string=None, timeout=None):
    try:
        start_time = time.monotonic() 
        while True:
            if (time.monotonic() - channel.recv_ready()):
                    output = channel.recv(1024).decode("utf-8")
                    print(output)
                    if wait_string in output:
                        print(wait_string)
                        return 0
                    else:
                        if time.monotonic() - start_time < timeout:
                            continue
            else:
                print(f"\nCommand '{command}' timed out after {timeout} seconds\n")
                return 1
    except Exception as e:
        print(f"Failed to Open ssh channel: {e}")
        return None
            
def receive_ptp_log(channel,timeout=None):
    offset_values = []
    start_time = time.monotonic()
    while True:
        # print("tello")
        if (time.monotonic() - start_time) < timeout:
            if channel.recv_ready():
                output = channel.recv(1024).decode("utf-8")
                # print(output)
                offset_values.append(output.strip())
         
                continue
            #     offset_values.append(output.strip())
            # return offset_values
        elif (time.monotonic() - start_time) < timeout + 7:        
            for _ in range(5):
                if channel.recv_ready():
                    output = channel.recv(1024).decode("utf-8")
                    print(output)
                    offset_values.append(output.strip())
            return offset_values
        else:            
            return None


def commands_to_T3_ptp_sh(t3):
    try:
        m1 = "/home/vvdn#"
        print(15*"*"+"  Entering to super-user Terminal3  "+ 15*"*")
        status = send_and_recieve(t3, 'sudo su', m1, 3)
        print(status)
        print(15*"*"+"  Terminal 3  "+ 15*"*")
        if status:
            print("login to Super-usr not suceeded with Terminal3")
            return False
        print(15*"*"+"  Running ptp.sh for sync  "+ 15*"*")
        send_to_testmac(t3,'/home/vvdn/ptp.sh')
        print("wait for Test_mac Sync --> May be 60 seconds")
        offset_values = receive_ptp_log(t3,60)
        if not offset_values:
            print("ptp log not obtained")
            return False
        print("ptp log obtained")
        offset_values = []
        for _ in range(5):
            response = t3.recv(1024).decode('utf-8').strip()
            print(response)
            if "phc2sys" in response:
                parts = response.split()
                if "offset" not in parts:
                    continue 
                offset_index = parts.index("offset")
                offset_value = int(parts[offset_index + 1])
                offset_values.append(offset_value)
        print("Delay offsets = ",offset_values)
        if len(offset_values) < 2:
            print("Delay values not obtained")
            return False
        return all(abs(offset) < 100 for offset in offset_values)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'Error Line Number:{exc_tb.tb_lineno}',e)
    
def Terminate_ptp_script_Terminal(channel,connctn):
    kill_command = "pkill -f ptp.sh"
    send_to_testmac(channel,kill_command)
    time.sleep(3)
    close_terminal_ssh(channel,connctn)
    return True

def check_ptp_script_running(test_mac_ip,test_mac_username,test_mac_password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(test_mac_ip, username=test_mac_username, password=test_mac_password)
        stdin, stdout, stderr = ssh_client.exec_command("ps aux | grep ptp.sh")
        process_list = stdout.read().decode("utf-8")
        if re.search(r'\bptp\.sh\b', process_list):
            print("The ptp.sh script is running. Killing it...")
            ssh_client.exec_command("sudo pkill -f ptp.sh")
            ssh_client.exec_command("sudo pkill -f phc2sys")
            ssh_client.exec_command("sudo pkill -f ptp4l")
            print("The ptp.sh script has been killed.")
        else:
            print("The ptp.sh script is not running.")
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print("SSH connection failed:", str(e))
    finally:
        ssh_client.close()

def commands_to_T1_l1_sh(t1):
    try:
        m1 = "/home/vvdn#"
        m3 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#"
        m5 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1#"
        m6 = "PHY>welcome to application console"

        print(15*"*"+"  Entering to super-user Terminal1  "+ 15*"*")
        status = send_and_recieve(t1, 'sudo su', m1, 3)
        print("status is",status)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("login to Super-usr not suceeded with Terminal1")
            return False
        print(15*"*"+"  Loading Virtual Function Modules  "+ 15*"*")
        status = send_and_recieve(t1, '/home/vvdn/vf.sh', m1, 5)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("loading of Virtual Function is not suceeded with Terminal1")
            return False
        print(15*"*"+"  Changing Directory to FlexRan package  "+ 15*"*")
        status = send_and_recieve(t1, 'cd /home/vvdn/Source/FlexRAN_v22.07_release_pacakge', m3, 2)
        print(status)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("Directory change is not suceeded with Terminal1")
            return False
        print(15*"*"+"  Setting Environment variables for Terminal1  "+ 15*"*")
        status = send_and_recieve(t1, 'source set_env_var.sh -d', m3, 7)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("Setting Environment variables is not suceeded with Terminal1")
            return False
        print(15*"*"+"  Changing Directory to --> l1  "+ 15*"*")
        status = send_and_recieve(t1, 'cd bin/nr5g/gnb/l1/', m5, 2)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("Directory change to l1 is not suceeded with Terminal1")
            return False
        print(15*"*"+"  Executing l1.sh in Terminal 1  "+ 15*"*")
        status = send_and_recieve(t1, './l1.sh -xran', m6, 60)
        print("status of l1 ",status)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("Execution of l1.sh is not suceeded with Terminal1")
            return False
        print(15*"*"+"  Reaching to PHY> Console in Terminal 1  "+ 15*"*")
        status = send_and_recieve(t1, '\n', 'PHY>', 3)
        print(15*"*"+"  Terminal 1  "+ 15*"*")
        if status:
            print("Reaching to PHY> Console is not suceeded with Terminal1")
            return False
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'Error Line Number:{exc_tb.tb_lineno}',e)

def send_and_receive_command_terminal(terminal, command_to_send, expecting_string, max_timeout_for_the_command):
    try:
        terminal.send(command_to_send)
        index = terminal.expect([pexpect.EOF, pexpect.TIMEOUT, expecting_string], timeout=max_timeout_for_the_command)
        if index == 0:
            return terminal.before.decode(),False  # EOF
        elif index == 1:
            return terminal.before.decode(),False  # Timeout
        elif index == 2:
            return terminal.before.decode(),True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()  
        print(f'Error Line Number:{exc_tb.tb_lineno}',e)

def commands_to_T2_Test_mac_sh(t2):
    try:
        m1 = "/home/vvdn#"
        m3 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#"
        m5 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/testmac#"
        m6 = "TESTMAC>welcome to application console"

        print(15*"*"+"  Entering to super-user Terminal2  "+ 15*"*")
        status = send_and_recieve(t2, 'sudo su', m1, 3)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("login to Super-usr not suceeded with Terminal2")
            return False
        print(15*"*"+"  Changing Directory to FlexRan package  "+ 15*"*")
        status = send_and_recieve(t2, 'cd /home/vvdn/Source/FlexRAN_v22.07_release_pacakge', m3, 2)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("Directory change is not suceeded with Terminal2")
            return False
        print(15*"*"+"  Setting Environment variables for Terminal2  "+ 15*"*")
        status = send_and_recieve(t2, 'source set_env_var.sh -d', m3, 7)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("Setting Environment variables is not suceeded with Terminal2")
            return False
        print(15*"*"+"  Changing Directory to --> testmac  "+ 15*"*")
        status = send_and_recieve(t2, 'cd bin/nr5g/gnb/testmac/', m5, 2)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("Directory change to testmac is not suceeded with Terminal2")
            return False
        print(15*"*"+"  Executing l2.sh in Terminal 2  "+ 15*"*")
        status = send_and_recieve(t2, './l2.sh', m6, 60)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("Execution of l2.sh is not suceeded with Terminal2")
            return False
        print(15*"*"+"  Reaching to TESTMAC> Console in Terminal 2  "+ 15*"*")
        status = send_and_recieve(t2, '\n', 'TESTMAC>', 3)
        print(15*"*"+"  Terminal 2  "+ 15*"*")
        if status:
            print("Reaching to TESTMAC> Console is not suceeded with Terminal2")
            return False
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'Error Line Number:{exc_tb.tb_lineno}',e)
    
def terminal1_listener(terminal1,log_name):
    global STOP_FLAG
    log_path = os.path.join(parent_dir,"Results")
    log_file = f"{log_path}/{log_name}"
    print("\n" + 30 * "*" + "Layer_1" + 30 * "*" + "\n")
    with open(log_file, "w") as file1:
        while not STOP_FLAG:
            if terminal1.recv_ready():
                output1 = terminal1.recv(1024).decode("utf-8")
                file1.write(output1)
                # print(output1)
            else:
                time.sleep(0.05)

def terminal2_listener(terminal2,log_name):
    global STOP_FLAG
    log_path = os.path.join(parent_dir,"Results")
    log_file = f"{log_path}/{log_name}"
    print("\n" + 30 * "*" + "Testmac" + 30 * "*" + "\n")
    with open(log_file, "w") as file1:
        while not STOP_FLAG:
            if terminal2.recv_ready():
                output2 = terminal2.recv(1024).decode("utf-8")
                file1.write(output2)
                # print(output2)
            else:
                time.sleep(0.05)
                
def exit_l1_script(t1):
    m1 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1#"    
    print(15*"*"+"  Exiting from l1.sh in Terminal 1  "+ 15*"*")
    status = send_and_recieve(t1, '\n\n', 'PHY>', 3)
    status = send_and_recieve(t1, 'exit', m1, 15)
    print("l1status",status)
    print(15*"*"+"  Terminal 1  "+ 15*"*")
    if status:
        print("Exiting from l1.sh is not suceeded with Terminal1")
        return False
    return True
    
def exit_l2_script(t2):
    # m2 = "/home/mitak/Source_bkp/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/testmac#"
    m2 = "/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/testmac#"
    print(15*"*"+"  Exiting from l2.sh in Terminal 2  "+ 15*"*")
    status = send_and_recieve(t2, '\n\n', 'TESTMAC>', 3)
    status = send_and_recieve(t2, 'exit', m2, 15)
    print(15*"*"+"  Terminal 2  "+ 15*"*")
    if status:
        print("Exiting from l2.sh is not suceeded with Terminal2")
        return False
    return True


def identify_testmac_Path(tc_info,ini_path):
    configur = ConfigParser()
    configur.read('{}/inputs.ini'.format(root_dir))
    #configur.read('{}/inputs.ini'.format(ini_path))
    scs = configur.get('INFO','scs_value')
    mu = {"KHZ_30":"1","KHZ_15":"0"}
    tcDetail = tc_info.split("_")
    dl_ul_tdd = tcDetail[0]
    modlnTyp = tcDetail[1]
    if 'dl' in dl_ul_tdd:
        modln = {"qpsk1": "11111", "64qam1": "13100", "256qam1": "13110"}
        TcTyp = "0"
    elif 'ul' in dl_ul_tdd:
        modln = {"qpsk1": "11111", "qpsk2": "14444", "16qam1": "12222", "64qam1": "13333"}
        TcTyp = "1"
    else:
        modln = {"qpsk1qpsk1": "11111", "64qam164qam1": "13100"}
        TcTyp = "2"
    BW = "100"
    runnr_path = "runnr "+TcTyp+" "+mu[scs]+" "+BW+" "+modln[modlnTyp]
    return runnr_path
    
########################################## Test-mac Execution Commands ############################################################
    
if __name__ == "__main__":
    try:
        STOP_FLAG = False
        Close_FLAG_T1 = False
        Close_FLAG_T2 = False
        Close_FLAG_T3 = False
        Exit_FLAG_L1 = False
        Exit_FLAG_L2 = False
        CU_planeError_FLAG = 0
        ru_obj = ru_control()
        connection = ru_obj.NP_Connection()
        if connection[-1] != True:
            print("Netopeer Connection not Established...")
            sys.exit(1000)
        else:
            conf_status = ru_obj.ru_configuration(connection[0])
            if conf_status != True:
                print(conf_status)
                sys.exit(1000)
        print("Test_mac configuration initialising...")
        obj_tstmac_cfgns = TestMac_Cfgns(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
        is_configured = obj_tstmac_cfgns.main()
        if not is_configured:
            raise CU_planeError("Error TestMac Configuration failed", 444)
        testmac_path = identify_testmac_Path(executing_tc,cwd)
        print("TestMac configuration completed")        

        terminal_object3,connctn3 = open_terminal_ssh(test_mac_ip,test_mac_username,test_mac_password)
        if not terminal_object3:
            raise CU_planeError("Channel for ptp is not able open", 3001)            
        Close_FLAG_T3 = True
        status = commands_to_T3_ptp_sh(terminal_object3)
        print(status)
        # if not status:
        if not status:
            raise CU_planeError("TestMac_Sync not obtained", 1001)
        else:
            print("TestMac sync Completed")
        
        sync_status = ru_obj.ru_sync_and_oper_state(connection[0])
        if sync_status != True:
            print(sync_status)
            sys.exit(10000)
        terminal_object1,connctn1 = open_terminal_ssh(test_mac_ip,test_mac_username,test_mac_password)
        if not terminal_object1:
            raise CU_planeError("Channel for l1.sh is not able open", 3002)
        Close_FLAG_T1 = True
        status = commands_to_T1_l1_sh(terminal_object1)
        if not status:
            raise CU_planeError("Error executing commands for terminal_object1", 101)
        terminal_object2,connctn2 = open_terminal_ssh(test_mac_ip,test_mac_username,test_mac_password)
        if not terminal_object2:
            raise CU_planeError("Channel for l2.sh is not able open", 3003)
        Close_FLAG_T2 = True
        status = commands_to_T2_Test_mac_sh(terminal_object2)
        if not status:
            raise CU_planeError("Error executing commands for terminal_object2", 102)
        status = send_and_recieve(terminal_object2,'phystart 4 0 0', 'TESTMAC>', 10)
        if status:
            raise CU_planeError("Error in executing phystart command in l2.sh", 103)
        log_file1 = identify_logfile_for_ch1(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
        log_file2 = identify_logfile_for_ch2(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
        if "ul" in executing_tc:
            WFMfile = identify_wfm_file_for_UL(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
            print(WFMfile)
            file_recall_status = recall_wfm_file(WFMfile)
            if file_recall_status != True:
                sys.exit(1000)
        elif 'tdd' in executing_tc:
            STATE_WFMfile = identify_state_wfm_file_for_TDD(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
            file_recall_status = recall_wfm_file(STATE_WFMfile[1])
            if file_recall_status != True:
                sys.exit(1000)
        #input("Do the recall statefile or .wfm or both file based on DL or UL or both manually in VXT and the Press Enter")
        time.sleep(10)
        #terminal_object2.send(testmac_path+"\n")
        send_to_testmac(terminal_object2,testmac_path)
        
        Exit_FLAG_L1 = True
        Exit_FLAG_L2 = True
        
        trd1 = threading.Thread(target=terminal1_listener, args=(terminal_object1,log_file1))
        trd2 = threading.Thread(target=terminal2_listener, args=(terminal_object2,log_file2))
        trd1.start()
        trd2.start()

        time.sleep(3)
        print('='*100)
        dl_Result = None
        if 'dl' in executing_tc:
            STATEfile = identify_state_file_for_DL(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
            SCRNSHOTfile = identify_ScreenShot_file_for_DL(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
            print(STATEfile)
            print(SCRNSHOTfile)
            print('='*100)
            print("checking_VXT_for Pass_Or_Fail")
            print('='*100)
            dl_Result = VXT_control(STATEfile,SCRNSHOTfile,dl_BW)
            print(dl_Result)
            print('='*100)
        elif 'tdd' in executing_tc:
            SCRNSHOTfile = identify_ScreenShot_file_for_DL(executing_tc, dl_BW, ul_BW, ComprBit_width, Tx_layer, Rx_layer, Antna_ports)
            print('='*100)
            print("checking_VXT_for Pass_Or_Fail")
            print('='*100)
            dl_Result = VXT_control(STATE_WFMfile[0],SCRNSHOTfile,dl_BW)
            print(dl_Result)
            print('='*100)
        #input("wait for 30 seconds and Press Enter after your validation of result")
        time.sleep(5)
        
        STOP_FLAG = True
        trd1.join()
        trd2.join()
        
        print("execution_completed")
        report_path = f"/comon-space/QA_Testing/CUPLANE/Results/{executing_tc}.pdf"
        if dl_Result != None:
            Result = genrate_report_dl([dl_Result[:-1]],report_path,dl_Result[-1])
            if 'Pass' in dl_Result:
                print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Pass'.center(92)))
                sys.exit(0)
            else:
                if len(dl_Result)>6 and len(dl_Result)<12:
                    print('{}'.format('Fail Reason :  Low Power or Evm'))
                else:
                    print('{}'.format('Fail Reason :  Data from VXT not captured.'))
                print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Fail'.center(92)))
                err_raise_Flag = True
        if 'ul' in executing_tc or 'tdd' in executing_tc:
            UL_log_path = os.path.join(parent_dir,"Results")
            bler_val = fetch_BLER_Percentage_list(f'{UL_log_path}/{log_file1}')
            print(bler_val)
            bler = bler_val[(len(bler_val)//2)+1]
            if int(bler) < 15:
                print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Pass'.center(92)))
                sys.exit(0)
            else:
                print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Fail'.center(92)))
                err_raise_Flag = True
        if err_raise_Flag:
            raise CU_planeError("The outpu evm/power/BLER is not as Expected", 9999)
        print("Completed_Execution")


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'Error Line Number:{exc_tb.tb_lineno}',e)
        CU_planeError_FLAG = 777  
    except CU_planeError as e:
        print(f"Error: {e}")
        CU_planeError_FLAG = e.error_code
        #sys.exit(e.error_code)
    finally:
        is_exited_l2 = False
        is_exited_l1 = False
        is_ptp_closed = False
        if Exit_FLAG_L2:
            is_exited_l2 = exit_l2_script(terminal_object2)
        if Exit_FLAG_L1:
            is_exited_l1 = exit_l1_script(terminal_object1)            
        if Close_FLAG_T3:
            Terminate_ptp_script_Terminal(terminal_object3,connctn3)
            close_terminal_ssh(terminal_object3,connctn3)
            if not check_ptp_script_running(test_mac_ip,test_mac_username,test_mac_password):
                  is_ptp_closed = True
        if Close_FLAG_T2:
            close_terminal_ssh(terminal_object2,connctn2)
        if Close_FLAG_T1:
            close_terminal_ssh(terminal_object1,connctn1)
        if CU_planeError_FLAG:
            sys.exit(CU_planeError_FLAG)
        flag_lists = [is_exited_l2,is_exited_l1,is_ptp_closed]
        if any(not flag for flag in flag_lists):
            print("Not all the Process properly closed in the testmac")
            sys.exit(666)
        print("completed")
        sys.exit(0)
