import pyvisa
import time,os,sys,csv
from tabulate import tabulate
from configparser import ConfigParser


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)
sys.path.append(root_dir)
from Scripts.generate_report import *
from Scripts.vxt_control_new import *


class vxt_configuration(vxt_configuration_and_result_capture):
    def __init__(self,test_case_name,eAxID,ext_gain,config_file) -> None:
        vxt_configuration_and_result_capture.__init__(self,test_case_name,eAxID,ext_gain,config_file)
        self.base_extended = [
                    ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                    ":CCAR:REF {}GHZ".format(self.DL_Center_Freq),":RAD:STAN:PRES:CARR B{}M".format(self.bandwidth),":RAD:STAN:PRES:FREQ:RANG FR1",
                    f":RAD:STAN:PRES:DMOD {self.duplex_type}", f":RAD:STAN:PRES:SCS SCS{self.scs_val}K", ':RAD:STAN:PRES:RBAL DLTM1DOT1',
                    ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO ON", ":EVM:CCAR0:PDCC1:INCL ON",
                    ":EVM:CCAR0:DEC:PDSC DESCrambled", ":EVM:CCAR0:DEC:PDCC DESCrambled", ":EVM:CCAR0:DEC:PBCH DESCrambled", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS:TABL TABL2",
                    ":EVM:CCAR0:PDSC1:MCS 4", ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 4",
                    ":EVM:CCAR0:PDSC3:MCS:TABL TABL2", ":EVM:CCAR0:PDSC3:MCS 4", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2",
                    ":EVM:CCAR0:PDSC4:MCS 4", ":CORR:BTS:GAIN {}".format(self.Ext_Gain)
                        ]
        self.compression_scpi_64_qam = [
                    ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                    ":CCAR:REF {}GHZ".format(self.DL_Center_Freq),":RAD:STAN:PRES:CARR B{}M".format(self.bandwidth),
                    ":RAD:STAN:PRES:FREQ:RANG FR1", f":RAD:STAN:PRES:DMOD {self.duplex_type}", f":RAD:STAN:PRES:SCS SCS{self.scs_val}K",
                    ':RAD:STAN:PRES:RBAL DLTM3DOT1', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM",
                    ":EVM:CCAR0:DC:PUNC ON",":EVM:CCAR0:PDCC1:INCL ON", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":EVM:CCAR0:DEC:PDCC DESCrambled", ":EVM:CCAR0:DEC:PBCH DESCrambled",
                    ":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS 19",
                    ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 19", ":EVM:CCAR0:PDSC3:MCS:TABL TABL2",
                    ":EVM:CCAR0:PDSC3:MCS 19", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2", ":EVM:CCAR0:PDSC4:MCS 19",
                    ":CORR:BTS:GAIN {}".format(self.Ext_Gain)
                    ]
        self.compression_scpi_256_qam = [
                    ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                    ":CCAR:REF {}GHZ".format(self.DL_Center_Freq),":RAD:STAN:PRES:CARR B{}M".format(self.bandwidth),
                    ":RAD:STAN:PRES:FREQ:RANG FR1", f":RAD:STAN:PRES:DMOD {self.duplex_type}", f":RAD:STAN:PRES:SCS SCS{self.scs_val}K",
                    ':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM",
                    ":EVM:CCAR0:DC:PUNC ON",":EVM:CCAR0:PDCC1:INCL ON", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":EVM:CCAR0:DEC:PDCC DESCrambled", ":EVM:CCAR0:DEC:PBCH DESCrambled",
                    ":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS 27",
                    ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 27", ":EVM:CCAR0:PDSC3:MCS:TABL TABL2",
                    ":EVM:CCAR0:PDSC3:MCS 27", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2", ":EVM:CCAR0:PDSC4:MCS 27",
                    ":CORR:BTS:GAIN {}".format(self.Ext_Gain)
                    ]
        if 'Comp' in self.test_case_name and '256' in self.test_case_name:
            self.basic_scpis = self.compression_scpi_256_qam
        elif '64_QAM_Comp' in self.test_case_name:
            self.basic_scpis = self.compression_scpi_64_qam
        elif '16_QAM' in self.test_case_name:
            self.basic_scpis = self.compression_scpi_16_qam
        else:
            self.basic_scpis = self.base_extended

    def make_visa_connection_and_vxt_configuration(self):
        try:
            Visa_status = self.visa_connection(self.vxt_add)
            if not Visa_status:
                time.sleep(1)
                self.clear_status_reg_of_device()
                time.sleep(1)
                self.reset_device()
                time.sleep(2)
                if '16_QAM' in self.test_case_name:
                    self.basic_scpis = self.compression_scpi_16_qam
                if self.vxt_configuration(self.basic_scpis):
                    return True
                else:
                    print("VXT Configuration are Failed.")
                    return 'VXT Configuration are Failed.'
            else:
                return Visa_status
        except Exception as e:
            Error = f'make_visa_connection_and_vxt_configuration Error : {e}'
            print(Error)
            return Error


def VXT_control(test_case_name,eaxcid,ext_gain,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    if float(ext_gain)>0:
        ext_gain = float(ext_gain)*(-1)
    vxt_obj = vxt_configuration(test_case_name,eaxcid,ext_gain,config_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.verify_result_and_capture_screenshot())
    else:
        status.extend([str(config_status),'0','Fail','',[]])
    # print(status)
    status.insert(0,eaxcid)
    status.insert(1,center_freq)
    status.insert(2,bandwidth)
    status.insert(4,str(vxt_obj.evm_limit))
    status.insert(6,str(vxt_obj.power_limit[0]))
    status.insert(7,str(vxt_obj.power_limit[1]))
    print(status)
    vxt_obj.disconnect_from_VXT()
    return status


if __name__=="__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    start_time = time.time()
    print('='*100)
    if len(sys.argv) > 2:
        DL_data = {}
        crc_data = {}
        RU_Name = information['ru_name']
        img_version = information['img_version']
        Center_Freq = information['tx_center_frequency']
        bandwidth = information['bandwidth']
        power_limit = information['power_limit'].split(',')
        evm_limit = information['evm_limit']
        ru_serial_no = information['ru_serial_no']
        test_case_name = sys.argv[1]
        eaxcid = sys.argv[2]
        print(test_case_name)
        Result = VXT_control(test_case_name,eaxcid,sys.argv[3],information)
        DL_data[sys.argv[1]] = [Result]
        print(DL_data)
    else:
        print('Please run with below format\npython VXT_configuration_result_capture.py {test_case_name} {eaxcid} {ext_gain}')
    # Occupied_bandwidth_Result = Occupied_bandwidth("tm_1_1_ob.state", "tm_1_1_ob.png")
    # # print(aclr_control("ACLR_TM_1_1.state", "ACLR_TM_1_1.png"))
    # # print(base_station_power("Power_TM_1_1.state", "Power_TM_1_1.png"))
    # t_on_off_p = t_on_off_p("tm1_1_t_on_off_p.state", "tm1_1_t_on_off_p.png")
    # # print(freq_error("TM_1_1.state", "TM_1_1_freq_error.png"))
    # report_path = '{}/CUPLANE/TestMac/Results/occupied_bandwidth_report.pdf'.format(root_dir)
    # genrate_report_ocuupied_bandwidth([Occupied_bandwidth_Result],report_path)
    # OBUE_result = O_B_U_E("TM_1_1_OBUE_Small.state", "TM_1_1_OBUE_Small.png")
    # power_result = tpdr("TM_3_1a.state", "TM_3_1a.png")
    # print(power_result)
    # print('='*100)
    end_time = time.time()
    print(f'\n\nTaken_Time_for_vxt_scp_recall : {end_time-start_time}')
        # vxt_obj.visa_connection(vxt_obj.vxt_add)
        # vxt_obj.Check_EVM_power()
