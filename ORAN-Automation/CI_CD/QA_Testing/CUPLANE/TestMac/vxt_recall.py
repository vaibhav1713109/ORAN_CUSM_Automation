import pyvisa
import time,os
from configparser import ConfigParser

cwd = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cwd)
## For reading data from .ini file
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(cwd))

def make_visa_connection():
    try:
        rm = pyvisa.ResourceManager()
        visa = configur.get('CUPlane','vxt_add')
        print(visa)
        InstrObj = rm.open_resource(visa)
        time.sleep(2)
        print(InstrObj)
        InstrObj.timeout = 10000
        return InstrObj
    except Exception as e:
        error = f"make_visa_connection Error : {e}"
        print(e)
        return e

def clear_status_reg_of_device(InstrObj):
    InstrObj.write('*CLS')                                #Clear Status Register of device
    InstrObj.write('*WAI')                                #Wait till Clear command is complete

    #########################################################################################
    ## Reseting the VXT
    #########################################################################################
def reset_device(InstrObj):
    InstrObj.write('*RST')                                #Reset the device
    InstrObj.write('*WAI')

def scpi_write(InstrObj, cmnd):
   InstrObj.write(cmnd)
   status = InstrObj.query('*OPC?')
   while(1):
        print(f'{cmnd} {status}')
        if int(status) != 1:
            time.sleep(1)
            status = InstrObj.query('*OPC?')
        else:
            break
   time.sleep(1)
   return True


def recall_wfm_file(filename):
    center_frequency = configur.get('INFO','rx_center_frequency')
    amplitude = configur.get('CUPlane','amplitude')
    InstrObj = make_visa_connection()
    remote_folder = "C:\\Users\\Administrator\\Documents\\CU_Plane_Conf"
    if InstrObj:
        local_file = os.path.join(f"{root_dir}/Wfmfiles", filename)
        if not os.path.isfile(local_file):
            print(f"File not found: {local_file}")
            return f"File not found: {local_file}"

        with open(local_file, 'rb') as f:
            read_data = f.read()

        #remote_file = os.path.join(remote_path, file_name)
        rem_file = os.path.normpath(remote_folder+'\\'+filename)    
        print(rem_file)        
        reset_device(InstrObj)
        clear_status_reg_of_device(InstrObj)
        InstrObj.write(f':MMEMory:MDIRectory "{remote_folder}"')
        InstrObj.write_binary_values(f':MMEMory:DATA "{rem_file}",', read_data, datatype='B')
        status_complete = InstrObj.query("*OPC?")
        if int(status_complete) != 1:
            print("not completed",status_complete)
            error = f'send_file_to_VXT Error: Failed to transfer {local_file} to {rem_file}'
            return error
        else:
            print(f'File {local_file} successfully transferred to {rem_file}')
            # wfm_command = [f":SOUR:RAD:ARB:LOAD {filename}",":SOUR:RAD:ARB ON",":SOUR:RAD:ARB:TRIG:TYPE CONT",
            #                 ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG",":SOUR:RAD:ARB:TRIG EXT1", ":SOUR:RAD:ARB:TRIG:SYNC ON",
            #                 ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON",":SOUR:RAD:ARB:TRIG:EXT:DEL 0s",":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS",
            #                 f":SOUR:POW {amplitude} dBm",f":SOUR:FREQ {center_frequency} GHz",":OUTP ON"]
            wfm_command = [f':SOUR:RAD:ARB:LOAD "{rem_file}"',f":SOUR:RAD:ARB:WAV '{rem_file}'",
                            ":SOUR:RAD:ARB ON",":SOUR:RAD:ARB:TRIG:TYPE CONT",
                            ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG",":SOUR:RAD:ARB:TRIG EXT1", ":SOUR:RAD:ARB:TRIG:SYNC ON",
                            ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON",":SOUR:RAD:ARB:TRIG:EXT:DEL 0s",":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS",
                            f":SOUR:POW {amplitude} dBm",f":SOUR:FREQ {center_frequency} GHz",":OUTP ON"]
            for cmd in wfm_command:
                scpi_write(InstrObj,cmd)
            print("Waveform file recalled successfully")
            return True
    else:
        print('Error while creating visa connection.')
        return 'Error while creating visa connection.'


if __name__  == "__main__":
    recall_wfm_file("ul_qpsk1_100_100_16_1_1_1.wfm")

# rm = pyvisa.ResourceManager()
# visa = 'TCPIP0::172.25.96.182::hislip0::INSTR'
# InstrObj = rm.open_resource(visa)
# time.sleep(2)

# print(InstrObj)
# InstrObj.timeout = 10000
#InstrObj.write(":MMEM:LOAD:STAT 'Extended_DL_UL.state'")

# #Select a waveform segment or sequence to be played by the ARB player. ---> wfm file name
# scpi_write(InstrObj, ":SOUR:RAD:ARB:WAV 'C:\\Users\\Administrator\\Documents\\giri\\ul.wfm'")

# #Toggle the state of the ARB function ---> ON
# scpi_write(InstrObj, ":SOUR:RAD:ARB ON")

# #Setting for trigger type determines the behavior of the waveform when it plays ---> Continuous
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:TYPE CONT")

# #Sets the active trigger type to Continuous. If Continuous is already selected as the active trigger type, 
# #pressing this key allows access to the continuous trigger type setup menu. 
# #In Continuous trigger mode, the waveform repeats continuously ----> Trigger+Run
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:TYPE:CONT TRIG")

# #The trigger source setting determines how the source receives the trigger that starts the waveform playing ---> External1
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG EXT1")

# #Sync to Trigger Source ---> ON
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:SYNC ON")

# #External Trigger Delay ---> ON and Os
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:EXT:DEL:STAT ON")
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIG:EXT:DEL 0s")

# #External Trigger Polarity ---> Positive
# scpi_write(InstrObj, ":SOUR:RAD:ARB:TRIGger:EXT:SLOP POS")

# #RF Power in Amplitude Setup
# scpi_write(InstrObj, ":SOUR:POW -60 dBm")

# #Frequency in the Frequency Setup menu
# scpi_write(InstrObj, ":SOUR:FREQ 3.54234 GHz")

# #Sets the source RF power output state.
# scpi_write(InstrObj, ":OUTP ON")

# print("Waveform file recalled successfully")

