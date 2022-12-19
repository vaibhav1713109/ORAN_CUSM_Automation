import sys
import os
import time, shutil
from configparser import ConfigParser
import subprocess, shutil
import csv

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)
configur = ConfigParser()
configur.read('{}/Requirement/inputs.ini'.format(root_dir))
sys.path.append(root_dir)
from Scripts.scp_gen import *
from Scripts.pcap_gen import *
from Scripts.pcap_load_play_recorde import *
# from Scripts.vxt_control_new import *
from Scripts.vxt_control_without_scp_load import *
from Scripts.orb_gen import *
from Scripts.vsa_constellation_and_result_capture import *
from Scripts.stop_player import *
from Scripts.generate_report import *
from Oran_GUI_Pyqt5.popup import *
from Oran_GUI_Pyqt5.sync_popup import *
from Scripts.M_Plane_Conf import *
from Requirement.TestCases import *
from Scripts.Instrument_config import *
from Scripts.initialisation import *
from Scripts.RunKtmSwitch import *
# from Scripts.compression_change import *
from Scripts.notification import *

def main(test_case_name,eaxid,amplitude,ext_gain,config_file):
    # python_path = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
    python_path = 'python'
    DL_data = {}
    UL_data = {}
    Center_Freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    power_limit = config_file['power_limit'].split(',')
    evm_limit = config_file['evm_limit']
    try:
        if 'PRACH' not in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'scp_gen.py'.center(98)))
            scp_gen_status = scp_genration(test_case_name=test_case_name,eaxcid=eaxid,amplitude=amplitude,config_file=config_file)
            if scp_gen_status != True:
                return scp_gen_status
        else:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'scp_gen_prach.py'.center(98)))
            scp_gen_status = scp_genration_prach(test_case_name=test_case_name, eaxcid = eaxid,config_file=config_file)
            if scp_gen_status != True:
                return scp_gen_status


        time.sleep(3)
        if 'PRACH' not in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_gen.py'.center(98)))
            pcap_gen_status = ors_pcap_genration(test_case_name=test_case_name, eAxID = eaxid,info_section=config_file)
            if pcap_gen_status != True:
                return pcap_gen_status
        else:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_gen_prach.py'.center(98)))
            pcap_gen_status = ors_pcap_genration_prach(test_case_name=test_case_name,eAxID = eaxid,info_section=config_file)
            if pcap_gen_status != True:
                return pcap_gen_status


        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_load_play_recorde.py'.center(98)))
        pcap_load_and_Play_gen_status = Pcap_Load_and_Data_play_record_(test_case_name=test_case_name,eAxID = eaxid,config_file=config_file)
        if pcap_load_and_Play_gen_status != True:
            return pcap_load_and_Play_gen_status


        time.sleep(3)
        if 'PRACH' not in test_case_name and 'DL' in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'VXT_configuration_result_capture.py'.center(98)))
            vxt_configuration_status = VXT_control(test_case_name,eaxid,ext_gain,config_file=config_file)
            DL_data[eaxid] = vxt_configuration_status[:-1]
            if type(vxt_configuration_status[-1]) == list:
                DL_data[eaxid].append(vxt_configuration_status[-1])

        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'orb_gen.py'.center(98)))
        if 'UL' in test_case_name or 'PRACH' in test_case_name:
            if 'PRACH' not in test_case_name:
                orb_gen_status = Generate_ORB(test_case_name=test_case_name,eAxID = eaxid,config_file=config_file)
                if orb_gen_status != True:
                    return orb_gen_status
            else:
                orb_gen_status = Generate_ORB_prach(test_case_name=test_case_name,eAxID = eaxid,config_file=config_file)
                if orb_gen_status != True:
                    return orb_gen_status

        if 'UL' in test_case_name:
            time.sleep(3)
            print('{0}\n#{1}#\n{0}'.format('*'*100,'vsa_constellation_and_result_capture.py'.center(98)))
            vsa_result_status = VSA_Function(test_case_name=test_case_name,eAxID = eaxid,config_file=config_file)
            UL_data[eaxid] = [eaxid,Center_Freq,bandwidth,vsa_result_status[0],
                                evm_limit,vsa_result_status[2],vsa_result_status[-1],vsa_result_status[1]]
        # DL_data = {'1': ['1', '3.625005', 'FR1_100M', '5.53', '6', '24.17', '23.5', '24.99', 'Pass', 'C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRU_v2\\1.0.20\\2207248400144\\EAXCID2\\Base_DL_UL\\capture.png',[['#6317395Channel', 'Slot', 'CRC Passed', 'Bit Length'], ['PDSCH 1', '0', 'True', '84240'], ['PDSCH 1', '1', 'True', '84240'], ['PDSCH 1', '2', 'True', '84240'], ['PDSCH 1', '3', 'True', '84240'], ['PDSCH 1', '4', 'True', '84240'], ['PDSCH 1', '5', 'True', '84240'], ['PDSCH 1', '6', 'True', '84240'], ['PDSCH 1', '10', 'True', '84240'], ['PDSCH 1', '11', 'True', '84240'], ['PDSCH 1', '12', 'True', '84240'], ['PDSCH 1', '13', 'True', '84240'], ['PDSCH 1', '14', 'True', '84240'], ['PDSCH 1', '15', 'True', '84240'], ['PDSCH 1', '16', 'True', '84240'], ['PDSCH 2', '0', 'True', '792'], ['PDSCH 2', '1', 'True', '792'], ['PDSCH 2', '2', 'True', '792'], ['PDSCH 2', '3', 'True', '792'], ['PDSCH 2', '4', 'True', '792'], ['PDSCH 2', '5', 'True', '792'], ['PDSCH 2', '6', 'True', '792'], ['PDSCH 2', '10', 'True', '792'], ['PDSCH 2', '11', 'True', '792'], ['PDSCH 2', '12', 'True', '792'], ['PDSCH 2', '13', 'True', '792'], ['PDSCH2', '14', 'True', '792'], ['PDSCH 2', '15', 'True', '792'], ['PDSCH 2', '16', 'True', '792'], ['PDSCH 3', '7', 'True', '35640'], ['PDSCH 3', '17', 'True', '35640'], ['PDSCH 4', '7', 'True', '252'], ['PDSCH 4', '17', 'True', '252'], ['PDCCH 1', '0', 'True', '108'], ['PDCCH 1', '1', 'True', '108'], ['PDCCH 1', '2', 'True', '108'], ['PDCCH 1', '3', 'True', '108'], ['PDCCH 1', '4', 'True', '108'], ['PDCCH 1', '5', 'True', '108'], ['PDCCH 1', '6', 'True', '108'], ['PDCCH 1', '7', 'True', '108'], ['PDCCH 1', '10', 'True', '108'], ['PDCCH 1', '11', 'True', '108'], ['PDCCH 1','12', 'True', '108'], ['PDCCH 1', '13', 'True', '108'], ['PDCCH 1', '14', 'True', '108'], ['PDCCH 1', '15', 'True', '108'], ['PDCCH 1', '16', 'True', '108'], ['PDCCH 1', '17', 'True', '108']]]}
        # UL_data = {'1': ['1', '3.625005', 'FR1_100M', '1.4488162994384766', '6', 'Pass', 'C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRU_v2\\1.0.20\\2207248400144\\EAXCID2\\Base_DL_UL',['PUCCH Decoder : Off', 'PUSCH Decoder : On', 'PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0', 'PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0', 'PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1', 'PUSCH_F5_IE :Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1']]}
    
    except Exception as e:
        print(f'TDD_Config Error : {e}')
        return f'TDD_Config Error : {e}'

    finally:
        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'stop_player.py'.center(98)))
        stop_payer_status = Stop_Player()
        print(stop_payer_status)

    if 'DL' in test_case_name and 'UL' in test_case_name:
        return (DL_data, UL_data)
    elif 'DL' in test_case_name:
        return (DL_data)
    else:
        return (UL_data)

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
    start_time = time.time()
    app = QtWidgets.QApplication([])
    config_file = configur['INFO']
    duplex_type = config_file['duplex_type']
    eaxids = config_file['eaxcids'].split(',')
    amplitudes = config_file['amplitude'].split(',')
    external_gain = config_file['external_gain'].split(',')
    RU_Name = config_file['ru_name']
    img_version = config_file['img_version']
    ru_serial_no = config_file['ru_serial_no']
    rf_switch_port = config_file['rf_switch_port'].split(',')
    testing_type = config_file['testing_type']
    bandwidth = config_file['bandwidth']
    present_time = time.localtime()
    time_format = time.strftime('%d_%m_%Y_%I_%M_%S_%p',present_time)
    zip_list = list(zip(rf_switch_port,eaxids,amplitudes,external_gain))
    start_vsa_application()
    print('Making Directrios for each cases....')
    dir_status = make_directories(eaxids,config_file)
    if dir_status != True:
        print(dir_status)
        sys.exit(1000)

    ##################################################################
    ## Check Sync of RU for loading instrument_config.xml
    ##################################################################
    ui = Ui_popup_sync()
    ui.check_sync('Check RU is Sync?')
    if ui.choice == QtWidgets.QMessageBox.Yes:
        pass
    else:
        Result = ORS_instrument_Configuration(config_file)
        Result = True
        if Result!= True:
            print('Instrument Configuration are failed...')
            sys.exit(1)
        else:
            ui.choice = QtWidgets.QMessageBox.question(ui,'Extract!',
                                                "Enter Yes when RU is sync",
                                                QtWidgets.QMessageBox.Yes)
            if ui.choice == QtWidgets.QMessageBox.Yes:
                pass
    time.sleep(5)
    ##################################################################
    ## Mplane connection to check sync state and activating carriers
    ##################################################################
    obj = MPlane_Configuration(config_data=config_file)
    connection = obj.create_connection()
    if type(connection) == bool:
        sys.exit(1000)

    sync_status = obj.CheckSync(connection)
    if sync_status != True:
        sys.exit(1000)

    common_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}"
    csv_file_data = []
    csv_file_path = f"{common_path}/{ru_serial_no}/{bandwidth}/Test_Report_ANT{'_'.join(eaxids)}_{time_format}.csv"
    csv_file = open(csv_file_path, mode='w+', newline='')
    writer = csv.writer(csv_file)
    table_header = ["Antenna ports","Test case","Bandwidth","Channel Power(dBm)","Constellation","EVM(%)","CRC","EVM(%)","Constellation","CRC"]
    writer.writerow(table_header)
    csv_file.close()
    for switch_port,eaxcid,amplitude,ext_gain in zip_list:
        change_comp_status = obj.ChangeCompression(connection,16)
        if change_comp_status != True:
            print(change_comp_status)
            sys.exit(1000)
        notification("\n******************** Compression Change to 16********************\n")
        flag_comp_9 = flag_comp_12 = flag_comp_14 = flag_comp_16 = False
        chn_status = run_ktmswitch("PXI10::0-0.0::INSTR", f"p1ch{switch_port}")
        if chn_status!=True:
            sys.exit(10000)
        report_path = f"{common_path}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/Eaxcid_{eaxcid}_{time_format}.pdf"
        DL_UL_Results = {}
        for test_case in test_cases:
            csv_file_1 = open(csv_file_path, mode='a', newline='')
            writer1 = csv.writer(csv_file_1)
            print('='*100)
            print('Running Test Case is {}'.format(test_case))
            print('='*100)
            notification('Running Test Case is {}'.format(test_case))
            # print(test_cases,duplex_type,eaxcid)
            ##################################################################
            ## Changing the compression
            ##################################################################
            if 'Comp_9' in test_case and flag_comp_9 == False:
                change_comp_status = obj.ChangeCompression(connection,9)
                if change_comp_status != True:
                    print(change_comp_status)
                    sys.exit(1000)
                notification("\n******************** Compression Change to 9********************\n")
                flag_comp_9 = True
            elif 'Comp_12' in test_case and flag_comp_12 == False:
                change_comp_status = obj.ChangeCompression(connection,12)
                if change_comp_status != True:
                    print(change_comp_status)
                    sys.exit(1000)
                notification("\n******************** Compression Change to 12********************\n")
                flag_comp_12 = True
            elif 'Comp_14' in test_case and flag_comp_14 == False:
                change_comp_status = obj.ChangeCompression(connection,14)
                if change_comp_status != True:
                    print(change_comp_status)
                    sys.exit(1000)
                notification("\n******************** Compression Change to 14********************\n")
                flag_comp_14 = True
            elif 'PRACH' in test_case:
                change_comp_status = obj.ChangeCompression(connection,16)
                if change_comp_status != True:
                    print(change_comp_status)
                    sys.exit(1000)
                notification("\n******************** Compression Change to 16********************\n")  
            Result = main(test_case,eaxcid,amplitude,ext_gain,config_file)
            if 'Error' in Result:
                notification(f'Test Case {test_case} || Not Complete Error Occured\n{Result}')
                continue
            notification('Test Case {} || Complete'.format(test_case))
            if 'DL' in test_case and 'UL' in test_case:
                Dl_data,ul_data = list(Result[0].values()),list(Result[1].values())
                DL_UL_Results[test_case] = [Dl_data,ul_data]
                sheet_data = [
                                f"ANT_{Dl_data[0][0]}",test_case,Dl_data[0][2],Dl_data[0][5],'',Dl_data[0][3],
                                Dl_data[0][8],ul_data[0][3],'',ul_data[0][5]
                                ]
                notification(f'''Test Case {test_case} \n{','.join(sheet_data)}''')
            elif 'DL' in test_case and 'UL' not in test_case:
                Dl_data = list(Result.values())
                DL_UL_Results[test_case] = [Dl_data]
                sheet_data = [
                                f"ANT_{Dl_data[0][0]}",test_case,Dl_data[0][2],
                                Dl_data[0][5],'',Dl_data[0][3],Dl_data[0][8],'','',''
                                ]
                notification(f'''Test Case {test_case} \n{','.join(sheet_data)}''')
            elif 'UL' in test_case and 'DL' not in test_case:
                ul_data = list(Result.values())
                DL_UL_Results[test_case] = [ul_data]
                sheet_data = [
                                f"ANT_{ul_data[0][0]}",test_case,ul_data[0][2],
                                '','','','',ul_data[0][3],'',ul_data[0][5]
                                ]
                notification(f'''Test Case {test_case} \n{','.join(sheet_data)}''')
            
            writer1.writerow(sheet_data)
            json_file = open(f"{common_path}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/Eaxcid_{eaxcid}_{time_format}.json", "w+")
            json.dump(DL_UL_Results, json_file,indent=4)
            json_file.close()
            read_file = open(f"{common_path}/{ru_serial_no}/{bandwidth}/EAXCID{eaxcid}/Eaxcid_{eaxcid}_{time_format}.json", "r")
            json_data = json.load(read_file)
            # print(DL_UL_Results)
            generate_report_dl_ul(json_data,report_path,config_file)
            read_file.close()
            csv_file_1.close()
    shutil.copytree(f"{common_path}",f"{common_path}_{time_format}")
    print(f'Logs are saved at location {common_path}_{time_format}')
    end_time = time.time()
    print(f'\n\nTaken_Time_for_Test_case run : {end_time-start_time}')

        