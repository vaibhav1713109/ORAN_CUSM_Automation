import sys, re, psutil
import os
import time
from configparser import ConfigParser
import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)
sys.path.append(root_dir)
from Requirement.TestCases import *


def make_directories(eaxcids,info):
    RU_Name = info['ru_name']
    img_vesrion = info['img_version']
    ru_serial_no = info['ru_serial_no']
    testing_type = info['testing_type']
    bandwidth = info['bandwidth']
    try:
        for eaxcid in eaxcids:
            for test_case in test_cases:
                if not os.path.exists(f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case}"):
                    os.makedirs(f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case}")
                    print(f"\nMake Dir for {root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case}")
        Result_dir = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}"
        if os.path.exists(Result_dir):
            print(f"make_directories status : {Result_dir} made.")
            return True
        else:
            return f'make_directories Error : {Result_dir} not exist.'
 
    except Exception as e:
        print(f'make_directories Error : {e}')
        return f'make_directories Error : {e}'

def make_directories_single_case(test_case_name, eaxcid,info):
    RU_Name = info['ru_name']
    img_vesrion = info['img_version']
    ru_serial_no = info['ru_serial_no']
    testing_type = info['testing_type']
    bandwidth = info['bandwidth']
    try:
        if not os.path.exists(f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"):
            os.makedirs(f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}")
        Result_dir = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_vesrion}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"
        if os.path.exists(Result_dir):
            print(f"make_directories status : {Result_dir} made.")
            return True
        else:
            return f'make_directories Error : {Result_dir} not exist.'
 
    except Exception as e:
        print(f'make_directories_single_case Error : {e}')
        return f'make_directories_single_case Error : {e}'


def start_vsa_application():
    print("============================================================================================")
    print("=========================== 89600 VSA CONFIGURATION ========================================")
    print("============================================================================================")


    if ("Agilent.SA.Vsa.Vector-x64.exe" in (p.name() for p in psutil.process_iter())):
        print("89600 VSA Application is already running.")
    elif os.path.exists(r"C:\Program Files\Keysight\89600 Software 2023_U1\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe"):
        print("Starting 89600 VSA Application...")
        # os.startfile("C:\Program Files\Keysight\89600 Software 2023\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        os.startfile(r"C:\Program Files\Keysight\89600 Software 2023_U1\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        time.sleep(30)
    else:
        print("Starting 89600 VSA Application...")
        # os.startfile("C:\Program Files\Keysight\89600 Software 2023\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        os.startfile(r"C:\Program Files\Keysight\89600 Software 2023_U2\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        time.sleep(30)
    pass

def check_visa_connection_of_vxt():
    pass

def ru_status():
    pass

if __name__ == "__main__":
    config_file = ConfigParser()
    config_file.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = config_file['INFO']
    print(sys.argv)
    if len(sys.argv)>2:
        start_vsa_application()
        status = make_directories_single_case(sys.argv[1],sys.argv[2],information)
        if status != True:
            print(status)
            sys.exit(1000)
        # print(ORS_instrument_configeration())
        # input('Enter once sync')
    elif len(sys.argv) == 1:
        make_directories(sys.argv[2],information)
    else:
        print('Please run with below format for all cases which are present in {} ...\npython initialisation.py'.format(f'{root_dir}/Requirement/TestCases.txt'))
        print('Please run with below format for single test case...\npython initialisation.py {test_case_name} EAXCID{eaxcid}')