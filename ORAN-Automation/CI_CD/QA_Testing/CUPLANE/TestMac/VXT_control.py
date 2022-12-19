import sys
import time
import pyvisa as visa
import os
from configparser import ConfigParser
from genrate_report import *

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# parent_dir = os.path.dirname(os.path.abspath(__file__))
print("parent_dir",parent_dir)
root_dir = os.path.dirname(parent_dir)
print(root_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))

class vxt_configuration_and_result_capture():
    def __init__(self,file_name,ScreenShot,bandwidth) -> None:
        self.vxt_add = configur.get('CUPlane','vxt_add')
        self.bandwidth = bandwidth
        self.state_file = file_name
        self.external_gain = configur.get('CUPlane','external_gain')
        self.center_frequency = configur.get('INFO','tx_center_frequency')
        self.Local_path = "{}/StateFiles/".format(parent_dir)
        self.remote_folder = "C:\\Users\\Administrator\\Documents\\CU_Plane_Conf"
        self.evm_limit = 2.5
        self.power_limit = [21.5,25.5]
        self.clgc_gain_calculation_time = 10
        """
        self.basic_scpis = [
                    ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:EVM', ":DISP:EVM:VIEW NORM",
                    ":INIT:CONT ON",f'''MMEMory:LOAD:EVM:SET ALL,"{self.scp_path}"''']
        """
        remote_file = os.path.normpath(self.remote_folder+"\\"+self.state_file)
        #cmd = f'MMEM:LOAD:STAT "{self.remote_folder}{self.state_file}"'
        self.basic_scpis = [f':MMEMory:LOAD:STAT "{remote_file}"',':CORR:BTS:GAIN {}'.format(self.external_gain),
                            f':CCAR:REF {self.center_frequency}GHz',f":RAD:STAN:PRES:CARR B{self.bandwidth}M",":INITiate:RESTart", ':SENS:POW:RANG:OPT IMM']
        #filePathPc1 = "/comon-space/QA_Testing/CUPLANE/Results/"
        filePathPc1 = "{}/Results/".format(parent_dir)
        self.filePathPc = os.path.normpath(filePathPc1+ScreenShot)
        self.crc_file_name = "{0}\\Meas.csv".format(self.remote_folder)

    #########################################################################################
    ## Make visa connection
    #########################################################################################
    def visa_connection(self,vxt_add = None, gpib_id= None):
        try:
            if(vxt_add):
                self.rm = visa.ResourceManager()
                self.device = self.rm.open_resource(vxt_add)
                self.device.timeout = 25000
                print(f'Connected to {self.device}')
                return 0
            elif(gpib_id):
                self.rm = visa.ResourceManager()
                self.device = self.rm.open_resource('GPIB0::{}::INSTR'.format(gpib_id)) 
                return 0       
            else:
                Error = 'Visa_connection Error: No valid instrument IP or GBIB ID given'
                print(Error)
                return 100
        except Exception as e:
            Error = f'Visa_connection Error : {e}'
            print(Error)
            return 100
        
    #########################################################################################
    ## Occupied bandwidth
    #########################################################################################
    def Occupied_band(self):
        occupied_bandwidth = '0'
        Error = ''
        time.sleep(2)
        try:
            CMD = ':FETC:OBWidth1?'
            Res = self.device.query_ascii_values(CMD)
            time.sleep(1)
            occupied_bandwidth = str(Res[0]/10**6)
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'Occupied_bandwidth_error : {}'.format(e)
            print(Error)
            return Error,'Fail', self.filePathPc
        if occupied_bandwidth:
            return occupied_bandwidth,'Pass', self.filePathPc
        else:
            return occupied_bandwidth,'Fail', self.filePathPc
    #########################################################################################
    ## Send state file to the VXT for vxt configuration
    #########################################################################################
    def send_file_to_vxt(self, local_path,file_name,remote_path):
        error = ''
        for _ in range(10):
            try:
                if not self.device:
                    print("Device not connected")
                    return 100
                local_file = os.path.join(local_path, file_name)
                if not os.path.isfile(local_file):
                    print(f"File not found: {local_file}")
                    return f"File not found: {local_file}"
                    return 404

                with open(local_file, 'rb') as f:
                    read_data = f.read()

                #remote_file = os.path.join(remote_path, file_name)
                rem_file = os.path.normpath(remote_path+'\\'+file_name)            
                self.device.write(f':MMEMory:MDIRectory "{remote_path}"')
                self.device.write_binary_values(f':MMEMory:DATA "{rem_file}",', read_data, datatype='B')
                status_complete = self.device.query("*OPC?")
                if int(status_complete) != 1:
                    print("not completed",status_complete)
                    error = f'send_file_to_VXT Error: Failed to transfer {local_file} to {rem_file}'
                    return error
                else:
                    print(f'File {local_file} successfully transferred to {rem_file}')
                    return 0
                # include one more SCPI for file check here

            except Exception as e:
                error = f'send_file_to_VXT Error: {e}'
        else:
            print(error)
            return 500
    
    def clear_status_reg_of_device(self):
        self.device.write('*CLS')                                #Clear Status Register of device
        self.device.write('*WAI')                                #Wait till Clear command is complete

    #########################################################################################
    ## Reseting the VXT 
    #########################################################################################
    def reset_device(self):
        self.device.write('*RST')                                #Reset the device
        self.device.write('*WAI')                                #Wait till Reset command is complete

    #########################################################################################
    ## Write scpi value
    #########################################################################################
    def scpi_write(self, cmnd):
        Error = ''
        self.device.write(cmnd)
        #self.device.write('*WAI')
        for _ in range(1):
            try:
                status = self.device.query("*OPC?")
                print(cmnd,status[0])
                if status[0] == '1': # Check for any error during the execution of SCPI command
                    return 1
            except Exception as e:
                Error = f'scpi_write Error {cmnd} : {e}'
                print(Error)
                time.sleep(1)
        else:
            return Error

    #########################################################################################
    ## Run the scpi of vxt for configuration
    #########################################################################################
    def vxt_configuration(self,scpi_cmds):
        try:
            for scpi in scpi_cmds:
                self.scpi_write(scpi)
            return True
        except Exception as e:
            Error = f'vxt_configuration Error : {e}'
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
            newFile = open(self.filePathPc, "wb")
            newFile.write(ResultData)
            newFile.close()
            print("Constellation Saved")
            return True
        except Exception as e:
            Error = 'Capture_screenshot Error : {}'.format(e)
            print(Error)
            return Error

    #########################################################################################
    ## Fetching EVM and power from modulation window
    #########################################################################################
    def fetch_EVM_power(self):
        Error = ''
        captured_evm = 0
        output_power = 0
        time.sleep(2)
        try:
            CMD = ':FETCh:EVM000001?'
            Res = self.device.query_ascii_values(CMD)
            #time.sleep(1)
            # print(Res)
            captured_evm = "{:.2f}".format(float(Res[1]))
            output_power = "{:.2f}".format(float(Res[22]))
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_EVM_power Error : {}'.format(e)
            print(Error)
            return "failed","failed",100
        if float(captured_evm) < float(self.evm_limit) and (float(output_power) > float(self.power_limit[0]) and float(output_power) < float(self.power_limit[1])):
            return captured_evm,output_power, True
        else:
            return captured_evm,output_power, False
    
    #########################################################################################
    ## Verify CRC value in DL
    #########################################################################################
    def verify_CRC(self):
        time.sleep(10)
        cmd = ':MMEM:STOR:RES "{}"'.format(self.crc_file_name)
        self.scpi_write(cmd)
        data_list = []
        Error = ''
        crc_pass = crc_fail = 0
        for _ in range(10):
            try:
                filepath = "{}_CC0Bits.csv".format(self.crc_file_name.split('.')[0])
                cmd = f':MMEM:DATA? "{filepath}"'
                ResultData = self.device.query(cmd)
                ResultData = ResultData.split('\n')
                for lines in ResultData:
                    lines = lines.split(',')
                    if len(lines) > 4:
                        data_list.append([lines[0],lines[1],lines[2],lines[3]])
                        if lines[2] == 'True':
                            crc_pass+=1
                        elif lines[2] == 'False':
                            crc_fail+=1
                print('*'*100)
                print(f'CRC Pass = {crc_pass}\nCRC Fail = {crc_fail}')
                print('*'*100)
                print("CRC Captured")
                if crc_fail > 0:
                    return data_list, False
                else:
                    return data_list, True
            except Exception as e:
                Error = 'Verify_CRC Error : {}'.format(e)
                # status = self.device.query(':SYST:ERR?')
                # print(status)
                print(Error)
        else:
            return Error

    #########################################################################################
    ## Fetching EVM and power from modulation window
    #########################################################################################
    def fetch_EVM(self):
        Error = ''
        captured_evm = 0
        time.sleep(2)
        try:
            CMD = ':FETCh:EVM000001?'
            Res = self.device.query_ascii_values(CMD)
            print(Res)
            captured_evm = "{:.2f}".format(float(Res[1]))
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_EVM Error : {}'.format(e)
            print(Error)
            return Error, 'Fail', self.filePathPc
        if float(captured_evm) < float(self.evm_limit):
            return captured_evm, 'Pass',self.filePathPc
        else:
            return captured_evm, 'Fail',self.filePathPc
        
    #########################################################################################
    ## Fetching EVM and power from modulation window
    #########################################################################################
    def fetch_base_station_power(self):
        Error = ''
        Output_Power = 0
        time.sleep(2)
        try:
            CMD = ':FETC:CHP?'
            Res = self.device.query_ascii_values(CMD)
            # Res = Res.split(',')
            print(Res)
            Output_Power = "{:.2f}".format(float(Res[0]))
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_base_station_power Error : {}'.format(e)
            print(Error)
            return Error, 'Fail', self.filePathPc
        if (float(Output_Power) > float(self.power_limit[0]) and float(Output_Power) < float(self.power_limit[1])):
            return Output_Power, 'Pass',self.filePathPc
        else:
            return Output_Power, 'Fail',self.filePathPc
        
    #########################################################################################
    ## Fetching EVM and power from modulation window
    #########################################################################################
    def fetch_aclr(self):
        Error = ''
        # aclr = [0,0,0,0]
        aclr = [0,0]
        time.sleep(2)
        try:
            CMD = ':FETC:ACP?'
            OUT = self.device.query_ascii_values(CMD)
            # aclr[0],aclr[1],aclr[2],aclr[3] = OUT[4],OUT[6],OUT[8],OUT[10]
            aclr[0],aclr[1] = str(OUT[4]),str(OUT[6])
            time.sleep(1)
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_aclr Error : {}'.format(e)
            print(Error)
            return Error,'Fail', self.filePathPc
        if float(aclr[0]) < -45 and float(aclr[1]) < -45:
            return *aclr,'Pass', self.filePathPc
        else:
            return *aclr,'Fail', self.filePathPc
    
    #########################################################################################
    ## Fetching EVM and power from modulation window
    #########################################################################################
    def fetch_freq_error(self):
        Error = ''
        freq_error = 0
        time.sleep(2)
        try:
            CMD = ':FETCh:EVM000001?'
            Res = self.device.query_ascii_values(CMD)
            print(Res)
            freq_error = "{:.2f}".format(float(Res[3]))
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_freq_error Error : {}'.format(e)
            print(Error)
            return Error, 'Fail', self.filePathPc
        if float(freq_error) < 300 and float(freq_error) > -300:
            return freq_error, 'Pass',self.filePathPc
        else:
            return freq_error, 'Fail',self.filePathPc
    
    #########################################################################################
    ## Verifying the Transmitter ON OFF power and save the screenshot
    #########################################################################################
    def T_ON_OFF_P(self):
        result = [0,0]
        Error = ''
        time.sleep(2)
        try:
            CMD = ':FETC:PVTime?'
            Res = self.device.query_ascii_values(CMD)
            time.sleep(1)
            result[0] = str(Res[6]*10**9)
            result[1] = str(Res[7])
            # print(result)
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'T_ON_OFF_POWER Error : {}'.format(e)
            print(Error)
            return *result,'Fail', self.filePathPc
        if result:
            return *result,'Pass', self.filePathPc
        else:
            return *result,'Fail', self.filePathPc
        
    def OBUE(self):
        result = []
        result1 = []
        Error = ''
        time.sleep(2)
        try:
            CMD = ':FETCh:SEMask1?'
            Res = self.device.query_ascii_values(CMD)
            time.sleep(1)
            itera = [13, 70, 23, 71, 33, 74, 43, 76, 53, 78]
            for i in itera:
                result.append(Res[i])
            
            result1 = [str(result[0]-result[1]),str(result[2]-result[3]),str(result[4]-result[5]),str(result[6]-result[7]),str(result[8]-result[9])]
            print(result1)
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'OBUE Error : {}'.format(e)
            print(Error)
            return *result1,'Fail', self.filePathPc
        print(result[2]-result[3])
        if (result[0]-result[1]) <= -34.5 and (result[2]-result[3]) <= -35.2 and (result[4]-result[5]) <= -37 and (result[6]-result[7]) <= -37 and (result[8]-result[9]) <= -37:
            return *result1,'Pass', self.filePathPc
        else:
            return *result1,'Fail', self.filePathPc
        
    #########################################################################################
    ## Verifying the DL result for EVM, CRC, power and save the screenshot
    #########################################################################################
    def verify_result_and_capture_screenshot(self):
        try:
            crc_data = self.verify_CRC()
            power_evm_result = self.fetch_EVM_power()
            #filepath = r"C:\temp\capture.png"
            time.sleep(5)
            filepath = r"C:\Users\Administrator\Documents\capture.png"
            self.device.write(":MMEM:STOR:SCR '{}'".format(filepath))
            # status = self.device.query('*OPC?')
            print("print taken")
            time.sleep(5)
            # image=r"C:\Users\Administrator\Documents\Keysight\Instrument\NR5G\screen\capture.png"
            ResultData = bytes(self.device.query_binary_values(f'MMEM:DATA? "{filepath}"', datatype='s'))
            # status = self.device.query('*OPC?')
            newFile = open(self.filePathPc, "wb")
            newFile.write(ResultData)
            newFile.close()
            print("Constellation Saved")
            if power_evm_result[-1] != True or crc_data[-1] != True:
                Error = f"{'*'*100}\nFail due to unexpected Power or EVM \nChannel Power : {power_evm_result[1]} \nEVM : {power_evm_result[0]}\n{'*'*100}"
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(Error)
                return captured_evm, output_power, 'Fail', self.filePathPc, crc_data[0]
            else:
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(f"{'*'*100}\nChannel Power : {output_power}\nEVM : {captured_evm}\n{'*'*100}")
                return captured_evm, output_power, 'Pass', self.filePathPc, crc_data[0]
        except Exception as e:
            Error = 'Capture_screenshot Error : {}'.format(e)
            print(Error)
            return Error
        
    def make_visa_connection_and_vxt_configuration(self):
        try:
            Visa_status = self.visa_connection(self.vxt_add)
            if not Visa_status:
                time.sleep(1)
                self.clear_status_reg_of_device()
                time.sleep(1)
                self.reset_device()
                time.sleep(2)
                if self.send_file_to_vxt(self.Local_path,self.state_file,self.remote_folder):
                    return 200
                time.sleep(2)
                print("send")
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
        
    def disconnect_from_VXT(self):
        try:
            self.device.close()
            self.rm.close()
            print("Disconnected from the VXT!")
        except Exception as e:
            Error = 'Capture_screenshot Error : {}'.format(e)
            print(Error)
            return 100
        
def Occupied_bandwidth(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.Occupied_band())
    else:
        status.append(config_status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status
     
def VXT_control(state_file,ScreenShot_file,bandwidth):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,bandwidth)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.verify_result_and_capture_screenshot())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    status.insert(5,str(vxt_obj.power_limit[0]))
    status.insert(6,str(vxt_obj.power_limit[1]))
    print(status)
    return status

def evm_control(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_EVM())
    print(status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    print(status)
    return status

def base_station_power(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_base_station_power())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.power_limit[0]))
    status.insert(4,str(vxt_obj.power_limit[1]))
    print(status)
    return status

def aclr_control(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_aclr())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(-2,'<-45')
    print(status)
    return status

def tpdr(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
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

def t_on_off_p(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
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

def freq_error(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
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


def O_B_U_E(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.OBUE())
    else:
        status.append(config_status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    print(status)
    return status

if __name__ == "__main__":
    print('='*100)
    # Occupied_bandwidth_Result = Occupied_bandwidth("tm_1_1_ob.state", "tm_1_1_ob.png")
    # # print(aclr_control("ACLR_TM_1_1.state", "ACLR_TM_1_1.png"))
    # # print(base_station_power("Power_TM_1_1.state", "Power_TM_1_1.png"))
    # t_on_off_p = t_on_off_p("tm1_1_t_on_off_p.state", "tm1_1_t_on_off_p.png")
    # # print(freq_error("TM_1_1.state", "TM_1_1_freq_error.png"))
    # report_path = '{}/CUPLANE/TestMac/Results/occupied_bandwidth_report.pdf'.format(root_dir)
    # genrate_report_ocuupied_bandwidth([Occupied_bandwidth_Result],report_path)
    # OBUE_result = O_B_U_E("TM_1_1_OBUE_Small.state", "TM_1_1_OBUE_Small.png")
    #power_result = tpdr("TM_3_1a.state", "TM_3_1a.png")
    #print(power_result)
    #print('='*100)
    status = VXT_control("dl_qpsk1_100_100_16_1_1_1.state","dl_qpsk1_100_100_16_1_1_1.png","100")
    print(status)
    report_path = f"/comon-space/QA_Testing/CUPLANE/Results/dl_qpsk1_100_100_16_1_1_1.pdf"
    Result = genrate_report_dl([status[:-1]],report_path,status[-1])
    if 'Pass' in status:
        print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Pass'.center(92)))
        sys.exit(0)
    else:
        if len(status)>6 and len(status)<12:
            print('{}'.format('Fail Reason :  Low Power or Evm'))
        else:
            print('{}'.format('Fail Reason :  Data from VXT not captured.'))
        print('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Fail'.center(92)))
