import sys
import os
import time,shutil
from configparser import ConfigParser


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_and_download import *

def give_trigger(pathwave_obj,config_file,FilePath,frequency,amplitude):
    vxt_add = config_file['vxt_address']
    ExternalDelayTime = config_file['externaldelaytime']
    # pathwave_obj.import_scp_file(FilePath=FilePath)
    pathwave_obj.basic_conf(freq=frequency,amplitude=amplitude,vxt_add=vxt_add)
    pathwave_obj.trigger_conf(ext_delay=ExternalDelayTime)
    pathwave_obj.genrate_download()
    return True

def scp_load(test_case_name,test_case_id,eaxcid,amplitude,config_file):
    try:
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        duplex_type = config_file['duplex_type']
        bandwidth = config_file['bandwidth']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        pathwave_address = config_file['pathwave_address']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/{test_case_name}"
        if 'TDD' in duplex_type:
            center_frequency = config_file['tx_center_frequency']
        else:
            if 'DL' in test_case_name:
                center_frequency = config_file['tx_center_frequency']
            else:
                center_frequency = config_file['rx_center_frequency']
        
        scp_file_name = f"{root_dir}/Scpfiles/{test_case_id}.scp"
        
        print("\n- Scp file recall successfull.")
        print(f"\n- Saving the scp file {report_path}\\{test_case_name}.scp")
        if not os.path.exists(f"{report_path}"):
            os.makedirs(f"{report_path}")
        shutil.copyfile(scp_file_name,f'{report_path}\\{test_case_name}.scp')
        if 'UL' in test_case_name:
            pathwave_obj = vxt_connection(visa_address=pathwave_address)
            status = pathwave_obj.visa_connection()
            if status != False:
                pathwave_obj.import_scp_file(FilePath=scp_file_name)
                input('check pathwave')
                carrier_count = pathwave_obj.device.query('RAD:NR5G:WAV:CCAR:COUN?')
                if int(carrier_count) > 1:
                    pathwave_obj.scpi_write('RAD:NR5G:WAV:CCAR:DEL 0')
                    # pathwave_obj.scpi_write(f'RAD:NR5G:WAV:FILE:EXP "{report_path}\\CTC_5GNR_UL.scp"')
                return give_trigger(pathwave_obj,config_file,f"{report_path}\\CTC_5GNR_UL.scp",center_frequency,amplitude)
            else:
                print('Trigger was not successfull..')
                return False
    except Exception as e:
        print(f'Scp_genration Error : {e}')
        return f'Scp_genration Error : {e}'

    finally:
        print('- Visa connection closed')
        pathwave_obj.device.close()


if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    # print(sys.argv)
    if len(sys.argv)>=2:
        test_case_name,test_case_id, eaxcid, amplitude = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
        print(scp_load(test_case_name,test_case_id, eaxcid, amplitude,information))
        # print(ORS_instrument_Configuration())
        # input('Enter once sync')
    else:
        print('Please run with below format\npython scp_gen.py {test_case_name} {test_case_id} {eaxcid} {amplitude}')