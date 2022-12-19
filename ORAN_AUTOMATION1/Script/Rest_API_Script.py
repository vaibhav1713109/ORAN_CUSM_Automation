#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : Rest_API_Script.py                                                                  #
# @brief  : Script for Creating Sync, load PCAP, play data, and recorder data Functions.        #
# @author : Razitha Roshin X, VVDN Technologies Pvt. Ltd (razitha.roshin@vvdntech.in)           #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)            #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################



import requests
import time


def sync_creation():
    url = "http://localhost:9000/Modules"
    print("============================================================================================")
    print("============================INSTRUMENT CONFIGURATION========================================")
    print("============================================================================================")
    #Get Module List
    payload = dict(id='0',model='S5040A',address='PXI0::2-0.0::INSTR')
    resp = requests.get(url,data=payload)
    print("Get Module List:"+ str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
    url = "http://localhost:9000/Modules/0/"
    #Configure Module
    instrumentconfig = r'C:\Users\Administrator\Documents\Keysight\Open RAN Studio\InstrumentConfig.xml'
    #instrumentconfig = "C:\\Demo\\InstrumentConfig.xml"
    files = {
        'data': (instrumentconfig, open(instrumentconfig, 'rb')),
    }
    resp = requests.post(url+"Configure",files = files)
    print("Load Configuration Status:" + str(resp.content)[1:] +"\t Response Code:" + str(resp.status_code))
    print("Instrument configured successfully")
    print("End.")
    print("============================================================================================")





def load_play_record_pcap(band_folder):
    print("============================================================================================")
    print("============================PLAYER AND RECORDER FUNCTION====================================")
    print("============================================================================================")

    url = "http://localhost:9000/Modules/0/"

    #url = "http://localhost:9000/Modules/1/"

    #Player Recorder Functions
    filename = band_folder+"\CTC_5GNR.pcap"
    files = {
    'data': (filename, open(filename, 'rb')),
    }
    payload = dict(state='on', radioframes='0')
    headers = {
    'Content-Type': 'application/json',
    }
    
    #load pcap
    resp = requests.post(url+"Player/pcap",files = files)
    print("Load Pcap Status:" + str(resp.content)[1:] +"\t Response Code:" + str(resp.status_code))
    
    #start Recorder
    data = '{"state":"on","radioframes":1}'
    resp = requests.put(url+"Recorder",data=data,headers = headers)
    print("Start Recorder Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
    
    #Get Recorder state
    resp = requests.get(url+"Recorder",data=payload)
    print("Recorder State:" + resp.text+"\t Response Code:" + str(resp.status_code))
    
    #start player
    data = '{"state":"on","radioframes":0}'
    resp = requests.put(url+"Player",data=data,headers = headers)
    print("Start Player Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
    
    
    #Getplayer state
    resp = requests.get(url+"Player",data=payload)
    print("Player State:" + resp.text+"\t Response Code:" + str(resp.status_code))
    
    time.sleep(3)
    
    #Get Recorder state
    resp = requests.get(url+"Recorder",data=payload)
    #time.sleep(15)
    print("Recorder State:" + resp.text+"\t Response Code:" + str(resp.status_code))
    
    #stop recorder
    data = '{"state":"off","radioframes":1}'
    resp = requests.put(url+"Recorder",data=data,headers = headers)
    print("Stop Recorder Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
    
    #getRecorder pcap
    file = open(filename[:-5] + "_captured.pcap", "wb")
    resp = requests.get(url+"Recorder/pcap")
    file.write(resp.content)
    file.close()
    print("Copied the Pcap")
    
    print("The Packets are Transmiting ....")
    
    print("============================================================================================")
    print("============================================================================================")
    
    
def Stop_Player():
    print("============================================================================================")
    print("============================PLAYER AND RECORDER FUNCTION====================================")
    print("============================================================================================")


    url = "http://localhost:9000/Modules/0/"

    #url = "http://localhost:9000/Modules/1/"


    payload = dict(state='on', radioframes='0')
    headers = {
    'Content-Type': 'application/json',
    }


    #Getplayer state
    resp = requests.get(url+"Player",data=payload)
    print("Player State:" + resp.text+"\t Response Code:" + str(resp.status_code))

    #stop player
    data = '{"state":"off","radioframes":1}'
    resp = requests.put(url+"Player",data=data,headers = headers)
    print("Stop Player Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))

    print("============================================================================================")
    print("============================================================================================")
    print("The Player stopped the transmission")



