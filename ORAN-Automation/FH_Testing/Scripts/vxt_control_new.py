import sys
import time
import pyvisa as visa
import os
from configparser import ConfigParser
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("vxt_control_new.py",root_dir)
# sys.path.append(root_dir)

class vxt_configuration_and_result_capture():
    def __init__(self,test_case_name,eAxID,ext_gain,config_file) -> None:
        self.test_case_name = test_case_name
        self.RU_Name = config_file['ru_name']
        self.img_version = config_file['img_version']
        self.ru_serial_no = config_file['ru_serial_no']
        self.duplex_type = config_file['duplex_type']
        self.scs_val = config_file['scs_value'][2:-3]
        self.vxt_add = config_file['vxt_address']
        self.eaxid = eAxID
        self.remote_folder = "C:/Users/Administrator/Documents"
        self.remote_file = f"{self.remote_folder}/{self.test_case_name}.NR_Carrier_1-0_DL.setx"
        self.bandwidth = config_file['bandwidth'][4:-1]
        testing_type = config_file['testing_type']
        if "16_QAM" in self.test_case_name:
            self.evm_limit = float(config_file['evm_limit'])+float(2)
        else:
            self.evm_limit = config_file['evm_limit']
        self.power_limit = config_file['power_limit'].split(',')
        self.clgc_gain_calculation_time = int(config_file['clgc_gain_calculation_time'])
        if 'TDD' in self.duplex_type:
            self.DL_Center_Freq = config_file['tx_center_frequency']
        else:
            self.DL_Center_Freq = config_file['tx_center_frequency']
        # self.Ext_Gain = float(config_file['external_gain'))*(-1]
        self.Ext_Gain = ext_gain
        self.crc_file_name = "Meas_{0}_eaxcid{1}.csv".format(test_case_name,self.eaxid)
        print(self.vxt_add,self.bandwidth,self.DL_Center_Freq,self.Ext_Gain)
        test_model = self.select_test_model(test_case_name)
        bs_catagory = self.select_bs_catagory()
        self.basic_scpis = [":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN",':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                            f':MMEM:LOAD:EVM:SET ALL, "{self.remote_file}"',":EVM:CCAR0:DEC:PDSC DESCrambled", ":EVM:CCAR0:DEC:PDCC DESCrambled",
                            ":DISP:EVM:WIND2:DATA DINF", ':CORR:BTS:GAIN {}'.format(self.Ext_Gain),
                            ':SENS:POW:RANG:OPT IMM']
        self.compression_scpi_16_qam = [
                    ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM",":INIT:CONT ON",
                    ":CCAR:REF {}GHZ".format(self.DL_Center_Freq),":RAD:STAN:PRES:CARR B{}M".format(self.bandwidth),
                    ":RAD:STAN:PRES:FREQ:RANG FR1", f":RAD:STAN:PRES:DMOD {self.duplex_type}", f":RAD:STAN:PRES:SCS SCS{self.scs_val}K",
                    ':RAD:STAN:PRES:RBAL DLTM3DOT2', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", 
                    ":EVM:CCAR0:DC:PUNC ON",":EVM:CCAR0:PDCC1:INCL ON", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":EVM:CCAR0:DEC:PDCC DESCrambled", ":EVM:CCAR0:DEC:PBCH DESCrambled", 
                    ":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS 10", 
                    ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 4", ":EVM:CCAR0:PDSC3:MCS:TABL TABL2", 
                    ":EVM:CCAR0:PDSC3:MCS 4", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2", ":EVM:CCAR0:PDSC4:MCS 10",
                    ":EVM:CCAR0:PDSC5:MCS:TABL TABL2", ":EVM:CCAR0:PDSC5:MCS 4", ":EVM:CCAR0:PDSC6:MCS:TABL TABL2", ":EVM:CCAR0:PDSC6:MCS 4",
                    ":CORR:BTS:GAIN {}".format(self.Ext_Gain)
                    ]
        self.filePathPc = f"{root_dir}/Results/{testing_type}/{self.RU_Name}/{self.img_version}/{self.ru_serial_no}/{config_file['bandwidth']}/EAXCID{self.eaxid}/{self.test_case_name}"
        print(self.filePathPc)

    def select_bs_catagory(self):
        bs_catagory = ['AWARea ', ' BWARea ', ' AMRange ', ' BMRange ', ' AMRLow ', ' BMRLow ', ' ALARea ', ' BLARea']
        if 'LPRU' in self.RU_Name:
            return "ALAR"
        else:
            return "BWAR"

    def select_test_model(self,test_case_name):
        test_models = [
                        'FQPSK ', ' FQAM16 ', ' FQAM64 ', ' FQAM256 ', ' FQAM1024 ', ' DLTM1DOT1 ',
                        ' DLTM1DOT2 ', ' DLTM2 ', ' DLTM2Q16 ', ' DLTM2QPS ', ' DLTM2A ', ' DLTM2B ',
                        ' DLTM3DOT1 ', ' DLTM3DOT1Q16 ', ' DLTM3DOT1QPS ', ' DLTM3DOT1A ', ' DLTM3DOT1B ',
                        ' DLTM3DOT2 ', ' DLTM3DOT3 ', ' FPIBPSK ', ' DLTM1DOT1P1 ', ' DLTM1DOT1L2'
                        ]
        if 'Comp' in self.test_case_name and '256' in self.test_case_name:
            return "DLTM3DOT1A"
        elif '64_QAM_Comp' in self.test_case_name:
            return "DLTM3DOT1"
        elif '16_QAM' in self.test_case_name:
            return "DLTM3DOT2"
        else:
            return "DLTM1DOT1"
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
        for _ in range(3):
            try:
                if not self.device:
                    print("Device not connected")
                    return "Device not connected"
                local_file = os.path.join(local_path, file_name)
                print(local_file)
                if not os.path.isfile(local_file):
                    print(f"File not found: {local_file}")
                    return f"File not found: {local_file}"

                with open(local_file, 'rb') as f:
                    read_data = f.read()

                #remote_file = os.path.join(remote_path, file_name)
                print(remote_path)
                rem_file = os.path.normpath(remote_path+'/'+file_name)
                ## Delete if file is already there...
                print(f'Deleting the file {rem_file}....')
                self.device.write(f'MMEM:DEL "{rem_file}"')
                self.device.write(f':MMEMory:MDIRectory "{remote_path}"')
                self.device.write_binary_values(f':MMEMory:DATA "{rem_file}",', read_data, datatype='B')
                status_complete = self.device.query("*OPC?")
                if int(status_complete) != 1:
                    print("not completed",status_complete)
                    error = f'send_file_to_VXT Error: Failed to transfer {local_file} to {rem_file}'
                    return error
                else:
                    print(f'File {local_file} successfully transferred to {rem_file}')
                    return True
                # include one more SCPI for file check here

            except Exception as e:
                error = f'send_file_to_VXT Error: {e}'
        else:
            print(error)
            return error

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
                time.sleep(0.1)
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
            newFile = open(f"{self.filePathPc}/capture.png", "wb")
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
        # self.scpi_write(":DISP:EVM:WIND2:DATA DINF")
        for _ in range(2):
            try:
                CMD = ':FETCh:EVM000001?'
                Res = self.device.query_ascii_values(CMD)
                #time.sleep(1)
                # print(Res)
                captured_evm = "{:.2f}".format(float(Res[1]))
                output_power = "{:.2f}".format(float(Res[22]))
                print('EVM = ',captured_evm)
                print('Active Power = ',output_power)
                time.sleep(5)
                self.capture_screenshot()
            except Exception as e:
                # Error = self.device.write("SYST:ERR?")
                Error = 'fetch_EVM_power Error : {}'.format(e)
                Error.split(' ',2)
                print(Error)
                return Error[0], Error[1], False
            # print(self.evm_limit,self.power_limit)
            if float(captured_evm) < float(self.evm_limit) and (float(output_power) > float(self.power_limit[0]) and float(output_power) < float(self.power_limit[1])):
                return captured_evm,output_power, True
            elif 'Base' in self.test_case_name:
                time.sleep(self.clgc_gain_calculation_time+45)
            else:
                time.sleep(self.clgc_gain_calculation_time)
        else:
            return captured_evm,output_power, False

    #########################################################################################
    ## Verify CRC value in DL
    #########################################################################################
    def verify_CRC(self):
        time.sleep(5)
        cmd = ':MMEM:STOR:RES "{}"'.format(self.crc_file_name)
        self.scpi_write(cmd)
        data_list = []
        Error = ''
        crc_pass = crc_fail = 0
        for _ in range(3):
            try:
                filepath = "C:\\Users\\Administrator\\Documents\\Keysight\\Instrument\\NR5G/data\\EVM/results\\{}_CC0Bits.csv".format(self.crc_file_name.split('.')[0])
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
            return [Error.rsplit(' ',4)],False

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
            captured_evm = "{:.2f}".format(float(Res[1]))
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'fetch_EVM Error : {}'.format(e)
            print(Error)
            print('Capture EVM :',captured_evm)
            print('Status : Fail')
            return Error, 'Fail', self.filePathPc
        if float(captured_evm) < float(self.evm_limit):
            print('Capture EVM :',captured_evm)
            print('Status : Pass')
            return captured_evm, 'Pass',self.filePathPc
        else:
            print('Capture EVM :',captured_evm)
            print('Status : Fail')
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
            print("="*100)
            print('Capture EVM :',Output_Power)
            print('Status : Fail')
            Error = 'fetch_base_station_power Error : {}'.format(e)
            print(Error)
            return Error, 'Fail', f"{self.filePathPc}/capture.png"
        if (float(Output_Power) > float(self.power_limit[0]) and float(Output_Power) < float(self.power_limit[1])):
            print("="*100)
            print('Capture EVM :',Output_Power)
            print('Status : Pass')
            return Output_Power, 'Pass',f"{self.filePathPc}/capture.png"
        else:
            print("="*100)
            print('Capture EVM :',Output_Power)
            print('Status : Fail')
            return Output_Power, 'Fail',f"{self.filePathPc}/capture.png"

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
            print('ACLR Values : ',aclr)
            print('Status : Fail')
            return *aclr,'Fail', f"{self.filePathPc}/capture.png"
        if float(aclr[0]) < -45 and float(aclr[1]) < -45:
            print('ACLR Values : ',aclr)
            print('Status : Pass')
            return *aclr,'Pass', f"{self.filePathPc}/capture.png"
        else:
            print('ACLR Values : ',aclr)
            print('Status : Fail')
            return *aclr,'Fail', f"{self.filePathPc}/capture.png"

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
            return Error, 'Fail', f"{self.filePathPc}/capture.png"
        if float(freq_error) < 300 and float(freq_error) > -300:
            return freq_error, 'Pass',f"{self.filePathPc}/capture.png"
        else:
            return freq_error, 'Fail',f"{self.filePathPc}/capture.png"

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
            return *result,'Fail', f"{self.filePathPc}/capture.png"
        if result:
            return *result,'Pass', f"{self.filePathPc}/capture.png"
        else:
            return *result,'Fail', f"{self.filePathPc}/capture.png"

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
            print(result)
            result1 = [str(result[0]-result[1]),str(result[2]-result[3]),str(result[4]-result[5]),str(result[6]-result[7]),str(result[8]-result[9])]
            print(result1)
            self.capture_screenshot()
        except Exception as e:
            # Error = self.device.write("SYST:ERR?")
            Error = 'OBUE Error : {}'.format(e)
            print(Error)
            return *result1,'Fail', f"{self.filePathPc}/capture.png"
        print(result[2]-result[3])
        if (result[0]-result[1]) <= -34.5 and (result[2]-result[3]) <= -35.2 and (result[4]-result[5]) <= -37 and (result[6]-result[7]) <= -37 and (result[8]-result[9]) <= -37:
            return *result1,'Pass', f"{self.filePathPc}/capture.png"
        else:
            return *result1,'Fail', f"{self.filePathPc}/capture.png"

    #########################################################################################
    ## Verifying the DL result for EVM, CRC, power and save the screenshot
    #########################################################################################
    def verify_result_and_capture_screenshot(self):
        try:
            power_evm_result = self.fetch_EVM_power()
            # print(power_evm_result)
            crc_data = self.verify_CRC()
            if power_evm_result[-1] != True or crc_data[-1] != True:
                Error = f"{'*'*100}\nFail due to unexpected Power or EVM \nChannel Power : {power_evm_result[1]} \nEVM : {power_evm_result[0]}\n{'*'*100}"
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(Error)
                return captured_evm, output_power, 'Fail', f"{self.filePathPc}/capture.png", crc_data[0]
            else:
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(f"{'*'*100}\nChannel Power : {output_power}\nEVM : {captured_evm}\n{'*'*100}")
                return captured_evm, output_power, 'Pass', f"{self.filePathPc}/capture.png", crc_data[0]
        except Exception as e:
            Error = f'verify_result_and_capture_screenshot Error : {type(e).__name__} {e}'
            print(Error)
            res = Error.rsplit(' ',3)
            res.append([])
            return res

    def make_visa_connection_and_vxt_configuration(self):
        try:
            Visa_status = self.visa_connection(self.vxt_add)
            if not Visa_status:
                time.sleep(1)
                self.clear_status_reg_of_device()
                time.sleep(1)
                self.reset_device()
                time.sleep(2)
                # print(self.filePathPc,f"{self.test_case_name}.scp",self.remote_folder)
                status = self.send_file_to_vxt(self.filePathPc,f"{self.test_case_name}.NR_Carrier_1-0_DL.setx",self.remote_folder)
                if status!= True:
                    return status
                time.sleep(2)
                print("send")
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

    def disconnect_from_VXT(self):
        try:
            self.device.close()
            self.rm.close()
            print("Disconnected from the VXT!")
        except Exception as e:
            Error = 'disconnect_from_VXT Error : {}'.format(e)
            print(Error)
            return 100

def Occupied_bandwidth(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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

def VXT_control(test_case_name,eaxcid,ext_gain,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    if float(ext_gain)>0:
        ext_gain = float(ext_gain)*(-1)
    vxt_obj = vxt_configuration_and_result_capture(test_case_name,eaxcid,ext_gain,config_file)
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

def evm_control(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_EVM())
    else:
        status.append(config_status)
    print(status)
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    print(status)
    return status

def base_station_power(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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

def aclr_control(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
    config_status = vxt_obj.make_visa_connection_and_vxt_configuration()
    status = []
    if config_status == True:
        status = list(vxt_obj.fetch_aclr())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(-2,'<-45')
    print(status)
    return status

def tpdr(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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

def t_on_off_p(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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

def freq_error(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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

def O_B_U_E(state_file,ScreenShot_file,config_file):
    center_freq = config_file['tx_center_frequency']
    bandwidth = config_file['bandwidth']
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file,config_file)
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
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    start_time = time.time()
    print('='*100)
    if len(sys.argv) > 2:
        test_case_name = sys.argv[1]
        ext_gain = sys.argv[3]
        RU_Name = information['ru_name']
        img_version = information['img_version']
        ru_serial_no = information['ru_serial_no']
        # state_file = sys.argv[2]
        eaxcid = sys.argv[2]
        VXT_control(test_case_name,eaxcid,ext_gain,information)
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