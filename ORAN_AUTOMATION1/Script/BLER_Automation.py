#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : BLER_Automation.py                                                                  #
# @brief  : Creating JSON file for BLER using Error Ratio Analyzer application.                 #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @Supervision : Gowtham Chandrasekaran, VVDN Technologies Pvt. Ltd (gowtham.c@vvdntech.in)     #
#################################################################################################



import os
import time
import json



def BLER_Script(sub_folder):
    #directory = input("Please enter the Directory path to Check Error Ratio Analyzer : ")
    pcap_path = []

    for root, dirs, files in os.walk(directory):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.scp'):
                # saves the whole path of files
                scp_path = os.path.join(root, file)
            if file.endswith('.pcap'):
                #find for captured recent pcap file
                pcap_path.append(os.path.join(root, file))
            if file.endswith('.xml'):
                # saves the whole path of files
                xml_path = os.path.join(root, file)
            if file.endswith('.orstx'):
                # saves the whole path of files
                orstx_path = os.path.join(root, file)


    init_time = os.path.getmtime(pcap_path[0])
    pcap_recent_path = pcap_path[0]
    for file in pcap_path:
        mod_time = os.path.getmtime(file)
        if(mod_time > init_time):
            pcap_recent_path = file
    

    cmd = "ErrorRatioAnalyzer.exe BLER "
    cmd1 = '%s"%s" "%s" "%s" "%s"'%(cmd,scp_path,xml_path,pcap_recent_path,orstx_path)
    #print(cmd1)
    #os.system("cd C:\Program Files\Keysight\Open RAN Studio")
    os.system(cmd1)
    #ErrorRatioAnalyzer.exe BLER "C:\Users\Administrator\Desktop\DBRU_B1_B3_RF\Sep_28\B1_5MHz_with_cavity\Channel_4_B1_-105dBm\5MHz_UL_11RB.scp" "C:\Users\Administrator\Desktop\DBRU_B1_B3_RF\Sep_28\B1_5MHz_with_cavity\Channel_4_B1_-105dBm\5MHz_UL_11RB.xml" "C:\Users\Administrator\Desktop\DBRU_B1_B3_RF\Sep_28\B1_5MHz_with_cavity\Channel_4_B1_-105dBm\captured 2022-09-28--14-36-22.pcap" "C:\Users\Administrator\Desktop\DBRU_B1_B3_RF\Sep_28\B1_5MHz_with_cavity\Channel_4_B1_-105dBm\5MHz_UL_11RB.orstx"
    # Opening JSON file

    for root, dirs, files in os.walk(directory):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.json'):
                # saves the whole path of files
                json_path = os.path.join(root, file)

    f = open(json_path)
  
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    file_name = sub_folder+"\BLER_Report.txt"
    # Iterating through the json
    # list
    file1 = open(file_name, "a")
    
    L1 = "BLER : "+data['BLER']+"\n"
    L2 = "Number_of_Total_Packets : "+data['Number_of_Total_Packets']+"\n"
    L3 = "Number_of_Error_Packets : "+data['Number_of_Error_Packets']+"\n"
    L4 = "Max_Number_of_Iterrations : "+data['Max_Number_of_Iterrations']+"\n"
    L5 = "Frames : "+"\n"
    file1.write(L1)
    file1.write(L2)
    file1.write(L3)
    file1.write(L4)
    file1.write(L5)
    count = 0
    for i in data['Frames']:
        count = count+1
    file1.write(count)
    file1.close()
  
    # Closing file
    f.close()
