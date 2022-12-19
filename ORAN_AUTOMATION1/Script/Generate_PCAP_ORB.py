#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : Generate_PCAP_ORB.py                                                                #
# @brief  : Creating PCAP and ORB files for all Conformance testcases for both TDD and FDD also corresponding with compression cases. #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)            #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################


import sys
import clr
sys.path.append("C:\Windows\Microsoft.NET\Framework\\v4.0.30319")
sys.path.append(r"C:\ORAN_AUTOMATION\Dependencies")

clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Open RAN Studio API.dll")
clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\xRAN Configuration.dll")
clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\xRAN Transport.dll")
clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Errors Logging Tracing.dll")
clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Agilent.SA.Vsa.Interfaces.dll")
# clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\KalApi.dll")
clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\System.Runtime.InteropServices.RuntimeInformation.dll")
clr.AddReference("System")
clr.AddReference("System.Linq")
clr.AddReference("System.Threading.Tasks")
from Keysight.OpenRanStudio import*
from ErrorsLoggingTracing.Exceptions import*
from Agilent.SA.Vsa import*


def Generate_ORB(sub_folder, eAxID):
    print("============================================================================================")
    print("============================Generate ORB from captured PCAP=================================")
    print("============================================================================================")
    
    
    #Api.ApplicationDirectory = "C:\Program Files\Keysight\Open RAN Studio"
    #Instantiation creates all resources necessary to subsequent API usage
    myApi = Api()
    
    pcap_filename = sub_folder+"\CTC_5GNR_captured.pcap"
    orstx_filename = sub_folder+"\CTC_5GNR.orstx"
    
    print("- Import PCAP in Explorer")
    myProject = myApi.Explorer(pcap_filename,orstx_filename)
    
    print("- Inspecting eAxID value of the packets")
    index = myProject.GetEaxcId(0)
    print("eAxID: ", index)
    
    print("- Filter Uplink Packets")
    # myProject.FilterPackets(OrsConfiguration.NumerologyType.Mu1, OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
    myProject.FilterPackets(OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
    
    save_file = sub_folder+"\CTC_5GNR_recovered_iq"
    print("- Extract Uplink U plane IQ Data")
    myProject.RecoverIQTD(index, OrsConfiguration.DataDirection.UL, save_file)
    #myApi.close()
    print("ORB_Created")

def DL(bands, eAxID, sub_folder, bit_width):
    print("============================================================================================")
    print("============================ORS CONFIGURATION===============================================")
    print("============================================================================================")
    #Instantiation creates all resources necessary to subsequent API usage
    myApi = Api()
    print("- Import Waveform Project (.scp)")
    #The method opens a project file (Signal Studio uses file extension ".scp") previously saved from Keysight Signal Studio. 
    file_name = sub_folder+"\CTC_5GNR.scp"
    myProject = myApi.ImportWaveformProject(file_name)
    
    print("- Set ORS Configuration")
    myConfig = OrsConfiguration(myProject)
    eAxID = int(eAxID, 16)
    myConfig.Flow_TableSize(OrsConfiguration.DataDirection.DL, 1) #Set the flow/eAxC index table size -- Flow_TableSize(DataDirection  dir, int  size ) 
    if (bit_width == 16):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.NONE, 16) # Add an entry to the flow/eAxC index table
    elif (bit_width == 9):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 9) # Add an entry to the flow/eAxC index table
    elif (bit_width == 12):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 12) # Add an entry to the flow/eAxC index table
    elif (bit_width == 14):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 14) # Add an entry to the flow/eAxC index table
    #( DataDirection  dir, int  flowIdx, int  eaxcId,  int  duIdBitAlloc,  int  bsIdBitAlloc,  int  ccIdBitAlloc,  int  ruIdBitAlloc,  UPlaneCmpType  cmpType,  UPlaneCmpMethod  cmpMethod,  int  cmpBitwidth,  CUPlaneCoupMethod  coupMethod = CUPlaneCoupMethod.NORMAL )
    myConfig.Numerology_SlotIdNumberingScheme(2, muFR1 = 1, muFR2 = 4) # Set slot ID numbering scheme
    if (bands == '40M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_40M) # Set bandwidth for IQ recovery
    elif (bands == '20M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_20M) # Set bandwidth for IQ recovery
    elif (bands == '100M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_100M) # Set bandwidth for IQ recovery
    myConfig.Numerology_RecoverIqFlowMu(OrsConfiguration.NumerologyType.Mu1) # Set numerology for IQ recovery
    myConfig.Networking_Mtu(1400) # Set the MTU, which impacts how stimulus packets are fragmented (on O-RAN application layer). 
    myConfig.Options_VlanId(100) # Sets VLAN ID
    myConfig.Beam_Method(OrsConfiguration.BfMethod.DISABLED)
    # myConfig.Timing_TcpAdvDl(425000)
    myConfig.Timing_TCpDl(425000)
    myConfig.Timing_TUpDl(250000)
    myConfig.Timing_TcpAdvDl(175000) 
    myConfig.Options_UseDpsFsFixed256QamScaler(True) #Force the full-scale scaler to perform digital power scaling relative to 256QAM disregarding carrier modulation
    #myConfig.FlowIdxMap_AddCarrierMapEntry(0, 1) #Add mapping from a carrier (index) to a flow/eAxC ID. This variant is for simple waveforms (no MIMO). --AddCarrierMapEntry  ( int  carrierIdx,  int  flowId,  RAT_T  rat = RAT_T.NR)  
    myConfig.FlowIdxMap_AddCarrierMapEntry(0, eAxID)
    Generate_PCAP(myApi, myConfig)
   
    

    
def UL(bands, eAxID, sub_folder, bit_width):
    print("============================================================================================")
    print("============================ORS CONFIGURATION===============================================")
    print("============================================================================================")
    #Instantiation creates all resources necessary to subsequent API usage
    myApi = Api()
    print("- Import Waveform Project (.scp)")
    #The method opens a project file (Signal Studio uses file extension ".scp") previously saved from Keysight Signal Studio. 
    file_name = sub_folder+"\CTC_5GNR.scp"
    myProject = myApi.ImportWaveformProject(file_name)
    
    print("- Set ORS Configuration")
    myConfig = OrsConfiguration(myProject)
    eAxID = int(eAxID, 16)
    myConfig.Flow_TableSize(OrsConfiguration.DataDirection.UL, 1)
    if (bit_width == 16):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.NONE, 16)
    elif (bit_width == 9):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 9)
    elif (bit_width == 12):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 12)
    elif (bit_width == 14):
        myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.BLOCK_FLOATING_POINT, 14)
    myConfig.Numerology_SlotIdNumberingScheme(2, muFR1 = 1, muFR2 = 4) # Set slot ID numbering scheme
    if (bands == '40M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_40M) # Set bandwidth for IQ recovery
    elif (bands == '20M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_20M) # Set bandwidth for IQ recovery
    elif (bands == '100M'):
        myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.FR1_100M) # Set bandwidth for IQ recovery
    myConfig.Numerology_RecoverIqFlowMu(OrsConfiguration.NumerologyType.Mu1) # Set numerology for IQ recovery
    myConfig.Networking_Mtu(1400) # Set the MTU, which impacts how stimulus packets are fragmented (on O-RAN application layer). 
    myConfig.Options_VlanId(100) # Sets VLAN ID
    myConfig.Beam_Method(OrsConfiguration.BfMethod.DISABLED)
    #myconfig.Timing_TcpAdvDl(425000)
    #myConfig.Timing_TCpDl(425000)
    #myConfig.Timing_TUpDl(300000)
    #myConfig.Timing_TcpAdvDl(0) 
    myConfig.Options_UseDpsFsFixed256QamScaler(True) #Force the full-scale scaler to perform digital power scaling relative to 256QAM disregarding carrier modulation
    myConfig.FlowIdxMap_AddCarrierMapEntry(0, eAxID)
    Generate_PCAP(myApi, myConfig)
    #myApi.GenerateBlerXmlFile()
    
    

def Generate_PCAP(myApi, myConfig):
    #Generates the stimulus PCAP file, which can be used by the Open RAN Studio Player. Automatically saves a ".setx" file for each carrier in case the Keysight VSA tool is applied later in the workflow, e.g., after using the Explorer recover IQ functionality
    print("- Export Configuration file")
    myApi.ExportStimulus(myConfig)
    #myApi.GenerateBlerXmlFile()
    print("Generated .pcap")
