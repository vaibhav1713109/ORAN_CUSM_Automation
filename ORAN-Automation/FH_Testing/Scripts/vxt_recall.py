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
# * @file     vxt_recall.py                                                                             #
# * @summary  To recall wfm                                                                             #
# * @author   Vaibhav Dhiman(vaibhav.dhiman@vvdntech.in)                                                #
# * @Lead     Sebu Mathew(sebu.mathew@vvdntech.in)                                                      #
# * @Manager  Manoj T (manoj.t@vvdntech.in)                                                             #
# *                                                                                                     #
#########################################################################################################

import pyvisa
import time,os,sys
from configparser import ConfigParser

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('root_dir',root_dir)
configur = ConfigParser()
configur.read('{}/Requirement/inputs.ini'.format(root_dir))

def make_visa_connection(info_section):
    try:
        rm = pyvisa.ResourceManager()
        visa = info_section['vxt_address']
        print(visa)
        InstrObj = rm.open_resource(visa)
        time.sleep(2)
        print(InstrObj)
        InstrObj.timeout = 10000
        return InstrObj
    except Exception as e:
        error = f"make_visa_connection Error : {e}"
        print(e)
        return e

def clear_status_reg_of_device(InstrObj):
    InstrObj.write('*CLS')                                #Clear Status Register of device
    InstrObj.write('*WAI')                                #Wait till Clear command is complete

    #########################################################################################
    ## Reseting the VXT
    #########################################################################################
def reset_device(InstrObj):
    InstrObj.write('*RST')                                #Reset the device
    InstrObj.write('*WAI')

def scpi_write(InstrObj, cmnd):
   InstrObj.write(cmnd)
   status = InstrObj.query('*OPC?')
   while(1):
        print(f'{cmnd} {status}')
        if int(status) != 1:
            time.sleep(0.001)
            status = InstrObj.query('*OPC?')
        else:
            break
   time.sleep(1)
   return True


def recall_wfm_file(filename,info_section,amplitude,report_path):
    center_frequency = info_section['rx_center_frequency']
    ext_delay = info_section['externaldelaytime']
    InstrObj = make_visa_connection(info_section)
    remote_folder = "C:\\Users\\Administrator\\Documents"
    if InstrObj:
        local_file = os.path.join(f"{report_path}", filename)
        if not os.path.isfile(local_file):
            print(f"File not found: {local_file}")
            return f"File not found: {local_file}"

        with open(local_file, 'rb') as f:
            read_data = f.read()

        #remote_file = os.path.join(remote_path, file_name)
        rem_file = os.path.normpath(remote_folder+'\\'+filename)    
        print(rem_file)        
        reset_device(InstrObj)
        clear_status_reg_of_device(InstrObj)
        print(f'Deleting the file {rem_file}....')
        InstrObj.write(f'MMEM:DEL "{rem_file}"')
        InstrObj.write(f':MMEMory:MDIRectory "{remote_folder}"')
        InstrObj.write_binary_values(f':MMEMory:DATA "{rem_file}",', read_data, datatype='B')
        status_complete = InstrObj.query("*OPC?")
        if int(status_complete) != 1:
            print("not completed",status_complete)
            error = f'send_file_to_VXT Error: Failed to transfer {local_file} to {rem_file}'
            return error
        else:
            print(f'File {local_file} successfully transferred to {rem_file}')
            # wfm_command = [f":SOUR:RAD:ARB:LOAD {filename}",":SOUR:RAD:ARB ON",":SOUR:RAD:ARB:TRIG:TYPE CONT",
            #                 ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG",":SOUR:RAD:ARB:TRIG EXT1", ":SOUR:RAD:ARB:TRIG:SYNC ON",
            #                 ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON",":SOUR:RAD:ARB:TRIG:EXT:DEL 0s",":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS",
            #                 f":SOUR:POW {amplitude} dBm",f":SOUR:FREQ {center_frequency} GHz",":OUTP ON"]
            wfm_command = [f':SOUR:RAD:ARB:LOAD "{rem_file}"',f":SOUR:RAD:ARB:WAV '{rem_file}'",
                            ":SOUR:RAD:ARB ON",":SOUR:RAD:ARB:TRIG:TYPE CONT",
                            ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG",":SOUR:RAD:ARB:TRIG EXT1", ":SOUR:RAD:ARB:TRIG:SYNC ON",
                            ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON",f":SOUR:RAD:ARB:TRIG:EXT:DEL {ext_delay}s",":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS",
                            f":SOUR:POW {amplitude} dBm",f":SOUR:FREQ {center_frequency} GHz",":OUTP ON"]
            for cmd in wfm_command:
                scpi_write(InstrObj,cmd)
            InstrObj.close()
            print("Waveform file recalled successfully")
            return True
    else:
        print('Error while creating visa connection.')
        return 'Error while creating visa connection.'


if __name__  == "__main__":
    info_section = configur['INFO']
    amplitude = "-42"
    report_path = r"C:\Automation\FH_Testing_V1.0.0\Results\CUPLANE\LPRU_v7\2.1.7\2311348700020\FR1_100M\EAXCID0\Extended_DL_UL"
    recall_wfm_file("CTC_5GNR_UL.wfm",info_section,amplitude,report_path)

# rm = pyvisa.ResourceManager()
# visa = 'TCPIP0::172.25.96.182::hislip0::INSTR'
# InstrObj = rm.open_resource(visa)
# time.sleep(2)

# print(InstrObj)
# InstrObj.timeout = 10000
#InstrObj.write(":MMEM:LOAD:STAT 'Extended_DL_UL.state'")

# #Select a waveform segment or sequence to be played by the ARB player. ---> wfm file name
# scpi_write(InstrObj, ":SOUR:RAD:ARB:WAV 'C:\\Users\\Administrator\\Documents\\giri\\ul.wfm'")

# #Toggle the state of the ARB function ---> ON
# scpi_write(InstrObj, ":SOUR:RAD:ARB ON")

# #Setting for trigger type determines the behavior of the waveform when it plays ---> Continuous
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:TYPE CONT")

# #Sets the active trigger type to Continuous. If Continuous is already selected as the active trigger type, 
# #pressing this key allows access to the continuous trigger type setup menu. 
# #In Continuous trigger mode, the waveform repeats continuously ----> Trigger+Run
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG")

# #The trigger source setting determines how the source receives the trigger that starts the waveform playing ---> External1
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG EXT1")

# #Sync to Trigger Source ---> ON
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:SYNC ON")

# #External Trigger Delay ---> ON and Os
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON")
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:EXT:DEL 0s")

# #External Trigger Polarity ---> Positive
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS")

# #RF Power in Amplitude Setup
# scpi_write(InstrObj, ":SOUR:POW -60 dBm")

# #Frequency in the Frequency Setup menu
# scpi_write(InstrObj, ":SOUR:FREQ 3.54234 GHz")

# #Sets the source RF power output state.
# scpi_write(InstrObj, ":OUTP ON")

# print("Waveform file recalled successfully")
