#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#################################################################################################


import re
import os, sys
from configparser import ConfigParser
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
from Script import FDD_Config
from Script import TDD_Config


########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/Requirement/requirement.txt'.format(parent))

dup_type = configur.get('DEFAULT', 'Duplex Type')
band_count = configur.getint('DEFAULT', 'Number of Layers')
bands = list(configur.get('DEFAULT', "Band Widths").split(","))
phase_comp = configur.get('DEFAULT', 'Phase Compensation')
eAxID = configur.get('DEFAULT', 'eAxCid')
Base_Folder_Path = configur.get('DEFAULT', 'Result\'s Path')
DL_Center_Freq = configur.get('DEFAULT', 'DL Center Freq')
UL_Center_Freq = configur.get('DEFAULT', 'UL Center Freq')
Power_Value = (configur.getint('DEFAULT', 'Power in dBm'))*(-1)
VXT_Add = configur.get('DEFAULT', 'VXT Address')
Ext_Gain = (configur.getint('DEFAULT', 'External Gain in dBm'))*(-1)
scs_val = configur.get('DEFAULT', 'Sub Carrier Spacing')
delay_param = list(configur.get('DEFAULT', 'Delay Timing Params').split(","))
Frequency_Band = configur.get('DEFAULT', 'Frequency Band')



# print(dup_type,band_count,bands,phase_comp,eAxID,Base_Folder_Path,DL_Center_Freq,UL_Center_Freq,Power_Value,VXT_Add)

#Check for the Duplex type. If matches the requirement, then calls corresponding functions else shows the error
if (dup_type == 'FDD'):
    FDD_Config.FDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain, scs_val)
elif (dup_type == 'TDD'):
    TDD_Config.TDD(band_count, bands, eAxID, phase_comp, Base_Folder_Path, DL_Center_Freq, UL_Center_Freq, Power_Value, VXT_Add, Ext_Gain, scs_val)
else:
    print("Please check the Duplex Type given in the requirement")
