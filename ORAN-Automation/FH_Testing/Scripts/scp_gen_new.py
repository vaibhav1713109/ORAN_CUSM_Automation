import sys, re
import os
import time
from configparser import ConfigParser
import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)
import clr
clr.AddReference(f"{root_dir}/Dependencies/Keysight.SignalStudio.N7631.dll")
from Keysight.SignalStudio.N7631 import *
from Keysight.SignalStudio import *
from generate_and_download import *


def give_trigger(config_file,report_path,frequency,amplitude):
    vxt_add = config_file['vxt_address']
    ExternalDelayTime = config_file['externaldelaytime']
    pathwave_address = config_file['pathwave_address']
    pathwave_obj = vxt_connection(visa_address=pathwave_address)
    status = pathwave_obj.visa_connection()
    FilePath = f"{report_path}/CTC_5GNR_UL.scp"
    if status != False:
        pathwave_obj.import_scp_file(FilePath=FilePath)
        pathwave_obj.basic_conf(freq=frequency,amplitude=amplitude,vxt_add=vxt_add)
        pathwave_obj.trigger_conf(ext_delay=ExternalDelayTime)
        pathwave_obj.genrate_download()
        pathwave_obj.device.close()
        return True
    else:
        print('Trigger was not successfull..')
        return False

def scp_genration_prach(test_case_name,eaxcid,amplitude,config_file):
    try:
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        vxt_add = config_file['vxt_address']
        duplex_type = config_file['duplex_type']
        scs_value = config_file['scs_value'][2:-3]
        ExternalDelayTime = config_file['externaldelaytime']
        bandwidth = config_file['bandwidth']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"
        text_file_name = f"{root_dir}/{testing_type}/{duplex_type}/Conformance/{test_case_name}.txt"
        if 'TDD' in duplex_type:
            frequency = config_file['tx_center_frequency']
        else:
            frequency = config_file['rx_center_frequency']
        ExternalDelayTime = config_file['externaldelaytime']
        # Read the APIs from ORS_APIs.txt file
        with open(text_file_name, 'r') as file:
            lines = file.readlines()
        api = Api()
        api.New()
        ########################################################################
        ## Modify the parameters in text file
        ########################################################################
        lines = "".join(lines)
        new_lines = lines.format(frequency=frequency,amplitude=amplitude,ExternalDelayTime=ExternalDelayTime,
             bandwidth = bandwidth,duplex_type=duplex_type,scs_val=scs_value)

        new_lines = new_lines.split('\n')
        for line in new_lines:
            print(f'Executing API: {line}')
            exec(f'{line}')

        if 'A3' in test_case_name:
            brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
            for i in range(10,brust_count):
                a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))
                print(f'Executing API: api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))')

            brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
            for i in range(brust_count):
                api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(i).SlotIndex = i

        if 'B4' in test_case_name:
            brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
            for i in range(1,brust_count):
                a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))
                print(f'Executing API: api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))')

            api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(0).SlotIndex = 9

        if 'C2' in test_case_name:
            brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
            for i in range(10,brust_count):
                a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))
                print(f'Executing API: api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))')

            brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
            for i in range(brust_count):
                api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(i).SlotIndex = i
        brust_count = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()
        print('Executing API: api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsCount()')
        print(f'Total Brust Count : {brust_count}')

        print(f"\nGenerating the scp file {report_path}/{test_case_name}.scp")
        print("\nSaving the scp file")
        if not os.path.exists(f"{report_path}"):
            os.makedirs(f"{report_path}")
        api.SaveSettingsFile(f"{report_path}/{test_case_name}.scp")


        file_exists = os.path.exists(f"{report_path}/{test_case_name}.scp")

        # time.sleep(5)
        if file_exists:
            print("The scp file exist")
        else:
            Error = "Scp_genration Error : The scp file not exists"  
            print(Error)
            return Error
        print('The scp file is successfully generated')
        vxt_connection_status = vxt_instrument_connection(VXT_Add=vxt_add,api=api)
        return Generate_Download(vxt_connection_status,vxt_add,api)
        # return True
 
    except Exception as e:
        print(f'Scp_genration Error : {e}')
        return f'Scp_genration Error : {e}'

    finally:
        print('Api connection closed')
        api.Close()

def scp_genration(test_case_name,eaxcid,amplitude,config_file):
    # try:
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        vxt_add = config_file['vxt_address']
        duplex_type = config_file['duplex_type']
        scs_value = config_file['scs_value'][2:-3]
        ExternalDelayTime = config_file['externaldelaytime']
        bandwidth = config_file['bandwidth']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"
        text_file_name = f"{root_dir}/{testing_type}/{duplex_type}/Conformance/{test_case_name}.txt"
        if 'TDD' in duplex_type:
            frequency = config_file['tx_center_frequency']
        else:
            if 'DL' in test_case_name:
                frequency = config_file['tx_center_frequency']
            else:
                frequency = config_file['rx_center_frequency']
        # Read the APIs from ORS_APIs.txt file
        with open(text_file_name, 'r') as file:
            lines = file.readlines()
        api = Api()
        api.New()
        ########################################################################
        ## Modify the parameters in text file
        ########################################################################
        lines = "".join(lines)
        new_lines = lines.format(frequency=frequency,amplitude=amplitude,ExternalDelayTime=ExternalDelayTime,
             bandwidth = bandwidth,duplex_type=duplex_type,scs_val=scs_value)
        new_lines = new_lines.split('\n')
        # print(new_lines)
        for line in new_lines:
            print(f'Executing API : {line}')
            exec(f'{line}')
        # Saving the scp file
        print("\nSaving the scp file")
        if not os.path.exists(f"{report_path}"):
            os.makedirs(f"{report_path}")
        api.SaveSettingsFile(f"{report_path}/{test_case_name}.scp")

        # Generating the scp file
        print(f"\nGenerating the scp file {report_path}/{test_case_name}.scp")
        nr_carrier_count = api.NR5GWaveformSettings.GetNRCarriersCount()
        if nr_carrier_count > 1:
            api.NR5GWaveformSettings.RemoveNRCarrier(0)
            print(f'Executing API: api.NR5GWaveformSettings.RemoveNRCarrier(0)')

        file_exists = os.path.exists(f"{report_path}/{test_case_name}.scp")
        # time.sleep(5)
        if file_exists:
            print("The scp file exist")
        else:
            Error = "Scp_genration Error : The scp file not exists"  
            print(Error)
            return Error
        print('The scp file is successfully generated')
        if 'UL' in test_case_name:
            api.SaveSettingsFile(f"{report_path}/CTC_5GNR_UL.scp")
            time.sleep(1)
            # vxt_connection_status = vxt_instrument_connection(VXT_Add=vxt_add,api=api)
            # return Generate_Download(vxt_connection_status,vxt_add,api)
            return give_trigger(config_file,report_path,frequency,amplitude)
        return True
 
    # except Exception as e:
    #     print(f'Scp_genration Error : {e}')
    #     return f'Scp_genration Error : {e}'

    # finally:
    #     print('Api connection closed')
    #     api.Close()

if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    if len(sys.argv)>2:
        test_case_name, eaxcid, amplitude = sys.argv[1],sys.argv[2],sys.argv[3]
        if "PRACH" not in sys.argv[1]:
            print(scp_genration(test_case_name, eaxcid, amplitude,information))
        else:
            print(scp_genration_prach(test_case_name, eaxcid, amplitude,information))
    else:
        print('Please run with below format\npython scp_gen.py {test_case_name} {eaxcid} {amplitude}')
