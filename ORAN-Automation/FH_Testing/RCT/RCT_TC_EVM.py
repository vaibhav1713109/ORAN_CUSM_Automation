import sys
import os
import time, shutil
from configparser import ConfigParser
import shutil
import csv

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(root_dir)
configur = ConfigParser()
configur.read('{}/RCT/Requirement/inputs.ini'.format(root_dir))
# sys.exit(100)
sys.path.append(root_dir)
from RCT.Main import *
from Scripts.stop_player import *
from RCT.vxt_control import *
from Scripts.generate_report import *

def Rct_TC_evm(test_case_name,eaxid,amplitude,ext_gain):
    DL_data = {}
    try:
        all_status = scp_pcap_play_data(test_case_name,eaxid,amplitude)
        if all_status != True:
            return all_status
        
        # time.sleep(3)
        # if 'PRACH' not in test_case_name and 'DL' in test_case_name:
        #     print('{0}\n#{1}#\n{0}'.format('*'*100,'VXT_configuration_result_capture.py'.center(98)))
        #     vxt_configuration_status = VXT_control(test_case_name,ext_gain,eaxid)
        #     DL_data[eaxid] = vxt_configuration_status[:-1]
        #     if type(vxt_configuration_status[-1]) == list:
        #         DL_data[eaxid].append(vxt_configuration_status[-1])
    
    except Exception as e:
        print(f'Rct_TC_evm Error : {e}')
        return f'Rct_TC_evm Error : {e}'
    
    finally:
        print('{0}\n#{1}#\n{0}'.format('*'*100,'stop_player.py'.center(98)))
        stop_payer_status = Stop_Player()
        print(stop_payer_status)
    
    return DL_data

if __name__ == "__main__":
    try:
        start_time = time.time()
        duplex_type = configur.get('INFO','duplex_type')
        RU_Name = configur.get('INFO','ru_name')
        img_version = configur.get('INFO','img_version')
        ru_serial_no = configur.get('INFO','ru_serial_no')
        test_case_name = sys.argv[1]
        eaxid = sys.argv[2]
        amplitude = sys.argv[3]
        external_gain = sys.argv[4]
        Result = Rct_TC_evm(test_case_name,eaxid,amplitude,external_gain)
        print(Result)
    except Exception as e:
        print("RCT_TC_EVM Error : {e}")
        print("Please run by below command :/npython RCT_TC_EVM.py {test_case_name} {eaxcid} {amplitude} {external_gain}")