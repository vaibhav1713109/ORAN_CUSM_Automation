import sys
import os
import time, shutil
from configparser import ConfigParser
import subprocess, shutil
import csv

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(root_dir)
configur = ConfigParser()
configur.read('{}/RCT/Requirement/inputs.ini'.format(root_dir))
# sys.exit(100)
sys.path.append(root_dir)
from Scripts.scp_gen import *
from Scripts.pcap_gen import *
from Scripts.pcap_load_play_recorde import *
from Scripts.Instrument_config import *
from Scripts.initialisation import *
from Scripts.notification import *

def scp_pcap_play_data(test_case_name:str,eaxid,amplitude:str):
    try:
        if 'PRACH' not in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'scp_gen.py'.center(98)))
            scp_gen_status = scp_genration(test_case_name=test_case_name,eaxcid=eaxid,amplitude=amplitude)
            if scp_gen_status != True:
                return scp_gen_status
        else:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'scp_gen_prach.py'.center(98)))
            scp_gen_status = scp_genration_prach(test_case_name=test_case_name, eaxcid = eaxid)
            if scp_gen_status != True:
                return scp_gen_status


        time.sleep(3)
        if 'PRACH' not in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_gen.py'.center(98)))
            pcap_gen_status = ors_pcap_genration(test_case_name=test_case_name, eAxID = eaxid)
            if pcap_gen_status != True:
                return pcap_gen_status
        else:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_gen_prach.py'.center(98)))
            pcap_gen_status = ors_pcap_genration_prach(test_case_name=test_case_name,eAxID = eaxid)
            if pcap_gen_status != True:
                return pcap_gen_status


        # time.sleep(3)
        # print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_load_play_recorde.py'.center(98)))
        # pcap_load_and_Play_gen_status = Pcap_Load_and_Data_play_record_(test_case_name=test_case_name,eAxID = eaxid)
        # if pcap_load_and_Play_gen_status != True:
        #     return pcap_load_and_Play_gen_status

        return True
    except Exception as e:
        print(f'scp_pcap_play_data Error : {e}')
        return f'scp_pcap_play_data Error : {e}'



def check_crc_pass(crc_data):
    crc_pass = crc_fail = 0
    for data in crc_data:
        if 'True' in data or 'Pass' in crc_data:
            crc_pass+=1
        elif 'False' in data or 'Fail' in crc_data:
            crc_fail+=1
    if crc_fail > 0:
        return 'Fail'
    else:
        return 'Pass'


if __name__ == "__main__":
    pass