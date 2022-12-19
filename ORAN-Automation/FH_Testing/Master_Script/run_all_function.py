import sys
import os,json
import time, shutil
from configparser import ConfigParser
import subprocess,csv

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)
configur = ConfigParser()
configur.read('{}/Requirement/inputs.ini'.format(root_dir))
sys.path.append(root_dir)
# from Scripts.scp_gen import *
from Scripts.scp_load import *
from Scripts.pcap_gen import *
from Scripts.pcap_load_play_recorde import *
from Scripts.vxt_control_new import *
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
# from Scripts.compression_change import *
from Scripts.notification import *

def main(test_case_name,test_case_id,eaxid,amplitude,ext_gain):
    # python_path = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
    python_path = 'python'
    DL_data = {}
    UL_data = {}
    Center_Freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    power_limit = configur.get('INFO','power_limit').split(',')
    evm_limit = configur.get('INFO','evm_limit')
    try:
        print('{0}\n#{1}#\n{0}'.format('*'*100,'scp_gen.py'.center(98)))
        scp_gen_status = load_scp(test_case_name=test_case_name,test_case_id=test_case_id,eAxID=eaxid,amplitude=amplitude)
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


        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'pcap_load_play_recorde.py'.center(98)))
        pcap_load_and_Play_gen_status = Pcap_Load_and_Data_play_record_(test_case_name=test_case_name,eAxID = eaxid)
        if pcap_load_and_Play_gen_status != True:
            return pcap_load_and_Play_gen_status


        time.sleep(3)
        if 'PRACH' not in test_case_name and 'DL' in test_case_name:
            print('{0}\n#{1}#\n{0}'.format('*'*100,'VXT_configuration_result_capture.py'.center(98)))
            vxt_configuration_status = VXT_control(test_case_name,eaxid,ext_gain)
            DL_data[eaxid] = vxt_configuration_status[:-1]
            if type(vxt_configuration_status[-1]) == list:
                DL_data[eaxid].append(vxt_configuration_status[-1])

        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'orb_gen.py'.center(98)))
        if 'UL' in test_case_name or 'PRACH' in test_case_name:
            if 'PRACH' not in test_case_name:
                orb_gen_status = Generate_ORB(test_case_name=test_case_name,eAxID = eaxid)
                if orb_gen_status != True:
                    return orb_gen_status
            else:
                orb_gen_status = Generate_ORB_prach(test_case_name=test_case_name,eAxID = eaxid)
                if orb_gen_status != True:
                    return orb_gen_status

        if 'UL' in test_case_name:
            time.sleep(3)
            print('{0}\n#{1}#\n{0}'.format('*'*100,'vsa_constellation_and_result_capture.py'.center(98)))
            vsa_result_status = VSA_Function(test_case_name=test_case_name,eAxID = eaxid)
            UL_data[eaxid] = [eaxid,Center_Freq,bandwidth,vsa_result_status[0],
                                evm_limit,vsa_result_status[2],vsa_result_status[-1],vsa_result_status[1]]
    
    except Exception as e:
        print(f'TDD_Config Error : {e}')
        return f'TDD_Config Error : {e}'

    finally:
        time.sleep(3)
        print('{0}\n#{1}#\n{0}'.format('*'*100,'stop_player.py'.center(98)))
        stop_payer_status = Stop_Player()
        print(stop_payer_status)

    # DL_data = {'1': ['1', '3.625005', 'FR1_100M', '5.53', '6', '24.17', '23.5', '24.99', 'Pass', 'C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRU_v2\\1.0.20\\2207248400144\\EAXCID2\\Base_DL_UL\\capture.png',[['#6317395Channel', 'Slot', 'CRC Passed', 'Bit Length'], ['PDSCH 1', '0', 'True', '84240'], ['PDSCH 1', '1', 'True', '84240'], ['PDSCH 1', '2', 'True', '84240'], ['PDSCH 1', '3', 'True', '84240'], ['PDSCH 1', '4', 'True', '84240'], ['PDSCH 1', '5', 'True', '84240'], ['PDSCH 1', '6', 'True', '84240'], ['PDSCH 1', '10', 'True', '84240'], ['PDSCH 1', '11', 'True', '84240'], ['PDSCH 1', '12', 'True', '84240'], ['PDSCH 1', '13', 'True', '84240'], ['PDSCH 1', '14', 'True', '84240'], ['PDSCH 1', '15', 'True', '84240'], ['PDSCH 1', '16', 'True', '84240'], ['PDSCH 2', '0', 'True', '792'], ['PDSCH 2', '1', 'True', '792'], ['PDSCH 2', '2', 'True', '792'], ['PDSCH 2', '3', 'True', '792'], ['PDSCH 2', '4', 'True', '792'], ['PDSCH 2', '5', 'True', '792'], ['PDSCH 2', '6', 'True', '792'], ['PDSCH 2', '10', 'True', '792'], ['PDSCH 2', '11', 'True', '792'], ['PDSCH 2', '12', 'True', '792'], ['PDSCH 2', '13', 'True', '792'], ['PDSCH2', '14', 'True', '792'], ['PDSCH 2', '15', 'True', '792'], ['PDSCH 2', '16', 'True', '792'], ['PDSCH 3', '7', 'True', '35640'], ['PDSCH 3', '17', 'True', '35640'], ['PDSCH 4', '7', 'True', '252'], ['PDSCH 4', '17', 'True', '252'], ['PDCCH 1', '0', 'True', '108'], ['PDCCH 1', '1', 'True', '108'], ['PDCCH 1', '2', 'True', '108'], ['PDCCH 1', '3', 'True', '108'], ['PDCCH 1', '4', 'True', '108'], ['PDCCH 1', '5', 'True', '108'], ['PDCCH 1', '6', 'True', '108'], ['PDCCH 1', '7', 'True', '108'], ['PDCCH 1', '10', 'True', '108'], ['PDCCH 1', '11', 'True', '108'], ['PDCCH 1','12', 'True', '108'], ['PDCCH 1', '13', 'True', '108'], ['PDCCH 1', '14', 'True', '108'], ['PDCCH 1', '15', 'True', '108'], ['PDCCH 1', '16', 'True', '108'], ['PDCCH 1', '17', 'True', '108']]]}
    # UL_data = {'1': ['1', '3.625005', 'FR1_100M', '1.4488162994384766', '6', 'Pass', 'C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRU_v2\\1.0.20\\2207248400144\\EAXCID2\\Base_DL_UL',['PUCCH Decoder : Off', 'PUSCH Decoder : On', 'PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0', 'PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2', 'PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0', 'PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1', 'PUSCH_F5_IE :Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1']]}
    # if 'DL' in test_case_name and 'UL' in test_case_name:
    #     return DL_data, UL_data
    # elif 'DL' in test_case_name:
    #     return DL_data
    # else:
    #     return UL_data

def run_ktmswitch(channelnumbers:str):
    print("------------------Starting the Channel no. {0}---------------------------\n\n\n".format(channelnumbers))
    CMD = f'''{root_dir}/Requirement/KtMSwitch_Cpp_CloseChannel.exe PXI10::0-0.0::INSTR p1ch{channelnumbers}'''
    output = os.system(CMD)
    print(output)
    ########## Check the status of RF Switch #############
    if type(output) == int and output != 0:
        print('-'*50)
        print('\n\n Please Connect the Type C USB with RF Switch...')
        print('-'*50)
        return False
    return True

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
    if len(sys.argv) >=2:
        time_format = sys.argv[1]
        information = configur['INFO']
        eaxid = information['eaxcids']
        RU_Name = information['ru_name']
        img_version = information['img_version']
        test_case = information['summary']
        test_case_id = information['test case id']
        ru_serial_no = information['ru_serial_no']
        amplitude = information['amplitude']
        ext_gain = information['external_gain']
        json_file_1 = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/{test_case}/{test_case}_{time_format}.json"
        DL_UL_Results = {}
        # obj = MPlane_Configuration()
        # connection = obj.create_connection()
        # run_ktmswitch(eaxid)
        # if type(connection) == bool:
        #     sys.exit(1000)
        print('='*100)
        print('Running Test Case is {}'.format(test_case))
        print('='*100)
        ###############################################################################
        ## Changing the compression
        ###############################################################################
        # if 'Comp_9' in test_case:
        #     change_comp_status = obj.ChangeCompression(connection,9)
        #     if change_comp_status != True:
        #         print(change_comp_status)
        #         sys.exit(1000)
        # elif 'Comp_12' in test_case:
        #     change_comp_status = obj.ChangeCompression(connection,12)
        #     if change_comp_status != True:
        #         print(change_comp_status)
        #         sys.exit(1000)
        # elif 'Comp_14' in test_case:
        #     change_comp_status = obj.ChangeCompression(connection,14)
        #     if change_comp_status != True:
        #         print(change_comp_status)
        #         sys.exit(1000)
        # elif 'PRACH' in test_case:
        #     change_comp_status = obj.ChangeCompression(connection,16)
        #     if change_comp_status != True:
        #         print(change_comp_status)
        #         sys.exit(1000)
        # else:
        #     change_comp_status = obj.ChangeCompression(connection,16)
        #     if change_comp_status != True:
        #         print(change_comp_status)
        #         sys.exit(1000)
        Result = main(test_case,test_case_id,eaxid,amplitude,ext_gain)

        ###############################################################################
        ## Verifying the result
        ###############################################################################
        if 'Error' in Result:
            # notification(f'Test Case {test_case} || Not Complete Error Occured\n{Result}')
            sys.exit(1000)
        if type(Result) == tuple and len(Result) >= 2 and 'DL' in test_case and 'UL' in test_case:
            Dl_data,ul_data = list(Result[0].values()),list(Result[1].values())
            DL_UL_Results[f"{test_case}"] = [Dl_data,ul_data]
            sheet_data = [f"ANT_{Dl_data[0][0]}",test_case,Dl_data[0][2],
                        Dl_data[0][5],'',Dl_data[0][3],Dl_data[0][8],
                        ul_data[0][3],'',ul_data[0][5]]
            # notification(f'Test Case {test_case} \n{sheet_data}')
        elif 'DL' in test_case and 'UL' not in test_case:
            DL_UL_Results[f"{test_case}"] = [list(Result.values())]
            Ul_data = list(Result[0].values())
            sheet_data = [
                        f"ANT_{Ul_data[0][0]}",test_case,Ul_data[0][2],
                        '','','','',Ul_data[0][3],'',Ul_data[0][5]
                        ]
            # notification(f'Test Case {test_case} \n{sheet_data}')
        elif 'UL' in test_case and 'DL' not in test_case:
            DL_UL_Results[f"{test_case}"] = [list(Result.values())]
            Dl_data = list(Result[0].values())
            sheet_data = [f"ANT_{Dl_data[0][0]}",test_case,Dl_data[0][2],
                        Dl_data[0][5],'',Dl_data[0][3],Dl_data[0][8],'','','']
            # notification(f'Test Case {test_case} \n{sheet_data}')
        
        ###############################################################################
        ## Appending the data into CSV file
        ###############################################################################
        csv_file_path = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/Eaxcid_{eaxid}_{time_format}.csv"
        if os.path.exists(csv_file_path):
            csv_file_1 = open(csv_file_path, mode='a', newline='')
            writer1 = csv.writer(csv_file_1)
            writer1.writerow(sheet_data)
            csv_file_1.close()
        else:
            csv_file_1 = open(csv_file_path, mode='w+', newline='')
            writer1 = csv.writer(csv_file_1)
            header = ["Antenna ports","Test case","Bandwidth","Channel Power(dBm)","Constellation","EVM(%)","CRC","EVM(%)","Constellation","CRC"]
            writer1.writerow(header)
            writer1.writerow(sheet_data)
            csv_file_1.close()
            
        ###############################################################################
        ## Appending the data into Json file for genrating PDF
        ###############################################################################
        json_file_1 = open(json_file_1,'w+')
        json.dump(DL_UL_Results, json_file_1,indent=4)
        json_file_1.close()
        # report_path = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/{test_case}/{test_case}_{time_format}.pdf"
        # generate_report_dl_ul(DL_UL_Results,report_path)
    else:
        pass
