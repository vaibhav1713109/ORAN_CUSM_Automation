#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#################################################################################################


import pyvisa
import time


def scpi_write(InstrObj, cmnd):

   InstrObj.write(cmnd)
   for _ in range(10):
        try:
            status = InstrObj.query("*OPC?")
            # print(type(status))
            if status == '1':
                print(status)
                break
        except Exception as e:
            print(e)

def Check_EVM(InstrObj):
    for _ in range(10):
        try:
            time.sleep(3)
            InstrObj.timeout = 5000
            CMD = ':FETCh:EVM000001?'
            Res = InstrObj.query_ascii_values(CMD)
            captured_evm = "{:.2f}".format(float(Res[1]))
            if float(captured_evm) < 5:
                return True
            else:
                return False
        except Exception as e:
            # INS.close()
            print('{} Check_EVM'.format(e))
    else:
        return 'Timeout expired before operation completed. Check_EVM'

def Check_Power(InstrObj):
    for _ in range(10):
        try:
            time.sleep(3)
            InstrObj.timeout = 5000
            CMD = ':FETC:CHP?'
            Res = InstrObj.query_ascii_values(CMD)
            output_power = "{:.2f}".format(float(Res[1]))
            if float(output_power) > 22 and float(output_power) < 25:
                return True
            else:
                return False
        except Exception as e:
            # INS.close()
            print('{} Check_Power'.format(e))
    
    else:
        return 'Timeout expired before operation completed. Check_Power'

def run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder):

    for scpi in scpi_cmds:
        scpi_write(InstrObj, scpi)
        time.sleep(1) 
    print("sleep start")
    time.sleep(5)
    Power = Check_Power(InstrObj)
    EVM = Check_Power(InstrObj)
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
    return Power, EVM


def Constellation_check_DL_FDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHZ"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD FDD", ":RAD:STAN:PRES:SCS SCS30K", ':RAD:STAN:PRES:RBAL DLTM1DOT1', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO OFF", ":EVM:CCAR0:PHAS:COMP:FREQ 0Hz", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS:TABL TABL1", ":EVM:CCAR0:PDSC1:MCS 0", ":EVM:CCAR0:PDSC2:MCS:TABL TABL1", ":EVM:CCAR0:PDSC2:MCS 0"])
    #a = ":EVM:CCAR0:PHAS:COMP:FREQ "+str(DL_Center_Freq)+"GHz"
    #scpi_cmds.append(a)
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    #a = ":SOUR:POW "+str(Power_Value)+" dBm"
    #scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)


def Constellation_check_DL_FDD_Comp(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHZ"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD FDD", ":RAD:STAN:PRES:SCS SCS30K", ':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO OFF", ":EVM:CCAR0:PHAS:COMP:FREQ 0Hz", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":DISP:EVM:WIND2:DATA DINF"])
    #a = ":EVM:CCAR0:PHAS:COMP:FREQ "+str(DL_Center_Freq)+"GHz"
    #scpi_cmds.append(a)
    #a = ":CORR:BTS:GAIN "+str(Power_Value)
    #scpi_cmds.append(a)
    #a = ":SOUR:POW "+str(Power_Value)+" dBm"
    #scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)

    
def Constellation_check_DL_TDD(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHZ"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    # scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD TDD", ":RAD:STAN:PRES:SCS SCS30K", ':RAD:STAN:PRES:RBAL DLTM1DOT1', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO OFF", ":EVM:CCAR0:PHAS:COMP:FREQ 0Hz", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS:TABL TABL1", ":EVM:CCAR0:PDSC1:MCS 0", ":EVM:CCAR0:PDSC2:MCS:TABL TABL1", ":EVM:CCAR0:PDSC2:MCS 0", ":EVM:CCAR0:PDSC3:MCS:TABL TABL1", ":EVM:CCAR0:PDSC3:MCS 0", ":EVM:CCAR0:PDSC4:MCS:TABL TABL1", ":EVM:CCAR0:PDSC4:MCS 0"])
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD TDD", ":RAD:STAN:PRES:SCS SCS30K", ':RAD:STAN:PRES:RBAL DLTM1DOT1', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO ON", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":DISP:EVM:WIND2:DATA DINF", ":EVM:CCAR0:PDSC1:MCS:TABL TABL1", ":EVM:CCAR0:PDSC1:MCS 0", ":EVM:CCAR0:PDSC2:MCS:TABL TABL1", ":EVM:CCAR0:PDSC2:MCS 0", ":EVM:CCAR0:PDSC3:MCS:TABL TABL1", ":EVM:CCAR0:PDSC3:MCS 0", ":EVM:CCAR0:PDSC4:MCS:TABL TABL1", ":EVM:CCAR0:PDSC4:MCS 0"])
    #a = ":EVM:CCAR0:PHAS:COMP:FREQ "+str(DL_Center_Freq)+"GHz"
    #scpi_cmds.append(a)
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    #a = ":SOUR:POW "+str(Power_Value)+" dBm"
    #scpi_cmds.append(a)
    # scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)
    
    
def Constellation_check_DL_TDD_Comp(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHZ"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD TDD", ":RAD:STAN:PRES:SCS SCS30K", ':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON", ":EVM:CCAR0:PHAS:COMP:AUTO OFF", ":EVM:CCAR0:PHAS:COMP:FREQ 0Hz", ":EVM:CCAR0:DEC:PDSC DESCrambled", ":DISP:EVM:WIND2:DATA DINF"])
    #a = ":EVM:CCAR0:PHAS:COMP:FREQ "+str(DL_Center_Freq)+"GHz"
    #scpi_cmds.append(a)
    #a = ":CORR:BTS:GAIN "+str(Power_Value)
    #scpi_cmds.append(a)
    #a = ":SOUR:POW "+str(Power_Value)+" dBm"
    #scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)    


def Constellation_check_DL_FDD_repeat(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = []
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)

def Constellation_check_DL_FDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":EVM:CCAR0:PDSC1:MCS 27", ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 27"]
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)


def Constellation_check_DL_TDD_repeat(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = []
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)

def Constellation_check_DL_TDD_Comp_1(bands, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, Ext_Gain):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":INST:SEL NR5G", ":INST:SEL NR5G", ":OUTP:STAT OFF", ":FEED:RF:PORT:INP RFIN", ':CONF:EVM', ":DISP:EVM:VIEW NORM"]
    a = ":CCAR:REF "+str(DL_Center_Freq)+"GHz"
    scpi_cmds.append(a)
    a = ":RAD:STAN:PRES:CARR B"+str(bands)
    scpi_cmds.append(a)
    scpi_cmds.extend([":RAD:STAN:PRES:FREQ:RANG FR1", ":RAD:STAN:PRES:DMOD TDD", ":RAD:STAN:PRES:SCS SCS30K"])
    scpi_cmds.extend([':RAD:STAN:PRES:RBAL DLTM3DOT1A', ":RAD:STAN:PRES:DLIN:BS:CAT ALAR", ":RAD:STAN:PRES:IMM", ":EVM:CCAR0:DC:PUNC ON",":EVM:CCAR0:PDSC1:MCS:TABL TABL2", ":EVM:CCAR0:PDSC1:MCS 27", ":EVM:CCAR0:PDSC2:MCS:TABL TABL2", ":EVM:CCAR0:PDSC2:MCS 27", ":EVM:CCAR0:PDSC3:MCS:TABL TABL2", ":EVM:CCAR0:PDSC3:MCS 27", ":EVM:CCAR0:PDSC4:MCS:TABL TABL2", ":EVM:CCAR0:PDSC4:MCS 27"])
    a = ":CORR:BTS:GAIN "+str(Ext_Gain)
    scpi_cmds.append(a)
    scpi_cmds.append(":MMEM:STOR:SCR 'lat.png'")
    run_scpi_cmnd(InstrObj, scpi_cmds, sub_folder)

def RF_OFF(VXT_Add):

    rm = pyvisa.ResourceManager()
    #visa = 'TCPIP::172.20.56.35::hislip0::INSTR'
    visa = VXT_Add
    InstrObj = rm.open_resource(visa)
    time.sleep(2)
    print (InstrObj)
    scpi_cmds = [":OUTP OFF"]
    for scpi in scpi_cmds:
        #type(scpi)
        #print(scpi)
        scpi_write(InstrObj, scpi)
