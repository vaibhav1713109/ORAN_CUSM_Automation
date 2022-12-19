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

clr.AddReference(r"C:\ORAN_AUTOMATION1\Dependencies\Keysight.SignalStudio.N7631.dll")
from Keysight.SignalStudio.N7631 import *
from Keysight.SignalStudio import *

def band(bands):    
    if(bands == "5M"):
        return 0
    if(bands == "10M"):
        return 1
    if(bands == "15M"):
        return 2
    if(bands == "20M"):
        return 3
    if(bands == "25M"):
        return 4
    if(bands == "30M"):
        return 5
    if(bands == "40M"):
        return 6
    if(bands == "50M"):
        return 7
    if(bands == "60M"):
        return 8
    if(bands == "70M"):
        return 9
    if(bands == "80M"):
        return 10
    if(bands == "90M"):
        return 11
    if(bands == "100M"):
        return 12
        

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
    api.SignalGenerator.ExternalDelayEnabled = True
    api.SignalGenerator.ExternalDelayTime = 5
    api.SignalGenerator.Continuous = Continuous.TriggerAndRun
    api.SignalGenerator.SingleTrigger = SingleTrigger.BufferedTrigger
    api.SignalGenerator.SegmentAdvance = SegmentAdvance.Continuous
    #inst = "TCPIP::172.25.96.131::hislip1::INSTR"
    inst = VXT_Add
    b = api.ConnectInstrument(inst)
    #b = True
    #print(b)
    #print(type(b))
    return b
    
    
def Base_DL_FDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    #api.NR5GWaveformSettings.RemoveNRCarrier(0)
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.DL)
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    #api.NR5GWaveformSettings.GetNRCarriersItem(0).SetDLTestModelPNType(DLTestModelPNType.PN9)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)        
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
    
    
    
    
def Extended_DL_FDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)        
    
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
    
    
    
def Base_UL_FDD(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting UL carrier 5G NR FRC required Configurations")
    
    #api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.UL
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(ret_band, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()


 
def Compression_FDD_DL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.FDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)        
    
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
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).ULFRCConfig(ret_band, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()


def Base_DL_UL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
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
    print("-Setting UL carrier 5G NR FRC required Configurations")
    api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).CarrierType = CarrierType.UL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).ULFRCConfig(ret_band, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off, tdd)
        #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_100M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
def Extended_DL_UL_TDD(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM1_1, 1, PhaseCompensationMode.Off)
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
    print("-Setting UL carrier 5G NR FRC required Configurations")
    api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).CarrierType = CarrierType.UL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).ULFRCConfig(ret_band, FRC.G_FR1_A1_5, 0, PUSCHMappingType.A, PhaseCompensationMode.Off, tdd)
        #api.NR5GWaveformSettings.GetNRCarriersItem(0).FullfilledConfig(Bandwidth.FR1_100M, Numerology.SCS30k, ModulationType.QPSK, tdd)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()
    
    
def Compression_TDD_DL_UL(bands, phase_comp, sub_folder, DL_Center_Freq, Power_Value, VXT_Add):
    api = Api()
    api.New()
    status = Instrument_Setup(DL_Center_Freq, Power_Value, VXT_Add, api)
    print("-Setting DL carrier 5G NR Testmodel required Configurations")
    api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.DL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(0).PresetDLTestModel(ret_band, DuplexType.TDD, Numerology.SCS30k, TestModel.NR_FR1_TM3_1a, 1, PhaseCompensationMode.Off)
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
    print("-Setting UL carrier 5G NR FRC required Configurations")
    api.NR5GWaveformSettings.AddNRCarrier(CarrierType.UL)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).CarrierType = CarrierType.UL
    tdd = TDDConfig(SlotConfigurationPeriod.MS5, 7, 6, 2, 4)
    ret_band = Bandwidth.Value = band(bands)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).ULFRCConfig(ret_band, FRC.G_FR1_A5_13, 0, PUSCHMappingType.A, PhaseCompensationMode.Off, tdd)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).NumberOfDMRSCDMGroup = 1 #(default value 1)
    api.NR5GWaveformSettings.GetNRCarriersItem(1).Uplink.GetULSCHItem(0).PayloadData.PayLoadDataType = PayloadDataType.PN23
    Create_SCP(sub_folder, api)
    Generate_Download(status, VXT_Add, api)
    print('The scp file is successfully generated')
    api.Close()

    
def NR_PRACH_A3(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
        api = Api()
        api.New()
        status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
        print("-Setting UL carrier 5G NR FRC required Configurations")
        api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.PRACH
        if (bands == '100M'):
            api.NR5GWaveformSettings.GetNRCarriersItem(0).PrachTestPreamblesConfig(Bandwidth.FR1_100M, Numerology.SCS30k, PRACHFormat.FormatA3, PRACHSubcarrierSpacing.SCS30k, False)
        elif (bands == '40M'):
            api.NR5GWaveformSettings.GetNRCarriersItem(0).PrachTestPreamblesConfig(Bandwidth.FR1_40M, Numerology.SCS30k, PRACHFormat.FormatA3, PRACHSubcarrierSpacing.SCS30k, False)
        elif (bands == '20M'):
            api.NR5GWaveformSettings.GetNRCarriersItem(0).PrachTestPreamblesConfig(Bandwidth.FR1_20M, Numerology.SCS30k, PRACHFormat.FormatA3, PRACHSubcarrierSpacing.SCS30k, False)
         
        api.NR5GWaveformSettings.NumberOfFrames = int(1)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationTable = PRACHConfigurationTable.FR1_UnpairedSpectrum
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationIndex = int(127)

        for i in range (0,77):
            a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(1))
            
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(2).SlotIndex = int(9)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(3).SlotIndex = int(9)

        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(1).n_RA_t = int(1)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(3).n_RA_t = int(1)
        Create_SCP(sub_folder, api)
        Generate_Download(status, VXT_Add, api)
        print('The scp file is successfully generated')
        api.Close()
        
 
 
def NR_PRACH_B4(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
        api = Api()
        api.New()
        status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
        print("-Setting UL carrier 5G NR FRC required Configurations")
        api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.PRACH
        ret_band = Bandwidth.Value = band(bands)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).PrachTestPreamblesConfig(ret_band, Numerology.SCS30k, PRACHFormat.FormatB4, PRACHSubcarrierSpacing.SCS30k, False)
         
        api.NR5GWaveformSettings.NumberOfFrames = int(1)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationTable = PRACHConfigurationTable.FR1_UnpairedSpectrum
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationIndex = int(167)
        
        for i in range (0,59):
            a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))
        i=0
        for j in range(0,20,2):
                api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(j).SlotIndex = int(i)
                api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(j+1).SlotIndex = int(i)
                i+=1
        for k in range(1,21,2):        
            api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(k).n_RA_slot = int(1)

        Create_SCP(sub_folder, api)
        Generate_Download(status, VXT_Add, api)
        print('The scp file is successfully generated')
        api.Close()
        
        
# def NR_PRACH_C2(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
def NR_PRACH_C2( bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add):
        api = Api()
        api.New()
        status = Instrument_Setup(UL_Center_Freq, Power_Value, VXT_Add, api)
        print("-Setting UL carrier 5G NR FRC required Configurations")
        api.NR5GWaveformSettings.GetNRCarriersItem(0).CarrierType = CarrierType.PRACH
        ret_band = Bandwidth.Value = band(bands)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).PrachTestPreamblesConfig(ret_band, Numerology.SCS30k, PRACHFormat.FormatC2, PRACHSubcarrierSpacing.SCS30k, False)
         
        api.NR5GWaveformSettings.NumberOfFrames = int(1)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationTable = PRACHConfigurationTable.FR1_UnpairedSpectrum
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.ConfigurationIndex = int(205)
        
        for i in range (0,77):
            a = api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.RemoveBurst(int(0))
        i=0
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(2).SlotIndex = int(9)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(3).SlotIndex = int(9)

        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(1).n_RA_t = int(1)
        api.NR5GWaveformSettings.GetNRCarriersItem(0).Prach.GetBurstsItem(3).n_RA_t = int(1)

        Create_SCP(sub_folder, api)
        Generate_Download(status, VXT_Add, api)
        print('The scp file is successfully generated')  
        api.Close()
        
        
def ST3_TDD(bands, phase_comp, sub_folder, UL_Center_Freq, Power_Value, VXT_Add, formats):
    if (formats == "A3"):
    	sub_folder = sub_folder+"\FormatA3"
        if not os.path.exists(sub_folder):
        	os.mkdir(sub_folder)
    	# NR_PRACH_A3(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
        NR_PRACH_A3(bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    if (formats == "B4"):
    	sub_folder = sub_folder+"\FormatB4"
    	if not os.path.exists(sub_folder):
        	os.mkdir(sub_folder)
    	# NR_PRACH_B4(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
        NR_PRACH_B4(bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
    if (formats == "C2"):
    	sub_folder = sub_folder+"\FormatC2"
    	if not os.path.exists(sub_folder):
        	os.mkdir(sub_folder)
    	# NR_PRACH_C2(api, bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)
        NR_PRACH_C2(bands, sub_folder, UL_Center_Freq, Power_Value, VXT_Add)



