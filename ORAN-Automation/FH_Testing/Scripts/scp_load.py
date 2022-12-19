import sys, re
import os
import time,shutil
from configparser import ConfigParser
import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)

#import pythonnet
import clr
clr.AddReference(f"{root_dir}/Dependencies/Keysight.SignalStudio.N7631.dll")
from Keysight.SignalStudio.N7631 import *
from Keysight.SignalStudio import *

sys.path.append(root_dir)
from Scripts.scp_gen import *



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
        return True
    else:
        print('Trigger was not successfull..')
        return False

def load_scp(test_case_name,test_case_id,eaxcid,amplitude,config_file):
    try:
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        duplex_type = config_file['duplex_type']
        bandwidth = config_file['bandwidth']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"
        if 'TDD' in duplex_type:
            center_frequency = config_file['tx_center_frequency']
        else:
            if 'DL' in test_case_name:
                center_frequency = config_file['tx_center_frequency']
            else:
                center_frequency = config_file['rx_center_frequency']
        print(center_frequency)
        scp_file_name = f"{root_dir}/Scpfiles/{test_case_id}.scp"
        print(scp_file_name)
        api = Api()
        # print(dir(api))
        print(f"\n- Recalling the scp file {test_case_id}.scp")
        api.OpenSetupFile(scp_file_name)
        # Saving the scp file
        print("\n- Scp file recall successfull.")
        print(f"\n- Saving the scp file {report_path}\\{test_case_name}.scp")
        if not os.path.exists(f"{report_path}"):
            os.makedirs(f"{report_path}",f"{report_path}\\{test_case_name}.scp")
        shutil.copyfile(scp_file_name,)
        # api.SaveSettingsFile(f"{report_path}\\{test_case_name}.scp")


        print(f"\nGenerating the scp file {report_path}\\{test_case_name}.scp")
        nr_carrier_count = api.NR5GWaveformSettings.GetNRCarriersCount()
        if nr_carrier_count > 1:
            api.NR5GWaveformSettings.RemoveNRCarrier(0)
            print(f'Executing API: api.NR5GWaveformSettings.RemoveNRCarrier(0)')

        file_exists = os.path.exists(f"{report_path}\\{test_case_name}.scp")

        # time.sleep(5)
        if file_exists:
            print("- The scp file exist")
        else:
            Error = "- Scp_genration Error : The scp file not exists"  
            print(Error)
            return Error
        print('- The scp file is successfully generated')
        if 'UL' in test_case_name or 'PRACH' in test_case_name:
            api.SaveSettingsFile(f"{report_path}\\CTC_5GNR_UL.scp")
            # vxt_connection_status = vxt_instrument_connection(VXT_Add=vxt_add,api=api)
            # return Generate_Download(vxt_connection_status,vxt_add,api)
            # return give_trigger(config_file,report_path,center_frequency,amplitude)
        return True
    except Exception as e:
        print(f'Scp_genration Error : {e}')
        return f'Scp_genration Error : {e}'

    finally:
        print('- Api connection closed')
        api.Close()

if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    # print(sys.argv)
    if len(sys.argv)>=2:
        test_case_name,test_case_id, eaxcid, amplitude = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
        print(load_scp(test_case_name,test_case_id, eaxcid, amplitude,information))
        # print(ORS_instrument_Configuration())
        # input('Enter once sync')
    else:
        print('Please run with below format\npython scp_gen.py {test_case_name} {test_case_id} {eaxcid} {amplitude}')