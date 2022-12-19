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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from vxt_recall import *
# from generate_and_download import *
# # from Oran_GUI_Pyqt5.popup import *
# # from Oran_GUI_Pyqt5.sync_popup import *

# def give_trigger(config_file,report_path,frequency,amplitude):
#     vxt_add = config_file['vxt_address']
#     ExternalDelayTime = config_file['externaldelaytime']
#     pathwave_address = config_file['pathwave_address']
#     pathwave_obj = vxt_connection(visa_address=pathwave_address)
#     status = pathwave_obj.visa_connection()
#     FilePath = f"{report_path}/CTC_5GNR_UL.scp"
#     if status != False:
#         try:
#             pathwave_obj.import_scp_file(FilePath=FilePath)
#             pathwave_obj.basic_conf(freq=frequency,amplitude=amplitude,vxt_add=vxt_add)
#             pathwave_obj.trigger_conf(ext_delay=ExternalDelayTime)
#             pathwave_obj.genrate_download()
#             return True
#         except Exception as e:
#             print(f'give_trigger Error | {type(e).__name__} : {e}')
#         finally:
#             print('Connection Closed...')
#             pathwave_obj.device.close()
#     else:
#         print('Trigger was not successfull..')
#         return False

def vxt_instrument_connection(VXT_Add, api):
    print('Connecting the instrumet')
    inst = VXT_Add
    b = api.ConnectInstrument(inst)
    #b = True
    # print(b)
    # print(type(b))
    return b

def Generate_Download(status, VXT_Add, api,freq,amplitude,delay):    
    if status:
        # print(status, VXT_Add, api,freq,amplitude,delay)
        commands = [f"api.SignalGenerator.Frequency = {(float(freq)*1000000000)}",
        f"api.SignalGenerator.Amplitude = {amplitude}",
        f"api.SignalGenerator.ExternalPolarity = Polarity.Positive",
        f"api.SignalGenerator.Continuous = Continuous.TriggerAndRun",
        f"api.SignalGenerator.SingleTrigger = SingleTrigger.BufferedTrigger",
        f"api.SignalGenerator.SegmentAdvance = SegmentAdvance.Continuous"]
        for cmd in commands:
            print(f'Executing API: {cmd}')
            exec(f'{cmd}')
        print("- Generating the configurations")
        # api.Generate()
        # print("- Connected to the Instrument at " + str(VXT_Add) + ".")
        # api.Download()
        return True
    else:
        Error = " ############ Generate_Download Error : Instrument Connection failed ############"
        return Error

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
        # Execute each API one by one
        for line in lines:
            # Your code to call the API and execute it
            if 'Frequency' in line:
                lineindex_of_freq = lines.index(line)
                lines[lineindex_of_freq] = f"api.SignalGenerator.Frequency = (float({frequency})*1000000000)\n"
            elif 'Amplitude' in line:
                lineindex_of_ext_delay = lines.index(line)
                lines[lineindex_of_ext_delay] = f"api.SignalGenerator.Amplitude = {amplitude}\n"
            elif 'ExternalDelayTime' in line:
                lineindex_of_ext_delay = lines.index(line)
                lines[lineindex_of_ext_delay] = f"api.SignalGenerator.ExternalDelayTime = {ExternalDelayTime}\n"
            elif 'PresetDLTestModel' in line:
                split_line = line.split(',')
                lineindex_of_bandwidth = lines.index(line)
                replace_bandwidth = re.sub('Bandwidth.FR1_.{1,3}M',f'Bandwidth.{bandwidth}', split_line[0])
                replace_scs_val = re.sub('Numerology.SCS.{1,3}k',f'Numerology.SCS{scs_value}k', split_line[1])
                replace_duplex_val = re.sub('DuplexType.TDD',f'DuplexType.{duplex_type}', replace_scs_val)
                split_line[0] = replace_bandwidth
                split_line[1] = replace_duplex_val
                line = ','.join(split_line)
                lines[lineindex_of_bandwidth] = line
            elif 'ULFRCConfig' in line:
                split_line = line.split(',')
                lineindex_of_bandwidth = lines.index(line)
                replaced_line = re.sub('Bandwidth.FR1_.{1,3}M',f'Bandwidth.{bandwidth}', split_line[0])
                split_line[0] = replaced_line
                line = ','.join(split_line)
                lines[lineindex_of_bandwidth] = line
            elif 'PrachTestPreamblesConfig' in line:
                split_line = line.split(',')
                lineindex_of_bandwidth = lines.index(line)
                replaced_line = re.sub('Bandwidth.FR1_.{1,3}M',f'Bandwidth.{bandwidth}', split_line[0])
                split_line[0] = replaced_line
                line = ','.join(split_line)
                lines[lineindex_of_bandwidth] = line

        for line in lines:
            print(f'Executing API: {line}')
            exec(f'{line}')
        with open(text_file_name, 'w+') as file1:
            file1.writelines(lines)

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
        trigger_status = Generate_Download(vxt_connection_status,vxt_add,api,frequency,amplitude,ExternalDelayTime)
        api.Export(f"{report_path}/{test_case_name}.wfm")
        api.SaveSettingsFile(f"{report_path}/{test_case_name}.scp")
        print(f"file {report_path}/{test_case_name}.scp saved successfully.")
        time.sleep(1)
        return recall_wfm_file(f'{test_case_name}.wfm',config_file,amplitude,report_path)
        # return True
 
    except Exception as e:
        print(f'Scp_genration Error : {e}')
        return f'Scp_genration Error : {e}'

    finally:
        print('Api connection closed')
        api.Close()

def scp_genration(test_case_name,eaxcid,amplitude,config_file):
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
        pathwave_address = config_file['pathwave_address']
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
        # Execute each API one by one
        for line in lines:
            # Your code to call the API and execute it
            if 'Frequency' in line:
                lineindex_of_freq = lines.index(line)
                lines[lineindex_of_freq] = f"api.SignalGenerator.Frequency = (float({frequency})*1000000000)\n"
            elif 'Amplitude' in line:
                lineindex_of_ext_delay = lines.index(line)
                lines[lineindex_of_ext_delay] = f"api.SignalGenerator.Amplitude = {amplitude}\n"
            elif 'ExternalDelayTime' in line:
                lineindex_of_ext_delay = lines.index(line)
                lines[lineindex_of_ext_delay] = f"api.SignalGenerator.ExternalDelayTime = {ExternalDelayTime}\n"
            elif 'PresetDLTestModel' in line:
                split_line = line.split(',',1)
                lineindex_of_bandwidth = lines.index(line)
                replace_bandwidth = re.sub('Bandwidth.FR1_.{1,3}M',f'Bandwidth.{bandwidth}', split_line[0])
                replace_scs_val = re.sub('Numerology.SCS.{1,3}k',f'Numerology.SCS{scs_value}k', split_line[1])
                replace_duplex_val = re.sub('DuplexType.TDD',f'DuplexType.{duplex_type}', replace_scs_val)
                split_line[0] = replace_bandwidth
                split_line[1] = replace_duplex_val
                line = ','.join(split_line)
                lines[lineindex_of_bandwidth] = line
            elif 'ULFRCConfig' in line:
                split_line = line.split(',')
                lineindex_of_bandwidth = lines.index(line)
                replaced_line = re.sub('Bandwidth.FR1_.{1,3}M',f'Bandwidth.{bandwidth}', split_line[0])
                split_line[0] = replaced_line
                line = ','.join(split_line)
                lines[lineindex_of_bandwidth] = line
                
        print(f'Executing API: api.SignalGenerator.Frequency = {(float(frequency)*1000000000)}')
        exec(f"api.SignalGenerator.Frequency = {(float(frequency)*1000000000)}")
        for line in lines:
            print(f'Executing API: {line}',end='')
            exec(f'{line}')
        with open(text_file_name, 'w+') as file1:
            file1.writelines(lines)

        # Saving the scp file
        print("\nSaving the scp file")
        if not os.path.exists(f"{report_path}"):
            os.makedirs(f"{report_path}")
        api.SaveSettingsFile(f"{report_path}/{test_case_name}.scp")

        # Generating the scp file
        print(f"\n- Recalling the scp file {report_path}/{test_case_name}.scp")
        api.OpenSetupFile(f"{report_path}/{test_case_name}.scp")
        nr_carrier_count = api.NR5GWaveformSettings.GetNRCarriersCount()
        print(f'- No of carriers : {nr_carrier_count}')
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
            vxt_connection_status = vxt_instrument_connection(VXT_Add=vxt_add,api=api)
            trigger_status = Generate_Download(vxt_connection_status,vxt_add,api,frequency,amplitude,ExternalDelayTime)
            api.Export(f"{report_path}/CTC_5GNR_UL.wfm")
            api.SaveSettingsFile(f"{report_path}/CTC_5GNR_UL.scp")
            print(f"file {report_path}/CTC_5GNR_UL.scp saved successfully.")
            time.sleep(1)
            return recall_wfm_file('CTC_5GNR_UL.wfm',config_file,amplitude,report_path)
        return True
 
    except Exception as e:
        print(f'Scp_genration Error : {e}')
        return f'Scp_genration Error : {e}'

    finally:
        print('Api connection closed')
        api.Close()
    

if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    if len(sys.argv)>2:
        test_case_name, eaxcid, amplitude = sys.argv[1],sys.argv[2],sys.argv[3]
        if "PRACH" not in sys.argv[1]:
            print(scp_genration(test_case_name, eaxcid, amplitude, information))
        else:
            print(scp_genration_prach(test_case_name, eaxcid, amplitude, information))
    else:
        print('Please run with below format\npython scp_gen.py {test_case_name} {eaxcid} {amplitude}')
