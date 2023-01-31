#################################################################################################
#-----------------------------------------------------------------------------------------------#
#              VVDN CONFIDENTIAL                                                                #
#-----------------------------------------------------------------------------------------------#
# Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd.                                          #
# All rights reserved                                                                           #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
# @file   : CU_PlaneGUI_S.py                                                                    #
# @brief  : GUI part for CU plane Automation.                                                   #
# @author : Sebu Mathew, VVDN Technologies Pvt. Ltd (sebu.mathew@vvdntech.in)                   #
#                                                                                               #
#################################################################################################

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class HomeApp(ttk.Frame):
    """ This application Provides the Common configuarion Parametrs....... """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.ConfFB()        
        
    def createWidgets(self):
        global is_SavePressedHme
        global Test_Conf
        is_SavePressedHme = 0
        self.Buttons_dict={}
        #Radio Buttons
        Optns_TstTyps = (("Conformance","Conformance"),("Functional","Functional"),("RCT","RCT"),("Basic","Basic"))
        self.TestType="TT"
        LabelTT="Suit Type : "
        self.Radio_ButtonsH(Optns_TstTyps,self.TestType,LabelTT,"Conformance",3,2,"pass")
        
        Optns_FrqBnds = (("FR1","FR1"),("FR2","FR2"))
        self.FreqBand="FB"
        LabelFB="Frequency Bands : "
        self.Radio_ButtonsH(Optns_FrqBnds,self.FreqBand,LabelFB,"FR1",5,2,self.ConfFB)
        
        Optns_CPTyps = (("Normal","Normal"),("Extended","Extended"))
        self.CyclcPrfx="CP"
        LabelCP="Cyclic Prefix : "
        self.Radio_ButtonsH(Optns_CPTyps,self.CyclcPrfx,LabelCP,"Normal",7,2,self.Conf_SCS)
        
        Optns_SCSTyps = (("15KHz","15"),("30KHz","30"),("60KHz","60"),("120KHz","120"))
        self.SubCarSpcng="SCS"
        LabelSCS="SCS : "
        self.Radio_ButtonsH(Optns_SCSTyps,self.SubCarSpcng,LabelSCS,"30",9,2,"pass")
        
        Optns_DUPTyps = (("TDD","TDD"),("FDD","FDD"))
        self.DuplexTyps="DUPLX"
        LabelDT="Duplex_Type : "
        self.Radio_ButtonsH(Optns_DUPTyps,self.DuplexTyps,LabelDT,"TDD",11,2,self.Conf_UL_DL_Centr_Freq)
        
        self.UL_CntrFreq = StringVar()
        self.DL_CntrFreq = StringVar()
        self.Cntrfreq_Lbl = ttk.Label(self,text="Centre Freq in GHz(UL/DL) :").grid(row=13,column=2,padx=5,pady=15,sticky="W")
        self.UL_CntrFreq_entry = ttk.Entry(self, textvariable=self.UL_CntrFreq)
        self.UL_CntrFreq_entry.grid(row=13,column=3,padx=6,pady=10,sticky="W")
        
        self.Power_dBm = StringVar()
        self.Power_dBm_Lbl = ttk.Label(self,text="Power in dBm :").grid(row=15,column=2,padx=5,pady=15,sticky="W")
        self.Power_dBm_entry = ttk.Entry(self, textvariable=self.Power_dBm)
        self.Power_dBm_entry.grid(row=15,column=4,padx=6,pady=10,sticky="W")
        
        self.TimingParams = StringVar()
        self.TimingParams_Lbl = ttk.Label(self,text="Timing Params :").grid(row=16,column=2,padx=5,pady=15,sticky="W")
        self.TimingParams_entry = ttk.Entry(self, textvariable=self.TimingParams,width=40)
        self.TimingParams_entry.grid(row=16,column=3,columnspan=2,padx=6,pady=10,sticky="W")
        
        self.PathResults = StringVar()
        self.PathResults_Lbl = ttk.Label(self,text="Result's Path :").grid(row=17,column=2,padx=5,pady=15,sticky="W")
        self.PathResults_entry = ttk.Entry(self, textvariable=self.PathResults,width=40)
        self.PathResults_entry.grid(row=17,column=3,columnspan=2,padx=6,pady=10,sticky="W")
        
        self.VXTAddrs = StringVar()
        self.VXTAddrs_Lbl = ttk.Label(self,text="VXT Address :").grid(row=19,column=2,padx=5,pady=15,sticky="W")
        self.VXTAddrs_entry = ttk.Entry(self, textvariable=self.VXTAddrs,width=40)
        self.VXTAddrs_entry.grid(row=19,column=3,columnspan=2,padx=6,pady=10,sticky="W")
        
        self.SaveBtn = ttk.Button(self, text="Save", command=self.saveButton)
        self.SaveBtn.grid(row=23,column=3,padx=6,pady=10,sticky="E")
        
    def saveButton(self):
        global is_SavePressedHme
        readStatus = self.ReadHomeAppConfigs()
        if not readStatus:
            messagebox.showinfo("information", "Config Cant be saved correct and save again")
            return False
        else:
            self.clear_frame()
            self.DisplaySelectedHomeConfigs()
            self.EditBtn = ttk.Button(self, text="Edit", command=self.editButton)
            self.EditBtn.grid(row=23,column=3,padx=0,pady=10,sticky="W")
            is_SavePressedHme = 1
            Test_Conf.createWidgets()
            Test_Func.createWidgets()
            Test_RCT.createWidgets()
            Test_Basic.createWidgets()
            return True        
        
    def editButton(self):
        global is_SavePressedHme
        self.clear_frame()
        self.createWidgets()
        self.ConfFB()
        Test_Conf.createWidgets()
        Test_Func.createWidgets()
        Test_RCT.createWidgets()
        Test_Basic.createWidgets()
        is_SavePressedHme = 0        
        
    def ReadHomeAppConfigs(self):
        global HomeAppConfigs
        HomeAppConfigs = {}
        HomeAppConfigs["TT"]=self.Buttons_dict["Var_"+self.TestType].get()
        HomeAppConfigs["FB"]=self.Buttons_dict["Var_"+self.FreqBand].get()
        HomeAppConfigs["CP"]=self.Buttons_dict["Var_"+self.CyclcPrfx].get()
        HomeAppConfigs["SCS"]=self.Buttons_dict["Var_"+self.SubCarSpcng].get()
        HomeAppConfigs["DUPLX"]=self.Buttons_dict["Var_"+self.DuplexTyps].get()
        if HomeAppConfigs["DUPLX"] == "FDD":
            HomeAppConfigs["UL_Freq"]=self.UL_CntrFreq.get()
            try:
                integer_result = float(HomeAppConfigs["UL_Freq"])                
            except ValueError:
                messagebox.showerror("error! ", "UL_Freq is not as expected")
                return False
            HomeAppConfigs["DL_freq"]=self.DL_CntrFreq.get()
            try:
                integer_result = float(HomeAppConfigs["DL_freq"])
            except ValueError:
                messagebox.showerror("error! ", "DL_Freq is not as expected")
                return False
        else:
            HomeAppConfigs["UL_Freq"]=self.UL_CntrFreq.get()            
            try:
                integer_result = float(HomeAppConfigs["UL_Freq"])
            except ValueError:
                messagebox.showerror("error! ", "Center Freq is not as expected")
                return False
        HomeAppConfigs["Pwr_dBm"]=self.Power_dBm.get()
        try:
            integer_result = float(HomeAppConfigs["Pwr_dBm"])
        except ValueError:
            messagebox.showerror("error! ", "dBm Power is not as expected")
            return False
        HomeAppConfigs["Timing_Param"]=self.TimingParams.get()
        HomeAppConfigs["Rslt_Path"]=self.PathResults.get()
        if len(HomeAppConfigs["Rslt_Path"]) < 3:
            messagebox.showerror("error! ", "Result Path is not as expected")
            return False
        HomeAppConfigs["Vxt_Addrs"]=self.VXTAddrs.get()
        if len(HomeAppConfigs["Vxt_Addrs"]) < 10:
            messagebox.showerror("error! ", "VXT Address is not as expected")
            return False
        return True        
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
    def DisplaySelectedHomeConfigs(self):
        ttk.Label(self,text="Suit Type :").grid(row=3,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["TT"]).grid(row=3,column=2,sticky="E")
        ttk.Label(self,text="Frequency Band :").grid(row=5,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["FB"]).grid(row=5,column=2,sticky="E")
        ttk.Label(self,text="Cyclic Prefix :").grid(row=7,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["CP"]).grid(row=7,column=2,sticky="E")
        ttk.Label(self,text="Sub Carrier Spacing :").grid(row=9,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["SCS"]).grid(row=9,column=2,sticky="E")
        ttk.Label(self,text="Duplex Type :").grid(row=11,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["DUPLX"]).grid(row=11,column=2,sticky="E")        
        
        if HomeAppConfigs["DUPLX"] == "TDD":
            ttk.Label(self,text="Centre Freq in GHz(UL/DL) :").grid(row=13,column=1,sticky="W")
            ttk.Label(self,text=HomeAppConfigs["UL_Freq"]).grid(row=13,column=2,sticky="E")
        else:
            ttk.Label(self,text="Centre Freq in GHz(UL&DL) :").grid(row=13,column=1,sticky="W")
            ttk.Label(self,text=HomeAppConfigs["UL_Freq"]).grid(row=13,column=2,sticky="E")
            ttk.Label(self,text=",").grid(row=13,column=2,sticky="E")
            ttk.Label(self,text=HomeAppConfigs["DL_freq"]).grid(row=13,column=2,columnspan=2,sticky="E")
        ttk.Label(self,text="Power in dBm :").grid(row=15,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["Pwr_dBm"]).grid(row=15,column=2,sticky="E")
        ttk.Label(self,text="Timing Params :").grid(row=16,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["Timing_Param"]).grid(row=16,column=2,sticky="E")
        ttk.Label(self,text="Result's Path :").grid(row=17,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["Rslt_Path"]).grid(row=17,column=2,columnspan=2,sticky="E")
        ttk.Label(self,text="VXT Address :").grid(row=19,column=1,sticky="W")
        ttk.Label(self,text=HomeAppConfigs["Vxt_Addrs"]).grid(row=19,column=2,columnspan=2,sticky="E")
            
    def Radio_ButtonsH(self,ButtonOptions,ButtonName,lblName,default,row_no,col_no,cmnd):
        Bn_no=1
        self.Buttons_dict["Var_"+ButtonName] = StringVar()
        self.Buttons_dict["Var_"+ButtonName].set(default)
        self.Buttons_dict["Lbl_"+ButtonName] = ttk.Label(self,text=lblName)
        self.Buttons_dict["Lbl_"+ButtonName].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
        for txt,mod in ButtonOptions:
            name_RB = "RB"+str(Bn_no)+"_"+ButtonName
            #row_no = row_no + 1
            col_no = col_no + 1
            if cmnd == "pass":
                self.Buttons_dict[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dict["Var_"+ButtonName])
            else:
                self.Buttons_dict[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dict["Var_"+ButtonName],command=cmnd)
            self.Buttons_dict[name_RB].grid(row=row_no,column=col_no,padx=10,pady=15,sticky="W")
            Bn_no = Bn_no + 1

    def ConfFB(self):
        self.Buttons_dict["RB2_"+self.FreqBand].configure(state='disabled')
        if self.Buttons_dict["Var_"+self.FreqBand].get() == "FR1":
            self.Buttons_dict["RB4_"+self.SubCarSpcng].configure(state='disabled')
        
    def Conf_SCS(self):
        if self.Buttons_dict["Var_"+self.CyclcPrfx].get() == "Normal":
            self.Buttons_dict["Var_"+self.SubCarSpcng].set("30")
            self.Buttons_dict["RB1_"+self.SubCarSpcng].configure(state='enabled')
            self.Buttons_dict["RB2_"+self.SubCarSpcng].configure(state='enabled')
            self.Buttons_dict["RB3_"+self.SubCarSpcng].configure(state='enabled')
        else:
            self.Buttons_dict["Var_"+self.SubCarSpcng].set("60")
            self.Buttons_dict["RB1_"+self.SubCarSpcng].configure(state='disabled')
            self.Buttons_dict["RB2_"+self.SubCarSpcng].configure(state='disabled')
            self.Buttons_dict["RB3_"+self.SubCarSpcng].configure(state='enabled')
            
    def Conf_UL_DL_Centr_Freq(self):         
        if self.Buttons_dict["Var_"+self.DuplexTyps].get() == "TDD":
            self.DL_CntrFreq_entry.destroy()
            self.Cntrfreq_Lbl = ttk.Label(self,text="Centre Freq in GHz(UL/DL) :").grid(row=13,column=2,padx=5,pady=15,sticky="W")
            self.UL_CntrFreq_entry = ttk.Entry(self, textvariable=self.UL_CntrFreq)
            self.UL_CntrFreq_entry.grid(row=13,column=3,padx=6,pady=15,sticky="W")
        else:
            self.Cntrfreq_Lbl = ttk.Label(self,text="Centre Freq in GHz(UL&DL) :").grid(row=13,column=2,padx=5,pady=15,sticky="W")
            self.UL_CntrFreq_entry = ttk.Entry(self, textvariable=self.UL_CntrFreq)
            self.UL_CntrFreq_entry.grid(row=13,column=3,padx=6,pady=15,sticky="W")
            self.DL_CntrFreq_entry = ttk.Entry(self, textvariable=self.DL_CntrFreq)
            self.DL_CntrFreq_entry.grid(row=13,column=4,columnspan=2,padx=6,pady=15,sticky="W")
            
class ConformanceApp(ttk.Frame):
    """ This application Provides the Conformance Testing's configuarion Parametrs....... """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        global HomeAppConfigs
        global is_SavePressedHme
        self.is_SubmitPressedConf = 0
        if not is_SavePressedHme:
            self.clear_frame()
            self.NotConfSuit_Lbl = ttk.Label(self,text="You are not saved the Home Configurations").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        else:
            if HomeAppConfigs["TT"] == "Conformance":
                self.clear_frame()
                self.Buttons_dictC={}
                
                Optns_PhaseCompnstn = (("OFF","F"),("ON","T"))
                self.PhaseCompnstn="PC"
                LabelPC="Phase Compensatoion : "
                self.Radio_ButtonsC(Optns_PhaseCompnstn,self.PhaseCompnstn,LabelPC,"F",2,2,"pass")
                
                Optns_NumofLayers = (("1","1"),("2","2"),("3","3"),("4","4"))
                self.NumofLayers="Layers"
                LabelNumofLayers="Numbe of Layers : "
                self.Radio_ButtonsC(Optns_NumofLayers,self.NumofLayers,LabelNumofLayers,"1",3,2,"pass")
                
                self.eAXcid = StringVar()
                self.eAXcid_Lbl = ttk.Label(self,text="eAXcid :").grid(row=4,column=2,padx=5,pady=15,sticky="W")
                self.eAXcid_entry = ttk.Entry(self, textvariable=self.eAXcid)
                self.eAXcid_entry.grid(row=4,column=3,columnspan=3,padx=5,pady=10,sticky="W")
                
                if HomeAppConfigs["SCS"] == "15":
                    Optns_BW1 = [('5MHz',5),('10MHz',10),('15MHz',15),('20MHz',20),('30MHz',30)]
                    Optns_BW2 = [('40MHz',40),('50MHz',50)]
                else:
                    Optns_BW1 = [('10MHz',10),('20MHz',20),('30MHz',30),('40MHz',40),('50MHz',50)]
                    Optns_BW2 = [('60MHz',60),('70MHz',70),('80MHz',80),('90MHz',90),('100MHz',100)]
                self.BWs_CheckButton_lbl = ttk.Label(self,text="Band Widths :")
                self.BWs_CheckButton_lbl.grid(row=6,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtons_dict={}
                self.VarCheckButton_dict={}
                self.CheckButtonC(Optns_BW1,6,2,"_BWs",1,"pass")
                self.CheckButtonC(Optns_BW2,7,2,"_BWs",6,"pass")
                
                Optns_FRC1 = [("A1_QPSK_R=1|3",1),("A4_16QAM_R=658|1024",7),("A5_64QAM_R=567|1024",8),("A9_256QAM_R=682.5|1024",9)]
                self.UL_FRC_ChkBtn_lbl = ttk.Label(self,text="UL FRCs Modulations :")
                self.UL_FRC_ChkBtn_lbl.grid(row=8,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonC(Optns_FRC1,8,2,"_UL_FRC",1,"pass")
                
                Optns_TM1 = [("TM1_1_QPSK",1),("TM3_2_16QAM",10),("TM3_1_64QAM",5),("TM3_1_a_256QAM",7)]
                self.DL_TM_ChkBtn_lbl = ttk.Label(self,text="DL TM Modulations :")
                self.DL_TM_ChkBtn_lbl.grid(row=10,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonC(Optns_TM1,10,2,"_DL_TM",1,"pass")
                
                self.SubmitBtn = ttk.Button(self, text="Submit", command=self.submitButton)
                self.SubmitBtn.grid(row=12,column=3,padx=6,pady=10,sticky="E")
                
            else:
                self.clear_frame()
                self.NotConfSuit_Lbl = ttk.Label(self,text="The Suit you are selected is not Conformance").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def CheckButtonC(self,Optns_BW,row_no,col_no,lbl,Bn_no,cmnd):
        for txt,mod in Optns_BW:
            name_var = "Var"+str(Bn_no)+lbl
            name_RB = "CB"+str(Bn_no)+lbl
            self.VarCheckButton_dict[name_var] = IntVar()
            col_no = col_no + 1
            if cmnd == "pass":
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0)
            else:
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0,command=self.cmnds)
            self.CheckButtons_dict[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1        
            
    def Radio_ButtonsC(self,ButtonOptions,ButtonName,lblName,default,row_no,col_no,cmnd):
        Bn_no=1
        self.Buttons_dictC["Var_"+ButtonName] = StringVar()
        self.Buttons_dictC["Var_"+ButtonName].set(default)
        self.Buttons_dictC["Lbl_"+ButtonName] = ttk.Label(self,text=lblName)
        self.Buttons_dictC["Lbl_"+ButtonName].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
        for txt,mod in ButtonOptions:
            name_RB = "RB"+str(Bn_no)+"_"+ButtonName
            col_no = col_no + 1
            if cmnd == "pass":
                self.Buttons_dictC[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictC["Var_"+ButtonName])
            else:
                self.Buttons_dictC[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictC["Var_"+ButtonName],command=self.cmnds)
            self.Buttons_dictC[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1
            
    def cmnds(self):
        print("Hi")
        
    def writeRequirementTxt(self):
        global HomeAppConfigs
        with open('requirement.txt', 'w') as f:
            f.write("Suit Type ="+HomeAppConfigs["TT"]+"\n")
            f.write("Frequency Band ="+HomeAppConfigs["FB"]+"\n")
            f.write("Cyclic Prefix ="+HomeAppConfigs["CP"]+"\n")
            f.write("Sub Carrier Spacing ="+HomeAppConfigs["SCS"]+"\n")
            f.write("Duplex Type ="+HomeAppConfigs["DUPLX"]+"\n")
            if HomeAppConfigs["DUPLX"] =="TDD":
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
            else:
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["DL_freq"]+"\n")
            f.write("Power in dBm ="+HomeAppConfigs["Pwr_dBm"]+"\n")
            f.write("Delay Timing Params ="+HomeAppConfigs["Timing_Param"]+"\n")
            f.write("Result's Path ="+HomeAppConfigs["Rslt_Path"]+"\n")
            f.write("VXT Address ="+HomeAppConfigs["Vxt_Addrs"]+"\n")
            
            f.write("Phase Compensation ="+self.ConformanceAppConfigs["PC"]+"\n")
            f.write("Number of Layers ="+self.ConformanceAppConfigs["NumofLayer"]+"\n")
            f.write("eAxCid ="+self.ConformanceAppConfigs["eAxCid"]+"\n")
            f.write("Band Widths =")
            for bw in self.BWs_list:
                f.write(str(bw.get())+",")
            f.write("\n")
            f.write("UL FRCs Modulations =")
            for frc in self.UL_FRC_list:
                f.write(str(frc.get())+",")
            f.write("\n")
            f.write("DL TM Modulations =")
            for tm in self.DL_TMs_list:
                f.write(str(tm.get())+",")
            f.write("\n")
            f.close()
         
        
    def submitButton(self):
        readStatus = self.ReadConformanceAppConfigs()
        if not readStatus:
            messagebox.showinfo("information", "Config Cant be saved correct and save again")
            return False
        else:
            self.clear_frame()
            self.DisplaySelectedHomeConfigs()
            self.EditBtn = ttk.Button(self, text="Edit", command=self.editButton)
            self.EditBtn.grid(row=13,column=3,padx=0,pady=10,sticky="W")
            self.is_SubmitPressedConf = 1
            self.writeRequirementTxt()
        return True
        
    def editButton(self):
        self.clear_frame()
        self.createWidgets()
        self.is_SubmitPressedConf = 0        
        
    def ReadConformanceAppConfigs(self):
        self.ConformanceAppConfigs = {}
        self.ConformanceAppConfigs["PC"]=self.Buttons_dictC["Var_"+self.PhaseCompnstn].get()
        self.ConformanceAppConfigs["NumofLayer"]=self.Buttons_dictC["Var_"+self.NumofLayers].get()
        self.ConformanceAppConfigs["eAxCid"]=self.eAXcid.get()
        self.ConformanceAppConfigs["Vars_CBs"]=self.VarCheckButton_dict
        return True        
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
    def DisplaySelectedHomeConfigs(self):
        clmn=2
        self.BWs_list=[]
        self.UL_FRC_list=[]
        self.DL_TMs_list=[]
        ttk.Label(self,text="Phase Compensation :").grid(row=3,column=1,sticky="W")
        ttk.Label(self,text=self.ConformanceAppConfigs["PC"]).grid(row=3,column=2,sticky="E")
        ttk.Label(self,text="Number of Layers :").grid(row=4,column=1,sticky="W")
        ttk.Label(self,text=self.ConformanceAppConfigs["NumofLayer"]).grid(row=4,column=2,sticky="E")
        ttk.Label(self,text="eAxCid :").grid(row=5,column=1,sticky="W")
        ttk.Label(self,text=self.ConformanceAppConfigs["eAxCid"]).grid(row=5,column=2,sticky="E")        
        Var_dict=self.ConformanceAppConfigs["Vars_CBs"]        
        for key in Var_dict:
            if "_BWs" in key:
                self.BWs_list.append(Var_dict[key])
            elif "_UL_FRC" in key:
                self.UL_FRC_list.append(Var_dict[key])
            elif "_DL_TM" in key:
                self.DL_TMs_list.append(Var_dict[key])
                
        clmn=2
        ttk.Label(self,text="Band Widths :").grid(row=7,column=1,sticky="W")
        for bw in self.BWs_list:
            ttk.Label(self,text=bw.get()).grid(row=7,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="UL FRCs Modulations :").grid(row=9,column=1,sticky="W")
        for frc in self.UL_FRC_list:
            ttk.Label(self,text=frc.get()).grid(row=9,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="DL TM Modulations :").grid(row=11,column=1,sticky="W")
        for tm in self.DL_TMs_list:
            ttk.Label(self,text=tm.get()).grid(row=11,column=clmn,sticky="E")
            clmn=clmn+1 
            
class FunctionalApp(ttk.Frame):
    """ This application Provides the Functional Testing's configuarion Parametrs....... """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        global HomeAppConfigs
        global is_SavePressedHme
        self.is_SubmitPressedFunc = 0
        if not is_SavePressedHme:
            self.clear_frame()
            self.NotConfSuit_Lbl = ttk.Label(self,text="You are not saved the Home Configurations").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        else:
            if HomeAppConfigs["TT"] == "Functional":
                self.clear_frame()
                self.Buttons_dictF={}
                
                Optns_PhaseCompnstn = (("OFF","F"),("ON","T"))
                self.PhaseCompnstn="PC"
                LabelPC="Phase Compensatoion : "
                self.Radio_ButtonsF(Optns_PhaseCompnstn,self.PhaseCompnstn,LabelPC,"F",2,2,"pass")
                
                Optns_NumofLayers = (("1","1"),("2","2"),("3","3"),("4","4"))
                self.NumofLayers="Layers"
                LabelNumofLayers="Numbe of Layers : "
                self.Radio_ButtonsF(Optns_NumofLayers,self.NumofLayers,LabelNumofLayers,"1",3,2,"pass")
                
                self.eAXcid = StringVar()
                self.eAXcid_Lbl = ttk.Label(self,text="eAXcid :").grid(row=4,column=2,padx=5,pady=15,sticky="W")
                self.eAXcid_entry = ttk.Entry(self, textvariable=self.eAXcid)
                self.eAXcid_entry.grid(row=4,column=3,columnspan=3,padx=5,pady=10,sticky="W")
                
                if HomeAppConfigs["SCS"] == "15":
                    Optns_BW1 = [('5MHz',5),('10MHz',10),('15MHz',15),('20MHz',20),('30MHz',30)]
                    Optns_BW2 = [('40MHz',40),('50MHz',50)]
                else:
                    Optns_BW1 = [('10MHz',10),('20MHz',20),('30MHz',30),('40MHz',40),('50MHz',50)]
                    Optns_BW2 = [('60MHz',60),('70MHz',70),('80MHz',80),('90MHz',90),('100MHz',100)]
                self.BWs_CheckButton_lbl = ttk.Label(self,text="Band Widths :")
                self.BWs_CheckButton_lbl.grid(row=6,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtons_dict={}
                self.VarCheckButton_dict={}
                self.CheckButtonF(Optns_BW1,6,2,"_BWs",1,"pass")
                self.CheckButtonF(Optns_BW2,7,2,"_BWs",6,"pass")
                
                Optns_FRC1 = [("A1_QPSK_R=1|3",1),("A4_16QAM_R=658|1024",7),("A5_64QAM_R=567|1024",8),("A9_256QAM_R=682.5|1024",9)]                           
                self.UL_FRC_ChkBtn_lbl = ttk.Label(self,text="UL FRCs Modulations :")
                self.UL_FRC_ChkBtn_lbl.grid(row=8,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonF(Optns_FRC1,8,2,"_UL_FRC",1,"pass")
                
                Optns_TM1 = [("TM1_1_QPSK",1),("TM3_2_16QAM",10),("TM3_1_64QAM",5),("TM3_1_a_256QAM",7)]
                self.DL_TM_ChkBtn_lbl = ttk.Label(self,text="DL TM Modulations :")
                self.DL_TM_ChkBtn_lbl.grid(row=10,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonF(Optns_TM1,10,2,"_DL_TM",1,"pass")
                
                self.SubmitBtn = ttk.Button(self, text="Submit", command=self.submitButton)
                self.SubmitBtn.grid(row=12,column=3,padx=6,pady=10,sticky="E")
                
            else:
                self.clear_frame()
                self.NotConfSuit_Lbl = ttk.Label(self,text="The Suit you are selected is not Functional").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def CheckButtonF(self,Optns_BW,row_no,col_no,lbl,Bn_no,cmnd):
        for txt,mod in Optns_BW:
            name_var = "Var"+str(Bn_no)+lbl
            name_RB = "CB"+str(Bn_no)+lbl
            self.VarCheckButton_dict[name_var] = IntVar()
            col_no = col_no + 1
            if cmnd == "pass":
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0)
            else:
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0,command=self.cmnds)
            self.CheckButtons_dict[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1        
            
    def Radio_ButtonsF(self,ButtonOptions,ButtonName,lblName,default,row_no,col_no,cmnd):
        Bn_no=1
        self.Buttons_dictF["Var_"+ButtonName] = StringVar()
        self.Buttons_dictF["Var_"+ButtonName].set(default)
        self.Buttons_dictF["Lbl_"+ButtonName] = ttk.Label(self,text=lblName)
        self.Buttons_dictF["Lbl_"+ButtonName].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
        for txt,mod in ButtonOptions:
            name_RB = "RB"+str(Bn_no)+"_"+ButtonName
            col_no = col_no + 1
            if cmnd == "pass":
                self.Buttons_dictF[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictF["Var_"+ButtonName])
            else:
                self.Buttons_dictF[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictF["Var_"+ButtonName],command=self.cmnds)
            self.Buttons_dictF[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1
            
    def cmnds(self):
        print("Hi")
        
    def writeRequirementTxt(self):
        global HomeAppConfigs
        with open('requirement.txt', 'w') as f:
            f.write("Suit Type ="+HomeAppConfigs["TT"]+"\n")
            f.write("Frequency Band ="+HomeAppConfigs["FB"]+"\n")
            f.write("Cyclic Prefix ="+HomeAppConfigs["CP"]+"\n")
            f.write("Sub Carrier Spacing ="+HomeAppConfigs["SCS"]+"\n")
            f.write("Duplex Type ="+HomeAppConfigs["DUPLX"]+"\n")
            if HomeAppConfigs["DUPLX"] =="TDD":
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
            else:
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["DL_freq"]+"\n")
            f.write("Power in dBm ="+HomeAppConfigs["Pwr_dBm"]+"\n")
            f.write("Delay Timing Params ="+HomeAppConfigs["Timing_Param"]+"\n")
            f.write("Result's Path ="+HomeAppConfigs["Rslt_Path"]+"\n")
            f.write("VXT Address ="+HomeAppConfigs["Vxt_Addrs"]+"\n")
            
            f.write("Phase Compensation ="+self.FunctionalAppConfigs["PC"]+"\n")
            f.write("Number of Layers ="+self.FunctionalAppConfigs["NumofLayer"]+"\n")
            f.write("eAxCid ="+self.FunctionalAppConfigs["eAxCid"]+"\n")
            f.write("Band Widths =")
            for bw in self.BWs_list:
                f.write(str(bw.get())+",")
            f.write("\n")
            f.write("UL FRCs Modulations =")
            for frc in self.UL_FRC_list:
                f.write(str(frc.get())+",")
            f.write("\n")
            f.write("DL TM Modulations =")
            for tm in self.DL_TMs_list:
                f.write(str(tm.get())+",")
            f.write("\n")
            f.close()
        
    def submitButton(self):
        readStatus = self.ReadFunctionalAppConfigs()
        if not readStatus:
            messagebox.showinfo("information", "Config Cant be saved correct and save again")
            return False
        else:
            self.clear_frame()
            self.DisplaySelectedHomeConfigs()
            self.EditBtn = ttk.Button(self, text="Edit", command=self.editButton)
            self.EditBtn.grid(row=13,column=3,padx=0,pady=10,sticky="W")
            self.is_SubmitPressedFunc = 1
            self.writeRequirementTxt()
        return True
        
    def editButton(self):
        self.clear_frame()
        self.createWidgets()
        self.is_SubmitPressedFunc = 0        
        
    def ReadFunctionalAppConfigs(self):
        self.FunctionalAppConfigs = {}
        self.FunctionalAppConfigs["PC"]=self.Buttons_dictF["Var_"+self.PhaseCompnstn].get()
        self.FunctionalAppConfigs["NumofLayer"]=self.Buttons_dictF["Var_"+self.NumofLayers].get()
        self.FunctionalAppConfigs["eAxCid"]=self.eAXcid.get()
        self.FunctionalAppConfigs["Vars_CBs"]=self.VarCheckButton_dict
        return True        
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
    def DisplaySelectedHomeConfigs(self):        
        self.BWs_list=[]
        self.UL_FRC_list=[]
        self.DL_TMs_list=[] 
        ttk.Label(self,text="Phase Compensation :").grid(row=3,column=1,sticky="W")
        ttk.Label(self,text=self.FunctionalAppConfigs["PC"]).grid(row=3,column=2,sticky="E")
        ttk.Label(self,text="Number of Layers :").grid(row=4,column=1,sticky="W")
        ttk.Label(self,text=self.FunctionalAppConfigs["NumofLayer"]).grid(row=4,column=2,sticky="E")
        ttk.Label(self,text="eAxCid :").grid(row=5,column=1,sticky="W")
        ttk.Label(self,text=self.FunctionalAppConfigs["eAxCid"]).grid(row=5,column=2,sticky="E")        
        Var_dict=self.FunctionalAppConfigs["Vars_CBs"]        
        for key in Var_dict:
            if "_BWs" in key:
                self.BWs_list.append(Var_dict[key])
            elif "_UL_FRC" in key:
                self.UL_FRC_list.append(Var_dict[key])
            elif "_DL_TM" in key:
                self.DL_TMs_list.append(Var_dict[key])
                
        clmn=2
        ttk.Label(self,text="Band Widths :").grid(row=7,column=1,sticky="W")
        for bw in self.BWs_list:
            ttk.Label(self,text=bw.get()).grid(row=7,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="UL FRCs Modulations :").grid(row=9,column=1,sticky="W")
        for frc in self.UL_FRC_list:
            ttk.Label(self,text=frc.get()).grid(row=9,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="DL TM Modulations :").grid(row=11,column=1,sticky="W")
        for tm in self.DL_TMs_list:
            ttk.Label(self,text=tm.get()).grid(row=11,column=clmn,sticky="E")
            clmn=clmn+1 
            

class RCTApp(ttk.Frame):
    """ This application Provides the RCT Testing's configuarion Parametrs....... """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        global HomeAppConfigs
        global is_SavePressedHme
        self.is_SubmitPressedRCT = 0
        if not is_SavePressedHme:
            self.clear_frame()
            self.NotConfSuit_Lbl = ttk.Label(self,text="You are not saved the Home Configurations").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        else:
            if HomeAppConfigs["TT"] == "RCT":
                self.clear_frame()
                self.Buttons_dictR={}
                
                Optns_PhaseCompnstn = (("OFF","F"),("ON","T"))
                self.PhaseCompnstn="PC"
                LabelPC="Phase Compensatoion : "
                self.Radio_ButtonsR(Optns_PhaseCompnstn,self.PhaseCompnstn,LabelPC,"F",2,2,"pass")
                
                Optns_NumofLayers = (("1","1"),("2","2"),("3","3"),("4","4"))
                self.NumofLayers="Layers"
                LabelNumofLayers="Numbe of Layers : "
                self.Radio_ButtonsR(Optns_NumofLayers,self.NumofLayers,LabelNumofLayers,"1",3,2,"pass")
                
                self.eAXcid = StringVar()
                self.eAXcid_Lbl = ttk.Label(self,text="eAXcid :").grid(row=4,column=2,padx=5,pady=15,sticky="W")
                self.eAXcid_entry = ttk.Entry(self, textvariable=self.eAXcid)
                self.eAXcid_entry.grid(row=4,column=3,columnspan=3,padx=5,pady=10,sticky="W")
                
                if HomeAppConfigs["SCS"] == "15":
                    Optns_BW1 = [('5MHz',5),('10MHz',10),('15MHz',15),('20MHz',20),('30MHz',30)]
                    Optns_BW2 = [('40MHz',40),('50MHz',50)]
                else:
                    Optns_BW1 = [('10MHz',10),('20MHz',20),('30MHz',30),('40MHz',40),('50MHz',50)]
                    Optns_BW2 = [('60MHz',60),('70MHz',70),('80MHz',80),('90MHz',90),('100MHz',100)]
                self.BWs_CheckButton_lbl = ttk.Label(self,text="Band Widths :")
                self.BWs_CheckButton_lbl.grid(row=6,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtons_dict={}
                self.VarCheckButton_dict={}
                self.CheckButtonR(Optns_BW1,6,2,"_BWs",1,"pass")
                self.CheckButtonR(Optns_BW2,7,2,"_BWs",6,"pass")
                
                Optns_FRC1 = [("A1_QPSK_R=1|3",1),("A3_QPSK_R=193|1024",2),("A3A_QPSK_R=99|1024",3),
                              ("A3B_QPSK_R=308|1024",4),("A8|A7_QPSK_R=157|1024",5)]                            
                self.UL_FRC_ChkBtn_lbl = ttk.Label(self,text="UL FRCs Modulations :")
                self.UL_FRC_ChkBtn_lbl.grid(row=8,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonR(Optns_FRC1,8,2,"_UL_FRC",1,"pass")
                Optns_FRC2 = [("A2_16QAM_R=2|3",6),("A4_16QAM_R=658|1024",7),("A5_64QAM_R=567|1024",8),
                               ("A9_256QAM_R=682.5|1024",9)]
                self.CheckButtonR(Optns_FRC2,9,2,"_UL_FRC",6,"pass")
                
                Optns_TM1 = [("TM1_1_QPSK",1),("TM1_2_QPSK",2),("TM3_3_QPSK",3),("TM2_64QAM",4),("TM3_1_64QAM",5)]
                self.DL_TM_ChkBtn_lbl = ttk.Label(self,text="DL TM Modulations :")
                self.DL_TM_ChkBtn_lbl.grid(row=10,column=2,padx=5,pady=15,sticky="W")
                self.CheckButtonR(Optns_TM1,10,2,"_DL_TM",1,"pass")
                Optns_TM2 = [("TM2_a_256QAM",6),("TM3_1_a_256QAM",7),("TM2_b_1024QAM",8),("TM3_1_b_1024QAM",9),("TM3_2_16QAM",10)]
                self.CheckButtonR(Optns_TM2,11,2,"_DL_TM",6,"pass")
                
                self.SubmitBtn = ttk.Button(self, text="Submit", command=self.submitButton)
                self.SubmitBtn.grid(row=12,column=3,padx=6,pady=10,sticky="E")
                
            else:
                self.clear_frame()
                self.NotConfSuit_Lbl = ttk.Label(self,text="The Suit you are selected is not RCT").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def CheckButtonR(self,Optns_BW,row_no,col_no,lbl,Bn_no,cmnd):
        for txt,mod in Optns_BW:
            name_var = "Var"+str(Bn_no)+lbl
            name_RB = "CB"+str(Bn_no)+lbl
            self.VarCheckButton_dict[name_var] = IntVar()
            col_no = col_no + 1
            if cmnd == "pass":
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0)
            else:
                self.CheckButtons_dict[name_RB] = ttk.Checkbutton(self,text=txt,variable=self.VarCheckButton_dict[name_var],onvalue=mod,offvalue = 0,command=self.cmnds)
            self.CheckButtons_dict[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1        
            
    def Radio_ButtonsR(self,ButtonOptions,ButtonName,lblName,default,row_no,col_no,cmnd):
        Bn_no=1
        self.Buttons_dictR["Var_"+ButtonName] = StringVar()
        self.Buttons_dictR["Var_"+ButtonName].set(default)
        self.Buttons_dictR["Lbl_"+ButtonName] = ttk.Label(self,text=lblName)
        self.Buttons_dictR["Lbl_"+ButtonName].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
        for txt,mod in ButtonOptions:
            name_RB = "RB"+str(Bn_no)+"_"+ButtonName
            col_no = col_no + 1
            if cmnd == "pass":
                self.Buttons_dictR[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictR["Var_"+ButtonName])
            else:
                self.Buttons_dictR[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictR["Var_"+ButtonName],command=self.cmnds)
            self.Buttons_dictR[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1
            
    def cmnds(self):
        print("Hi")
        
    def writeRequirementTxt(self):
        global HomeAppConfigs
        with open('requirement.txt', 'w') as f:
            f.write("Suit Type ="+HomeAppConfigs["TT"]+"\n")
            f.write("Frequency Band ="+HomeAppConfigs["FB"]+"\n")
            f.write("Cyclic Prefix ="+HomeAppConfigs["CP"]+"\n")
            f.write("Sub Carrier Spacing ="+HomeAppConfigs["SCS"]+"\n")
            f.write("Duplex Type ="+HomeAppConfigs["DUPLX"]+"\n")
            if HomeAppConfigs["DUPLX"] =="TDD":
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
            else:
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["DL_freq"]+"\n")
            f.write("Power in dBm ="+HomeAppConfigs["Pwr_dBm"]+"\n")
            f.write("Delay Timing Params ="+HomeAppConfigs["Timing_Param"]+"\n")
            f.write("Result's Path ="+HomeAppConfigs["Rslt_Path"]+"\n")
            f.write("VXT Address ="+HomeAppConfigs["Vxt_Addrs"]+"\n")
            
            f.write("Phase Compensation ="+self.RCTAppConfigs["PC"]+"\n")
            f.write("Number of Layers ="+self.RCTAppConfigs["NumofLayer"]+"\n")
            f.write("eAxCid ="+self.RCTAppConfigs["eAxCid"]+"\n")
            f.write("Band Widths =")
            for bw in self.BWs_list:
                f.write(str(bw.get())+",")
            f.write("\n")
            f.write("UL FRCs Modulations =")
            for frc in self.UL_FRC_list:
                f.write(str(frc.get())+",")
            f.write("\n")
            f.write("DL TM Modulations =")
            for tm in self.DL_TMs_list:
                f.write(str(tm.get())+",")
            f.write("\n")
            f.close()
        
    def submitButton(self):
        readStatus = self.ReadRCTAppConfigs()
        if not readStatus:
            messagebox.showinfo("information", "Config Cant be saved correct and save again")
            return False
        else:
            self.clear_frame()
            self.DisplaySelectedHomeConfigs()
            self.EditBtn = ttk.Button(self, text="Edit", command=self.editButton)
            self.EditBtn.grid(row=13,column=3,padx=0,pady=10,sticky="W")
            self.is_SubmitPressedRCT = 1
            self.writeRequirementTxt()
        return True
        
    def editButton(self):
        self.clear_frame()
        self.createWidgets()
        self.is_SubmitPressedRCT = 0        
        
    def ReadRCTAppConfigs(self):
        self.RCTAppConfigs = {}
        self.RCTAppConfigs["PC"]=self.Buttons_dictR["Var_"+self.PhaseCompnstn].get()
        self.RCTAppConfigs["NumofLayer"]=self.Buttons_dictR["Var_"+self.NumofLayers].get()
        self.RCTAppConfigs["eAxCid"]=self.eAXcid.get()
        self.RCTAppConfigs["Vars_CBs"]=self.VarCheckButton_dict
        return True        
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
    def DisplaySelectedHomeConfigs(self):        
        self.BWs_list=[]
        self.UL_FRC_list=[]
        self.DL_TMs_list=[] 
        ttk.Label(self,text="Phase Compensation :").grid(row=3,column=1,sticky="W")
        ttk.Label(self,text=self.RCTAppConfigs["PC"]).grid(row=3,column=2,sticky="E")
        ttk.Label(self,text="Number of Layers :").grid(row=4,column=1,sticky="W")
        ttk.Label(self,text=self.RCTAppConfigs["NumofLayer"]).grid(row=4,column=2,sticky="E")        
        ttk.Label(self,text="eAxCid :").grid(row=5,column=1,sticky="W")
        ttk.Label(self,text=self.RCTAppConfigs["eAxCid"]).grid(row=5,column=2,sticky="E")        
        Var_dict=self.RCTAppConfigs["Vars_CBs"]        
        for key in Var_dict:
            if "_BWs" in key:
                self.BWs_list.append(Var_dict[key])
            elif "_UL_FRC" in key:
                self.UL_FRC_list.append(Var_dict[key])
            elif "_DL_TM" in key:
                self.DL_TMs_list.append(Var_dict[key])
                
        clmn=2
        ttk.Label(self,text="Band Widths :").grid(row=7,column=1,sticky="W")
        for bw in self.BWs_list:
            ttk.Label(self,text=bw.get()).grid(row=7,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="UL FRCs Modulations :").grid(row=9,column=1,sticky="W")
        for frc in self.UL_FRC_list:
            ttk.Label(self,text=frc.get()).grid(row=9,column=clmn,sticky="E")
            clmn=clmn+1
        clmn=2
        ttk.Label(self,text="DL TM Modulations :").grid(row=11,column=1,sticky="W")
        for tm in self.DL_TMs_list:
            ttk.Label(self,text=tm.get()).grid(row=11,column=clmn,sticky="E")
            clmn=clmn+1 
            
class BasicApp(ttk.Frame,):
    """ This application Provides Basic DL and UL configuarion Parametrs....... """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        global HomeAppConfigs
        global is_SavePressedHme
        self.is_SubmitPressedBasic = 0
        if not is_SavePressedHme:
            self.clear_frame()
            self.NotConfSuit_Lbl = ttk.Label(self,text="You are not saved the Home Configurations").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        else:
            if HomeAppConfigs["TT"] == "Basic":
                self.clear_frame()
                self.Buttons_dictB={}
                
                Optns_PhaseCompnstn = [("OFF","F")]
                self.PhaseCompnstn="PC"
                LabelPC="Phase Compensatoion : "
                self.Radio_ButtonsB(Optns_PhaseCompnstn,self.PhaseCompnstn,LabelPC,"F",2,2,"pass")
                
                Optns_NumofLayers = [("1","1")]
                self.NumofLayers="Layers"
                LabelNumofLayers="Numbe of Layer : "
                self.Radio_ButtonsB(Optns_NumofLayers,self.NumofLayers,LabelNumofLayers,"1",3,2,"pass")
                
                self.eAXcid = StringVar()
                self.eAXcid_Lbl = ttk.Label(self,text="eAXcid :").grid(row=4,column=2,padx=5,pady=15,sticky="W")
                self.eAXcid_entry = ttk.Entry(self, textvariable=self.eAXcid)
                self.eAXcid_entry.grid(row=4,column=3,columnspan=3,padx=5,pady=10,sticky="W")
                
                if HomeAppConfigs["SCS"] == "15":
                    Optns_BW = [('20MHz',20)]
                    deflt="20"
                else:
                    Optns_BW = [('100MHz',100)]
                    deflt="100"
                self.BW_Basic="_BW_Basic"
                LabelBW_Basic="Band Width : "
                self.Radio_ButtonsB(Optns_BW,self.BW_Basic,LabelBW_Basic,deflt,7,2,"pass")
                    
                Optns_FRC = [("A1_QPSK_R=1|3","1")]
                self.UL_FRC="_UL_FRC"
                LabelUL_FRC="UL FRCs Modulations : "
                self.Radio_ButtonsB(Optns_FRC,self.UL_FRC,LabelUL_FRC,"1",9,2,"pass")
                
                Optns_TM = [("TM1_1_QPSK","1")]
                self.DL_TM="_DL_TMC"
                LabelDL_TM="DL TM Modulations : "
                self.Radio_ButtonsB(Optns_TM,self.DL_TM,LabelDL_TM,"1",11,2,"pass")
                
                self.SubmitBtn = ttk.Button(self, text="Submit", command=self.submitButton)
                self.SubmitBtn.grid(row=12,column=3,padx=6,pady=10,sticky="E")
                
            else:
                self.clear_frame()
                self.NotConfSuit_Lbl = ttk.Label(self,text="The Suit you are selected is not Basic").grid(row=3,column=4,columnspan=2,padx=5,pady=15,sticky="NSEW")
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def Radio_ButtonsB(self,ButtonOptions,ButtonName,lblName,default,row_no,col_no,cmnd):
        Bn_no=1
        self.Buttons_dictB["Var_"+ButtonName] = StringVar()
        self.Buttons_dictB["Var_"+ButtonName].set(default)
        self.Buttons_dictB["Lbl_"+ButtonName] = ttk.Label(self,text=lblName)
        self.Buttons_dictB["Lbl_"+ButtonName].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
        for txt,mod in ButtonOptions:
            name_RB = "RB"+str(Bn_no)+"_"+ButtonName
            col_no = col_no + 1
            if cmnd == "pass":
                self.Buttons_dictB[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictB["Var_"+ButtonName])
            else:
                self.Buttons_dictB[name_RB] = ttk.Radiobutton(self,text=txt,value=mod,variable=self.Buttons_dictB["Var_"+ButtonName],command=self.cmnds)
            self.Buttons_dictB[name_RB].grid(row=row_no,column=col_no,padx=5,pady=15,sticky="W")
            Bn_no = Bn_no + 1
            
    def cmnds(self):
        print("Hi")
        
    def writeRequirementTxt(self):
        global HomeAppConfigs
        with open('requirement.txt', 'w') as f:
            f.write("Suit Type ="+HomeAppConfigs["TT"]+"\n")
            f.write("Frequency Band ="+HomeAppConfigs["FB"]+"\n")
            f.write("Cyclic Prefix ="+HomeAppConfigs["CP"]+"\n")
            f.write("Sub Carrier Spacing ="+HomeAppConfigs["SCS"]+"\n")
            f.write("Duplex Type ="+HomeAppConfigs["DUPLX"]+"\n")
            if HomeAppConfigs["DUPLX"] =="TDD":
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
            else:
                f.write("UL Center Freq ="+HomeAppConfigs["UL_Freq"]+"\n")
                f.write("DL Center Freq ="+HomeAppConfigs["DL_freq"]+"\n")
            f.write("Power in dBm ="+HomeAppConfigs["Pwr_dBm"]+"\n")
            f.write("Delay Timing Params ="+HomeAppConfigs["Timing_Param"]+"\n")
            f.write("Result's Path ="+HomeAppConfigs["Rslt_Path"]+"\n")
            f.write("VXT Address ="+HomeAppConfigs["Vxt_Addrs"]+"\n")
            
            f.write("Phase Compensation ="+self.BasicAppConfigs["PC"]+"\n")
            f.write("Number of Layers ="+self.BasicAppConfigs["NumofLayer"]+"\n")
            f.write("eAxCid ="+self.BasicAppConfigs["eAxCid"]+"\n")
            f.write("Band Widths ="+self.BasicAppConfigs["Band Width"]+"\n")
            f.write("UL FRCs Modulations ="+self.BasicAppConfigs["UL_FRCs"]+"\n")
            f.write("DL TM Modulations ="+self.BasicAppConfigs["DL_TMs"]+"\n")
            f.close()
        
    def submitButton(self):
        readStatus = self.ReadBasicAppConfigs()
        if not readStatus:
            messagebox.showinfo("information", "Config Cant be saved correct and save again")
            return False
        else:
            self.clear_frame()
            self.DisplaySelectedHomeConfigs()
            self.EditBtn = ttk.Button(self, text="Edit", command=self.editButton)
            self.EditBtn.grid(row=13,column=3,padx=0,pady=10,sticky="W")
            self.is_SubmitPressedBasic = 1
            self.writeRequirementTxt()
        return True
        
    def editButton(self):
        self.clear_frame()
        self.createWidgets()
        self.is_SubmitPressedBasic = 0        
        
    def ReadBasicAppConfigs(self):
        self.BasicAppConfigs = {}
        self.BasicAppConfigs["PC"]=self.Buttons_dictB["Var_"+self.PhaseCompnstn].get()
        self.BasicAppConfigs["NumofLayer"]=self.Buttons_dictB["Var_"+self.NumofLayers].get()
        self.BasicAppConfigs["eAxCid"]=self.eAXcid.get()
        self.BasicAppConfigs["Band Width"]=self.Buttons_dictB["Var_"+self.BW_Basic].get()
        self.BasicAppConfigs["UL_FRCs"]=self.Buttons_dictB["Var_"+self.UL_FRC].get()
        self.BasicAppConfigs["DL_TMs"]=self.Buttons_dictB["Var_"+self.DL_TM].get()        
        return True        
        
    def clear_frame(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
    def DisplaySelectedHomeConfigs(self):
        ttk.Label(self,text="Phase Compensation :").grid(row=3,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["PC"]).grid(row=3,column=2,sticky="E")
        ttk.Label(self,text="Number of Layers :").grid(row=4,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["NumofLayer"]).grid(row=4,column=2,sticky="E")
        ttk.Label(self,text="eAxCid :").grid(row=5,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["eAxCid"]).grid(row=5,column=2,sticky="E")
        ttk.Label(self,text="Band Width :").grid(row=6,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["Band Width"]).grid(row=6,column=2,sticky="E")
        ttk.Label(self,text="UL FRC Modulation :").grid(row=7,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["UL_FRCs"]).grid(row=7,column=2,sticky="E")
        ttk.Label(self,text="DL TM Modulation :").grid(row=8,column=1,sticky="W")
        ttk.Label(self,text=self.BasicAppConfigs["DL_TMs"]).grid(row=8,column=2,sticky="E")        

            
def main():
    #Setup Tk()
    global window
    global HomeAppConfigs
    global is_SavePressedHme
    global Test_Conf
    global Test_Func
    global Test_RCT
    global Test_Basic
    
    window = Tk()
    window.title("CU Plane Automation Suit")
    window_width = 1000
    window_height = 600
    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    # set the position of the window to the center of the screen
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    Mysky = "#DCF0F2"
    Myyellow = "#F2C84B"
    MyDeep = "deep sky blue"
    style = ttk.Style(window)
    style.theme_create( "dummy", parent="alt", settings={
        "TFrame": {"configure": {"background": Mysky} },
        "TLabel" : {"configure": {"background": Mysky, "font" : ('URW Gothic L', '10', 'bold')} },
        "TRadiobutton" : {"configure": {"background": Mysky, "font" : ('Noto Sans CJK SC', '9')} },
        "TCheckbutton" : {"configure": {"background": Mysky, "font" : ('Noto Sans CJK SC', '9')} },
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": MyDeep } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": Myyellow,"font" : ('FreeSerif', '12', 'bold') },
            "map":       {"background": [("selected", Mysky)],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )
    style.theme_use("dummy")
   
    #Setup the notebook (tabs)
    notebook = ttk.Notebook(window)
    frame0 = ttk.Frame(notebook)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)
    frame4 = ttk.Frame(notebook)
    notebook.add(frame0, text="Home")
    notebook.add(frame1, text="Conformance")
    notebook.add(frame2, text="Functional")
    notebook.add(frame3, text="RCT")
    notebook.add(frame4, text="Basic")
    notebook.grid()
    notebook.pack(expand = 1, fill ="both")

    #Create tab frames
    Home_Conf = HomeApp(master=frame0)
    Home_Conf.grid()
    Test_Conf = ConformanceApp(master=frame1)
    Test_Conf.grid()
    Test_Func = FunctionalApp(master=frame2)
    Test_Func.grid()
    Test_RCT = RCTApp(master=frame3)
    Test_RCT.grid()
    Test_Basic = BasicApp(master=frame4)
    Test_Basic.grid()


    #Main loop
    window.mainloop()

if __name__ == '__main__':
    main()
