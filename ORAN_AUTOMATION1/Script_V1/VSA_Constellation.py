#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : VSA_Constellation.py                                                                #
# @brief  : Script for VSA operations.                                                          #
# @author : Umamaheswari E, VVDN Technologies Pvt. Ltd (e.umamaheswari@vvdntech.in)             #
# @Supervision : Sebu Mathew , VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)             #
# @Support Given : Hariharan R, VVDN Technologies Pvt. Ltd (hariharan.r@vvdntech.in)            #
# @Support Given : Muhammed Siyaf E K, VVDN Technologies Pvt. Ltd (muhammed.siyaf@vvdntech.in)  #
# @Support Given : Athulya Saju, VVDN Technologies Pvt. Ltd (athulya.saju@vvdntech.in)          #
#################################################################################################


import sys
import psutil
import os
import time
import clr
sys.path.append(r"C:\ORAN_AUTOMATION\Dependencies")

clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Agilent.SA.Vsa.Interfaces.dll")
#clr.AddReference(r"C:\ORAN_AUTOMATION\Dependencies\Agilent.SA.Vsa.DigitalDemod.Interfaces.dll")
clr.AddReference("System")
clr.AddReference("System.Linq")
clr.AddReference("System.Threading.Tasks")
from Agilent.SA.Vsa import*
#from Agilent.SA.Vsa.DigitalDemod import*

def VSA_Function(sub_folder):
    print("============================================================================================")
    print("=========================== 89600 VSA CONFIGURATION ========================================")
    print("============================================================================================")


    if ("Agilent.SA.Vsa.Vector-x64.exe" in (p.name() for p in psutil.process_iter())):
        print("89600 VSA Application is already running.")
    else:
        print("Starting 89600 VSA Application...")
        os.startfile("C:\Program Files\Keysight\89600 Software 2023\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        time.sleep(30)

    app = ApplicationFactory.Create()
    app.Preset()
    app.Measurements.SelectedItem.PresetTraces()
    app.Display.Traces.RemoveExtra()
    app.Measurements.SelectedItem.Restart()
    time.sleep(3)
    print("- Recall .setx file to VSA")
    file_name = sub_folder+"\CTC_5GNR.NR_Carrier_1-0_UL.setx"
    app.RecallSetup(file_name)
    app.Title = "UL_Constellation _Verification"
    time.sleep(3)
    print("- Recall Recording .ORB file to VSA")
    orb_filename = sub_folder+"\CTC_5GNR_recovered_iq.20_mu1_ant1.iqt.orb"
    app.Measurements.SelectedItem.Input.Recording.RecallFile(orb_filename, "ORB", RecordPaddingType.RepetitionPadding, 5.0)
    time.sleep(3)

    app.Display.Traces.SelectedIndex = 0
    app.Display.Traces.SelectedItem.DataName = "IQ Meas1"
    app.Display.Traces[3].IsVisible = bool(0)
    app.Display.Traces[3].DataName = "No Data"
    app.Display.Traces.SelectedItem.Markers.SelectedItem.Point = 1
    app.Display.Traces.SelectedIndex = 2
    app.Display.Traces.SelectedItem.DataName = "Slot Summary1"

    app.Measurements.SelectedItem.Restart()

    print("- Save an image of the main window in the png format.")
    time.sleep(5)
    save_filename = sub_folder+"\VSA_Screenshot_1"
    time.sleep(2)
    app.Display.Printer.SaveBitmap(save_filename, BitmapType.Png)
    app.Display.Traces.SelectedIndex = 2
    app.Display.Traces.SelectedItem.DataName = "Decoded Info1"
    time.sleep(2)
    save_filename = sub_folder+"\VSA_Screenshot_2"
    app.Display.Printer.SaveBitmap(save_filename, BitmapType.Png)
    
    print("- Exit the application")
    #app.Quit()
    
    print("End.")
    
def VSA_Function_PRACH(sub_folder, formats):
    print("============================================================================================")
    print("=========================== 89600 VSA CONFIGURATION ========================================")
    print("============================================================================================")


    if ("Agilent.SA.Vsa.Vector-x64.exe" in (p.name() for p in psutil.process_iter())):
        print("89600 VSA Application is already running.")
    else:
        print("Starting 89600 VSA Application...")
        os.startfile("C:\Program Files\Keysight\89600 Software 2023\89600 VSA Software\Agilent.SA.Vsa.Vector-x64.exe")
        time.sleep(30)

    app = ApplicationFactory.Create()
    app.Preset()
    app.Measurements.SelectedItem.PresetTraces()
    app.Display.Traces.RemoveExtra()
    app.Measurements.SelectedItem.Restart()
    time.sleep(3)
    print("- Recall .setx file to VSA")
    file_name = sub_folder+"\Format"+formats+"\CTC_5GNR.NR_Carrier_1-0_UL.setx"
    app.RecallSetup(file_name)
    app.Title = "UL_Constellation _Verification"
    time.sleep(3)
    print("- Recall Recording .ORB file to VSA")
    orb_filename = sub_folder+"\Format"+formats+"\CTC_5GNR_recovered_iq.20_mu1_ant1.iqt.orb"
    app.Measurements.SelectedItem.Input.Recording.RecallFile(orb_filename, "ORB", RecordPaddingType.RepetitionPadding, 5.0)
    time.sleep(3)

    app.Display.Traces.SelectedIndex = 0
    app.Display.Traces.SelectedItem.DataName = "IQ Meas1"
    app.Display.Traces[3].IsVisible = bool(0)
    app.Display.Traces[3].DataName = "No Data"
    app.Display.Traces.SelectedItem.Markers.SelectedItem.Point = 1
    app.Display.Traces.SelectedIndex = 2
    app.Display.Traces.SelectedItem.DataName = "Slot Summary1"

    app.Measurements.SelectedItem.Restart()

    print("- Save an image of the main window in the png format.")
    time.sleep(5)
    save_filename = sub_folder+"\Format"+formats+"\VSA_Screenshot_1"
    time.sleep(2)
    app.Display.Printer.SaveBitmap(save_filename, BitmapType.Png)
    app.Display.Traces.SelectedIndex = 2
    app.Display.Traces.SelectedItem.DataName = "Decoded Info1"
    time.sleep(2)
    save_filename = sub_folder+"\Format"+formats+"\VSA_Screenshot_2"
    app.Display.Printer.SaveBitmap(save_filename, BitmapType.Png)
    
    print("- Exit the application")
    #app.Quit()
    
    print("End.")
