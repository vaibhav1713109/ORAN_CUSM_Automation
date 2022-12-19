import sys
import time
import pyvisa as visa
import os
from configparser import ConfigParser

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("parent_dir",parent_dir)
root_dir = os.path.dirname(os.path.dirname(parent_dir))
print(root_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))

class vxt_configuration_and_result_capture():
    def __init__(self,file_name,ScreenShot) -> None:
        self.vxt_add = configur.get('CUPlane','vxt_add')
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
                            f':CCAR:REF {self.center_frequency}GHz', ':SENS:POW:RANG:OPT IMM']
        #filePathPc1 = "/comon-space/QA_Testing/CUPLANE/Results/"
        filePathPc1 = "{}/Results/".format(parent_dir)
        self.filePathPc = os.path.normpath(filePathPc1+ScreenShot)
        self.crc_file_name = "{0}\\Meas.csv".format(self.remote_folder)

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
                    return 1303
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

    def reset_device(self):
        self.device.write('*RST')                                #Reset the device
        self.device.write('*WAI')                                #Wait till Reset command is complete

    def scpi_write(self, cmnd):
        Error = ''
        self.device.write(cmnd)
        #self.device.write('*WAI')
        for _ in range(10):
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

    def vxt_configuration(self,scpi_cmds):
        try:
            for scpi in scpi_cmds:
                self.scpi_write(scpi)
            return True
        except Exception as e:
            Error = f'vxt_configuration Error : {e}'
            print(Error)
            return Error

    def fetch_EVM_power(self):
        Error = ''
        captured_evm = 0
        output_power = 0
        time.sleep(2)
        try:
            CMD = ':FETCh:EVM000001?'
            Res = self.device.query_ascii_values(CMD)
            #time.sleep(1)
            print(Res)
            captured_evm = "{:.2f}".format(float(Res[1]))
            output_power = "{:.2f}".format(float(Res[0]))
        except Exception as e:
            Error = self.device.write("SYST:ERR?")
            #Error = 'fetch_EVM_power Error : {}'.format(e))
            print(Error)
            return "failed","failed",100
        if float(captured_evm) < float(self.evm_limit) and (float(output_power) > float(self.power_limit[0]) and float(output_power) < float(self.power_limit[1])):
            return captured_evm,output_power, True
        else:
            return captured_evm,output_power, False

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

    def fetch_EVM_tm2(self):
        Error = ''
        captured_evm = 0
        output_power = 0
        time.sleep(2)
        try:
            CMD = ':FETCh:EVM000001?'
            Res = self.device.query_ascii_values(CMD)
            #time.sleep(1)
            print(Res)
            captured_evm = "{:.2f}".format(float(Res[1]))
            output_power = "{:.2f}".format(float(Res[0]))
        except Exception as e:
            Error = self.device.write("SYST:ERR?")
            #Error = 'fetch_EVM_power Error : {}'.format(e))
            print(Error)
            return "failed","failed",100
        if float(captured_evm) < float(self.evm_limit):
            return captured_evm,output_power, True
        else:
            return captured_evm,output_power, False

    def verify_result_and_capture_screenshot_tm2(self):
        try:
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
            if power_evm_result[-1] != True:
                Error = f"{'*'*100}\nFail due to unexpected Power or EVM \nChannel Power : {power_evm_result[1]} \nEVM : {power_evm_result[0]}\n{'*'*100}"
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(Error)
                return captured_evm, output_power, 'Fail', self.filePathPc
            else:
                output_power = power_evm_result[1]
                captured_evm = power_evm_result[0]
                print(f"{'*'*100}\nChannel Power : {output_power}\nEVM : {captured_evm}\n{'*'*100}")
                return captured_evm, output_power, 'Pass', self.filePathPc
        except Exception as e:
            Error = 'Capture_screenshot Error : {}'.format(e)
            print(Error)
            return Error

    def Constellation_check(self):
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
                # self.common_cmds.extend(scpi_cmds)
                if self.vxt_configuration(self.basic_scpis):
                    time.sleep(13)
                    status = self.verify_result_and_capture_screenshot()
                    return status
                else:
                    print("VXT Configuration are Failed.") 
                    return 'VXT Configuration are Failed.'
            else:
                return Visa_status
        except Exception as e:
            Error = f'Constellation_check Error : {e}'
            print(Error)
            return Error
        
    def Constellation_check_tm_2(self):
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
                # self.common_cmds.extend(scpi_cmds)
                if self.vxt_configuration(self.basic_scpis):
                    time.sleep(13)
                    status = self.verify_result_and_capture_screenshot_tm2()
                    return status
                else:
                    print("VXT Configuration are Failed.") 
                    return 'VXT Configuration are Failed.'
            else:
                return Visa_status
        except Exception as e:
            Error = f'Constellation_check Error : {e}'
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

def VXT_control(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    status = list(vxt_obj.Constellation_check())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    status.insert(5,str(vxt_obj.power_limit[0]))
    status.insert(6,str(vxt_obj.power_limit[1]))
    print(status)
    return status

def TM_2_control(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    status = list(vxt_obj.Constellation_check_tm_2())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(3,str(vxt_obj.evm_limit))
    print(status)
    return status

def base_station_power(state_file,ScreenShot_file):
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    vxt_obj = vxt_configuration_and_result_capture(state_file,ScreenShot_file)
    status = list(vxt_obj.Constellation_check_tm_2())
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    status.insert(5,str(vxt_obj.power_limit[0]))
    status.insert(6,str(vxt_obj.power_limit[1]))
    print(status)
    return status

if __name__ == "__main__":
    print('='*100)
    print(TM_2_control("TM_2.state", "CU_TC3.png"))
    print('='*100)
