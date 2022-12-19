#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : Generate_SCP.py                                                                     #
# @brief  : Creating SCP files for all Conformance testcases for both TDD and FDD.              #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @author : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)                   #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################


import sys
import clr
import os.path
import time

clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Keysight.SignalStudio.N7631.dll")
from Keysight.SignalStudio.N7631 import *
from Keysight.SignalStudio import *



def Create_SCP(sub_folder, api):    
    #Generating the scp file
    file_name = sub_folder+"\CTC_5GNR.scp"
    print(file_name)
    print("Generating the scp file")
    api.SaveSettingsFile(file_name)
    
def Generate_Download(status, VXT_Add, api):    
    if status:
        print("Generating the configurations")
        api.Generate()
        print("- Connected to the Instrument at " + str(VXT_Add) + ".")
        api.Download()
    else:
        print("- Connection failed")


def Numerology_SCS(scs_val):
    if scs_val == 15:
        return Numerology.SCS15k
    if scs_val == 30:
        return Numerology.SCS30k
    if scs_val == 60:
        return Numerology.SCS60k
    if scs_val == 120:
        return Numerology.SCS120k
    if scs_val == 240:
        return Numerology.SCS240k

def select_bandwidth(bands):
    if(bands == '40M'):
        return Bandwidth.FR1_40M
    elif(bands == '20M'):
        return Bandwidth.FR1_20M
    elif(bands == '100M'):
        return Bandwidth.FR1_100M
    pass

def phase_compMode(phase_comp):
    if phase_comp == 'Off':
        return PhaseCompensationMode.Off
    else:
        return PhaseCompensationMode.Auto
    
    
def Instrument_Setup(Center_Freq, Power_Value, VXT_Add, api):
    print("============================================================================================")
    print("================================SCP CREATION FUNCTION=======================================")
    print("============================================================================================")
    print("-Setting Up the Instrument configurations")
    #SignalGenerator.Frequency = 354234000000
    api.SignalGenerator.Frequency = (float(Center_Freq)*1000000000)
    print("freq: ",api.SignalGenerator.Frequency)
    api.SignalGenerator.Amplitude = int(Power_Value)
    print("amp: ",api.SignalGenerator.Amplitude)
    api.SignalGenerator.TriggerType = TriggerType.Continuous
    api.SignalGenerator.TriggerSource = TriggerSource.External
    api.SignalGenerator.ExternalPolarity = Polarity.Positive
    # api.SignalGenerator.ExternalDelayEnabled = True
    # api.SignalGenerator.ExternalDelayTime = 0.000000005
    api.SignalGenerator.Continuous = Continuous.TriggerAndRun
    # api.SignalGenerator.SingleTrigger = SingleTrigger.BufferedTrigger
    # api.SignalGenerator.SegmentAdvance = SegmentAdvance.Continuous
    #inst = "TCPIP::172.25.96.131::hislip1::INSTR"
    inst = VXT_Add
    b = api.ConnectInstrument(inst)
    #b = True
    #print(b)
    #print(type(b))
    return b
        
def Base_DL_FDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add, scs_val):
    api = Api()
    api.New()
    #api.NR5GWaveformSettings.RemoveNRCarrier(0)
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.DL)
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    
    Numerology_scs = Numerology_SCS(scs_val=scs_val)
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).SetDLTestModelPNType(DLTestModelPNType.PN9)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands=bands), DuplexType.FDD, Numerology_scs, TestModel.NR_FR1_TM1_1, 1, phase_compMode(phase_comp=phase_comp))        
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.FDD, Numerology_scs, TestModel.NR_FR1_TM1_1, 1, phase_compmode)        
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, phase_compmode)        
    #else:
    #    print(type(bands))        
    #    print(bands)        
    #    print("Not Excuted")        
    
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PatternBits = '0'
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PatternBits = '0'
    #print(api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).MCS)
    #print(api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).MCSTable)
    #a = input("waiting")
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
    
    
def Base_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands=bands), DuplexType.TDD, Numerology_SCS(scs_val=scs_val), TestModel.NR_FR1_TM1_1, 1, phase_compMode(phase_comp=phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_40M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_40M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_20M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
        #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_100M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).Enabled = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PatternBits = '0'
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PatternBits = '0'
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).PayloadData.PatternBits = '0'
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).PayloadData.PayLoadDataType = PayloadDataType.Pattern
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).PayloadData.PatternBits = '0'
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
def Extended_DL_FDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands=bands), DuplexType.FDD, Numerology_SCS(scs_val=scs_val), TestModel.NR_FR1_TM1_1, 1, phase_compMode(phase_comp=phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_40M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)        
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)        
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)        
    
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
    
def Extended_DL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands=bands), DuplexType.TDD, Numerology_SCS(scs_val=scs_val), TestModel.NR_FR1_TM1_1, 1, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_40M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_40M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_20M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
        #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_100M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).Enabled = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
def Base_UL_FDD(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting UL carrier 5G NR FRC required Configurations")
    
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.UL
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(select_bandwidth(bands=bands), FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_40M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_20M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_100M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()


def Base_UL_TDD(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting UL carrier 5G NR FRC required Configurations")
    
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.UL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(select_bandwidth(bands), FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, phase_compMode(phase_comp), tdd)
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_40M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off, tdd)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_40M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_20M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off, tdd)
    #     #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_20M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_100M, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Auto, tdd)
        #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_100M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN9
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()  
    
def Compression_FDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands), DuplexType.FDD, Numerology_SCS(scs_val), TestModel.NR_FR1_TM3_1a, 1, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_40M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)        
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)        
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)        
    
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).Enabled = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()


def Compression_FDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting UL carrier 5G NR FRC required Configurations")
    
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.UL
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(select_bandwidth(bands), FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_40M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_20M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_100M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()


def Compression_TDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add,scs_val):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(select_bandwidth(bands), DuplexType.TDD, Numerology_SCS(scs_val), TestModel.NR_FR1_TM3_1a, 1, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_40M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_20M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(Bandwidth.FR1_100M, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Auto)
    #Changing the required configurations after setting testmodel
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).ChannelCoding = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).AutoDCI = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDCIItem(0).Enabled = True
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(1).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(2).PayloadData.PayLoadDataType = PayloadDataType.PN23
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Downlink.GetDLSCHItem(3).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    print('The scp file is successfully generated')
    api.Close()

def Compression_TDD_UL(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting UL carrier 5G NR FRC required Configurations")
    
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.UL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(select_bandwidth(bands), FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, phase_compMode(phase_comp))
    # if(bands == '40M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_40M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '20M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_20M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    # elif(bands == '100M'):
    #     api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(Bandwidth.FR1_100M, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Auto)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()  