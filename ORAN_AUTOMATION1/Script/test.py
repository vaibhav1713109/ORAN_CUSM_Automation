import pyvisa
import time


def scpi_write(InstrObj, cmnd):

   InstrObj.write(cmnd)

   status = InstrObj.query('*OPC?')
   time.sleep(10)

   if int(status) != 1:

       return True

def Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Ext_Gain):

    rm = pyvisa.ResourceManager()
    visa = 'TCPIP::172.17.95.118::hislip0::INSTR'
    # visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHz"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD TDD", ":RAD:STAN:PRES:SCS SCS30K"])
    scpi_cmds.extend([':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":EVM:CCAR0:PDSC1:MCS 27", ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 27", ":EVM:CCAR0:PDSC3:MCS:TABL TABL2", ":EVM:CCAR0:PDSC3:MCS 27", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2", ":EVM:CCAR0:PDSC4:MCS 27"])
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    print(scpi_cmds)
    # return True
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)



def run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder):

    for scpi in scpi_cmds:
        #type(scpi)
        #print(scpi)
        scpi_write(InstrObj, scpi)
        time.sleep(3) 
    print("sleep start")
    time.sleep(5)
    filepath = r"C:\temp\capture.png"
    InstrObj.write(":MMEM:STOR:SCR '{}'".format(filepath))
    print("print taken")
    status = InstrObj.query('*OPC?')
    time.sleep(10)
    # image=r"C:\Users\Administrator\Documents\Keysight\Instrument\NR5G\screen\capture.png"
    filePathPc = sub_folder+"\VXT_capture.png"
    ResultData = bytes(InstrObj.query_binary_values(f'MMEM:DATA? "{filepath}"', datatype='s'))
    newFile = open(filePathPc, "wb")
    newFile.write(ResultData)
    newFile.close()
    InstrObj.close()
    print("Constellation Saved")


Constellation_check_DL_TDD_Comp_1('100',r'C:\ORAN_AUTOMATION1\Result', '3.54234', '-12')