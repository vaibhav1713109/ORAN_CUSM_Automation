import sys
import time
import pyvisa as visa
import os
from configparser import ConfigParser


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
# print("vxt_control.py path :",root_dir)
# sys.exit(100)
from Scripts.vxt_control_new import *

global remote_folder
remote_folder = "C:/Users/Administrator/Documents"
configur = ConfigParser()
configur.read('{}/Requirement/inputs.ini'.format(root_dir))

class vxt_configuratio(vxt_configuration_and_result_capture):
    def __init__(self,test_case_name,ext_gain,eAxID,scpi_commands,screen_shot_name) -> None:
        vxt_configuration_and_result_capture.__init__(self,test_case_name,eAxID,ext_gain)
        self.Ext_Gain = ext_gain
        self.test_case_name = test_case_name
        self.remote_folder = remote_folder
        basic_cmds = [f":CCAR:REF {self.DL_Center_Freq}GHz",":RAD:STAN:PRES:CARR B{}M".format(self.bandwidth),
                    ":RAD:STAN:PRES:FREQ:RANG FR1", f":RAD:STAN:PRES:DMOD {self.duplex_type}", f":RAD:STAN:PRES:SCS SCS{self.scs_val}K",
                    ':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM",
                    ":EVM:CCAR0:DC:PUNC ON",':CORR:BTS:GAIN {}'.format(self.Ext_Gain),':SENS:POW:RF:RANG:OPT IMM']
        self.basic_scpis = scpi_commands
        self.basic_scpis.extend(basic_cmds)
        if not os.path.exists(self.filePathPc):
            os.makedirs(self.filePathPc)

    def make_visa_connection_and_vxt_configuration(self):
        try:
            Visa_status = self.visa_connection(self.vxt_add)
            if not Visa_status:
                time.sleep(1)
                self.clear_status_reg_of_device()
                time.sleep(1)
                self.reset_device()
                time.sleep(2)
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

    #########################################################################################
    ## Capture the Screenshot
    #########################################################################################
    def capture_screenshot(self):
        """Description : Capture the screenshot of present window in VXT and transfer the file from vxt to remote server."""
        try:
            filepath = r"C:\Users\Administrator\Documents\capture.png"
            self.device.write(":MMEM:STOR:SCR '{}'".format(filepath))
            # status = self.device.query('*OPC?')
            print("print taken")
            time.sleep(5)
            # image=r"C:\Users\Administrator\Documents\Keysight\Instrument\NR5G\screen\capture.png"
            ResultData = bytes(self.device.query_binary_values(f'MMEM:DATA? "{filepath}"', datatype='s'))
            # status = self.device.query('*OPC?')
            newFile = open(f"{self.filePathPc}/{screen}.png", "wb")
            newFile.write(ResultData)
            newFile.close()
            print("Constellation Saved")
            return True
        except Exception as e:
            Error = 'Capture_screenshot Error : {}'.format(e)
            print(Error)
            return Error

def VXT_control(test_case_name:str,ext_gain:str,eAxID:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                            f':MMEMory:LOAD:STAT "{remote_file}"', ':CORR:BTS:GAIN {}'.format(ext_gain),':SENS:POW:RF:RANG:OPT IMM'
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    if float(ext_gain)>0:
        ext_gain = float(ext_gain)*(-1)
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,eAxID,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.verify_result_and_capture_screenshot())
    else:
        status.extend([str(config_status),'0','Fail','',[]])
    # print(status)
    # status.insert(0,eaxcid)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    status.insert(5,str(vxt_obj.power_limit[0]))
    status.insert(6,str(vxt_obj.power_limit[1]))
    print(status)
    vxt_obj.disconnect_from_VXT()
    return status

def evm_control(test_case_name:str,ext_gain:str,eAxID:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                            # f':MMEMory:LOAD:STAT "{remote_file}"', ':CORR:BTS:GAIN {}'.format(ext_gain),
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    if float(ext_gain)>0:
        ext_gain = float(ext_gain)*(-1)
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,eAxID,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_EVM())
    else:
        status.extend([config_status,'Fail',''])
    print(status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    status.insert(0,eAxID)
    print(status)
    return status

def base_station_power(test_case_name:str,ext_gain:str,eAxID:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:CHP', ":DISP:CHP:VIEW NORM",":INIT:CONT ON",
                            # f':MMEMory:LOAD:STAT "{remote_file}"', ':CORR:BTS:GAIN {}'.format(ext_gain),
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    if float(ext_gain)>0:
        ext_gain = float(ext_gain)*(-1)
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,eAxID,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_base_station_power())
    else:
        status.extend([config_status,'Fail',''])
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.power_limit[0]))
    status.insert(4,str(vxt_obj.power_limit[1]))
    status.insert(0,eAxID)
    print(status)
    return status

def ccdf_control(test_case_name:str,ext_gain:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:PST', ":DISP:PST:VIEW NORM",":INIT:CONT ON",
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.ccdf_cal())
    else:
        status.extend([config_status,'0','Fail',''])
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,'10')
    print(status)
    return status

def aclr_control(test_case_name:str,ext_gain:str,eAxID:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:ACP', ":DISP:ACP:VIEW NORM",":INIT:CONT ON",
                            # f':MMEMory:LOAD:STAT "{remote_file}"', ':CORR:BTS:GAIN {}'.format(ext_gain),
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,eAxID,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_aclr())
    else:
        config_status = config_status.rsplit(' ',1)
        status.extend([config_status[0],config_status[1],'0','Fail',''])
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(-2,'<-45')
    status.insert(0,eAxID)
    print(status)
    return status

def Occupied_bandwidth(test_case_name:str,ext_gain:str,eAxID:str):
    remote_file = f"{remote_folder}/RCT/StateFiles/{test_case_name}.state"
    scpi_commands = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:OBW', ":DISP:OBW:VIEW NORM",":INIT:CONT ON",
                            f':MMEMory:LOAD:STAT "{remote_file}"', ':CORR:BTS:GAIN {}'.format(ext_gain),
                            ]
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ext_gain,eAxID,scpi_commands)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.Occupied_band())
    else:
        status.extend([config_status,'Fail',''])
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status

def tpdr(test_case_name,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_EVM_power())
        vxt_obj.capture_screenshot()
        status = status[1:]
        status.append(vxt_obj.filePathPc)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status

def t_on_off_p(test_case_name,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.T_ON_OFF_P())
    else:
        status.append(config_status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status

def freq_error(test_case_name,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_freq_error())
    else:
        status.append(config_status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,'+-300')
    print(status)
    return status

def O_B_U_E(test_case_name,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuratio(test_case_name,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.OBUE())
    else:
        status.extend(config_status.rsplit(' ',4))
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status

if __name__ == "__main__":
    start_time = time.time()
    print('='*100)
    if len(sys.argv) > 3:
        RU_Name = configur.get('INFO','ru_name')
        ru_serial_no = configur.get('INFO','ru_serial_no')
        test_case_name = sys.argv[1]
        eaxcid = sys.argv[2]
        ext_gain = sys.argv[3]
        # evm_res = evm_control(test_case_name,ext_gain,eaxcid)
        # evm_res = ['1', '3.700005', 'FR1_10M', '3.50', '3', 'Fail', 'c:\\Automation\\FH_Testing/Results/RCT/LPRU_v7/3.0.2/2309348300005_10M/FR1_10M/EAXCID1/Base_DL_UL']
        # aclr_res = aclr_control(test_case_name,ext_gain,eaxcid)
        # aclr_res = ['1', '3.700005', 'FR1_10M', '-51.31622997', '-52.20732297', '<-45', 'Pass', 'c:\\Automation\\FH_Testing/Results/RCT/LPRU_v7/3.0.2/2309348300005_10M/FR1_10M/EAXCID1/Base_DL_UL/capture.png']
        # bs_power_res = base_station_power(test_case_name,ext_gain,eaxcid)
        # bs_power_res = ['1', '3.700005', 'FR1_10M', '21.38', '23', '24.99', 'Fail', 'c:\\Automation\\FH_Testing/Results/RCT/LPRU_v7/3.0.2/2309348300005_10M/FR1_10M/EAXCID1/Base_DL_UL/capture.png']
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