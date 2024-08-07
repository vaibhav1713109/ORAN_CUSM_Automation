# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Home_Page.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import resource
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton,QHBoxLayout,QFileDialog
import os
directory_path = os.path.dirname(__file__)
# directory_path = os.path.dirname(directory_path)
print(directory_path)
import shutil


class Ui_CU_TDD_HomePage(object):
    def setupUi(self, MainWindow):
        self.TestCaseData = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(665, 494)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            """*{
                    color:black;
                    border:none;
                }
                #TestWindow{
                    max-height:300px;
                }
                #TestPlanF{
                    max-width:300px	;
                }
                #ExecutionWIndow{
                    min-height:200px;
                }
                #dlTestFrame, #ulTestFrame{
                    border-left: 1px solid black;
                    /* border-bottom: 1px solid black; */
                    border-radius:2px;
                }
                #RunBtnFrame,#BasicConfContents,#Added_TC,#AllTestContents{
                    background-color:rgb(186, 189, 182);
                    }
                #centralwidget{
                    background-color:rgb(255, 255, 255);
                }
                #TestCaseLabel,#RunCases,#confLabel,#executionLable{
                    background-color: qlineargradient(spread:pad, x1:0.483025, y1:0.256, x2:0.522388, y2:1, stop:0 rgba(4, 108, 124, 255), stop:1 rgba(165, 156, 191, 255));
                }
                #TestPlanF, #Configuration,#RuningCase, #ExecFrame
                { 
                    background-color: rgb(211, 215, 207);
                }
                #sapratedLine{
                    background-color: rgb(0, 0, 0);
                }
                QComboBox,QLineEdit{
                    border-bottom: 1px solid black;
                    border-radius:2px;
                    background-color:rgb(186, 189, 182);
                }
                
                #runBtn, #pdfBtn, #submitBtn, #addbtn{
                    background-color: #04AA6D;
                }
                QPushButton{
                    padding:1px;
                    border-radius:4px;
                }
                #downlinkLabel, #uplinkLabel{
                    background-color: rgb(211, 215, 207);
                    border-radius:5px;
                    padding-left:2px;  
                }
            """
        )
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TestWindow = QtWidgets.QFrame(self.centralwidget)
        self.TestWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TestWindow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TestWindow.setObjectName("TestWindow")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.TestWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TestPlanF = QtWidgets.QFrame(self.TestWindow)
        self.TestPlanF.setStyleSheet("")
        self.TestPlanF.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TestPlanF.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TestPlanF.setObjectName("TestPlanF")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.TestPlanF)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TestCaseLabel = QtWidgets.QLabel(self.TestPlanF)
        self.TestCaseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TestCaseLabel.setObjectName("TestCaseLabel")
        self.verticalLayout_2.addWidget(
            self.TestCaseLabel, 0, QtCore.Qt.AlignTop)
        self.AllTest = QtWidgets.QScrollArea(self.TestPlanF)
        self.AllTest.setWidgetResizable(True)
        self.AllTest.setObjectName("AllTest")
        self.AllTestContents = QtWidgets.QWidget()
        self.AllTestContents.setGeometry(QtCore.QRect(0, -65, 163, 272))
        self.AllTestContents.setObjectName("AllTestContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.AllTestContents)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # DL test Cases
        self.DL_testCases = [
                             'Base_DL','Base_UL', 'Extended_DL','Extended_UL', '16_QAM_Comp_16_bit_DL','16_QAM_Comp_16_bit_UL',
                             '64_QAM_Comp_16_bit_DL','64_QAM_Comp_16_bit_UL', '256_QAM_DL_Comp_16_bit', 
                             '16_QAM_Comp_9_bit_DL', '16_QAM_Comp_9_bit_UL','64_QAM_Comp_9_bit_DL', '64_QAM_Comp_9_bit_UL',
                             '256_QAM_DL_Comp_9_bit', '16_QAM_Comp_12_bit_DL', '16_QAM_Comp_12_bit_UL','64_QAM_Comp_12_bit_DL', 
                             '64_QAM_Comp_12_bit_UL', '256_QAM_DL_Comp_12_bit', '16_QAM_Comp_14_bit_DL', '16_QAM_Comp_14_bit_UL',
                             '64_QAM_Comp_14_bit_DL', '64_QAM_Comp_14_bit_UL', '256_QAM_DL_Comp_14_bit', 'No_Beamforming_DL', 
                             'No_Beamforming_UL','ST3_PRACH_A3','ST3_PRACH_B4','ST3_PRACH_C2 '
                             ]

        self.downlinkLabel = QtWidgets.QLabel(self.AllTestContents)
        self.downlinkLabel.setObjectName("downlinkLabel")
        self.verticalLayout_6.addWidget(self.downlinkLabel)
        self.dlTestFrame = QtWidgets.QFrame(self.AllTestContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dlTestFrame.sizePolicy().hasHeightForWidth())
        self.dlTestFrame.setSizePolicy(sizePolicy)
        self.dlTestFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dlTestFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dlTestFrame.setObjectName("dlTestFrame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.dlTestFrame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        # Make DL test Cases Check Box
        self.Dl_checkboxes = []
        for tc in self.DL_testCases:
            self.dl_testCase = QtWidgets.QCheckBox(self.dlTestFrame)
            self.dl_testCase.setObjectName(tc)
            self.dl_testCase.setText(tc)
            self.verticalLayout_7.addWidget(self.dl_testCase)
            self.Dl_checkboxes.append(self.dl_testCase)
        self.Dl_selectAll = QtWidgets.QCheckBox(self.dlTestFrame)
        self.Dl_selectAll.setObjectName("Dl_selectAll")
        self.verticalLayout_7.addWidget(self.Dl_selectAll)
        self.verticalLayout_6.addWidget(self.dlTestFrame)

        # after clicking on select all button in Downlink Frame
        self.Dl_selectAll.clicked.connect(self.checked_all_dl)

        # UL test Cases
        # self.UL_testCases = ['Uplink Base', 'Uplink Extended',
        #                      'Uplink No Compresssion', 'Uplink 9 Bit', 'Uplink 12 Bit', 'Uplink 14 bit']
        # self.uplinkLabel = QtWidgets.QLabel(self.AllTestContents)
        # self.uplinkLabel.setObjectName("uplinkLabel")
        # self.verticalLayout_6.addWidget(self.uplinkLabel)
        self.ulTestFrame = QtWidgets.QFrame(self.AllTestContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ulTestFrame.sizePolicy().hasHeightForWidth())
        self.ulTestFrame.setSizePolicy(sizePolicy)
        self.ulTestFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ulTestFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ulTestFrame.setObjectName("ulTestFrame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.ulTestFrame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        # Make UL test Cases Check Box
        # self.ul_CheckBoxes = []
        # for ul_tc in self.UL_testCases:
        #     self.ul_TetsCase = ul_tc
        #     self.ul_TetsCase = QtWidgets.QCheckBox(self.ulTestFrame)
        #     self.ul_TetsCase.setObjectName(ul_tc)
        #     self.ul_TetsCase.setText(ul_tc)
        #     # print(self.ul_TetsCase.checkState())
        #     self.verticalLayout_8.addWidget(self.ul_TetsCase)
        #     self.ul_CheckBoxes.append(self.ul_TetsCase)
        # self.ul_SelectAll = QtWidgets.QCheckBox(self.ulTestFrame)
        # self.ul_SelectAll.setObjectName("ul_SelectAll")
        # self.verticalLayout_8.addWidget(self.ul_SelectAll)
        # self.verticalLayout_6.addWidget(self.ulTestFrame)

        # # after clicking on select all button in Uplink Frame
        # self.ul_SelectAll.clicked.connect(self.checked_all_ul)

        self.AllTest.setWidget(self.AllTestContents)
        self.verticalLayout_2.addWidget(self.AllTest)
        self.addbtn = QtWidgets.QPushButton(self.TestPlanF)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/plus-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addbtn.setIcon(icon)
        self.addbtn.setIconSize(QtCore.QSize(16, 16))
        self.addbtn.setObjectName("addbtn")
        self.addbtn.setText("Add")
        self.verticalLayout_2.addWidget(self.addbtn, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addWidget(self.TestPlanF)
        self.RuningCase = QtWidgets.QFrame(self.TestWindow)
        self.RuningCase.setStyleSheet("")
        self.RuningCase.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RuningCase.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RuningCase.setObjectName("RuningCase")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.RuningCase)
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.RunCases = QtWidgets.QLabel(self.RuningCase)
        self.RunCases.setAlignment(QtCore.Qt.AlignCenter)
        self.RunCases.setObjectName("RunCases")
        self.verticalLayout_3.addWidget(self.RunCases, 0, QtCore.Qt.AlignTop)

        ## After pressing add button
        self.addbtn.clicked.connect(self.added_case)

        # Run Button Frame
        self.RunBtnFrame = QtWidgets.QFrame(self.RuningCase)
        self.RunBtnFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RunBtnFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RunBtnFrame.setObjectName("RunBtnFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.RunBtnFrame)
        self.horizontalLayout_2.setContentsMargins(6, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Run Button-------------------------------------------
        self.runBtn = QtWidgets.QPushButton(self.RunBtnFrame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.runBtn.setIcon(icon)
        self.runBtn.setIconSize(QtCore.QSize(18, 18))
        self.runBtn.setObjectName("runBtn")
        self.runBtn.setText('RUN')
        self.horizontalLayout_2.addWidget(self.runBtn, 0, QtCore.Qt.AlignLeft)

        self.stopBtn = QtWidgets.QPushButton(self.RunBtnFrame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/stop-circle.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopBtn.setIcon(icon)
        self.stopBtn.setIconSize(QtCore.QSize(18, 18))
        self.stopBtn.setObjectName("runBtn")
        self.stopBtn.setText('STOP')
        self.horizontalLayout_2.addWidget(self.stopBtn, 0, QtCore.Qt.AlignLeft)

        # Save PDF-------------------------------------------
        self.pdfBtn = QtWidgets.QPushButton(self.RunBtnFrame)
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"),
        #                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pdfBtn.setIcon(icon)
        self.pdfBtn.setIconSize(QtCore.QSize(20, 20))
        self.pdfBtn.setObjectName("pdfBtn")
        # self.pdfBtn.clicked.connect(self.openSaveDialog)
        self.pdfBtn.setText('Save PDF')
        self.horizontalLayout_2.addWidget(self.pdfBtn, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_3.addWidget(self.RunBtnFrame)

    # def openSaveDialog(self):
    #     option=QFileDialog.Options()
    #     #####################################################################
    #     # Append PDF file path here
    #     #####################################################################
    #     file_path = r'{}\Downlink\pdf\Result123.pdf'.format(directory_path)
    #     option =QFileDialog.DontUseNativeDialog
    #     # l = 'hello world'
    #     file=QFileDialog.getSaveFileName(self.frame_3,"Save File Window Title","defualt.pdf","All Files (*)",options=option)
    #     print(file[0])
    #     shutil.copyfile(file_path, file[0])

        

        
        ########### Added Test Cases #############

        # list_of_tc = {'tc1': ('pass', str(4.6)), 'tc2': ('fail', str(3.7)), 'tc3': ('pass', str(5.8)),
        #               'tc4': ('pass', str(4.6)), 'tc7': ('fail', str(3.7)), 'tc10': ('pass', str(5.8)),
        #               'tc5': ('pass', str(4.6)), 'tc8': ('fail', str(3.7)), 'tc11': ('pass', str(5.8)),
        #               'tc6': ('pass', str(4.6)), 'tc9': ('fail', str(3.7)), 'tc12': ('pass', str(5.8))}
        list_of_tc = {}
        i = 1
        self.Added_TC = QtWidgets.QTableWidget(self.RuningCase)
        self.Added_TC.setShowGrid(True)
        self.Added_TC.setGridStyle(QtCore.Qt.SolidLine)
        self.Added_TC.setWordWrap(True)
        self.Added_TC.setRowCount(0)
        self.Added_TC.setObjectName("Added_TC")
        self.Added_TC.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.Added_TC.setHorizontalHeaderItem(0, item)
        item.setText('Name')
        item = QtWidgets.QTableWidgetItem()
        self.Added_TC.setHorizontalHeaderItem(1, item)
        item.setText('Status')
        item = QtWidgets.QTableWidgetItem()
        self.Added_TC.setHorizontalHeaderItem(2, item)
        item.setText('Duration')
        self.Added_TC.horizontalHeader().setCascadingSectionResizes(False)
        self.Added_TC.horizontalHeader().setSortIndicatorShown(False)
        self.Added_TC.horizontalHeader().setStretchLastSection(True)
        self.Added_TC.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_3.addWidget(self.Added_TC)
        self.horizontalLayout.addWidget(self.RuningCase)

        # Test Configuration Window---------------------------------------
        self.Configuration = QtWidgets.QFrame(self.TestWindow)
        self.Configuration.setStyleSheet("")
        self.Configuration.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Configuration.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Configuration.setObjectName("Configuration")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Configuration)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.confLabel = QtWidgets.QLabel(self.Configuration)
        self.confLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.confLabel.setObjectName("confLabel")
        self.verticalLayout_3.addWidget(self.confLabel, 0, QtCore.Qt.AlignTop)
        self.BasicConf = QtWidgets.QScrollArea(self.Configuration)
        self.BasicConf.setWidgetResizable(True)
        self.BasicConf.setObjectName("BasicConf")
        self.BasicConfContents = QtWidgets.QWidget()
        self.BasicConfContents.setGeometry(QtCore.QRect(-73, -107, 247, 300))
        self.BasicConfContents.setObjectName("BasicConfContents")
        self.formLayout = QtWidgets.QFormLayout(self.BasicConfContents)
        self.formLayout.setObjectName("formLayout")

        # User Inputs
        scsvalues = ('15KHz', '30KHz', '60KHz', '120KHz', '240KHz')
        bandwidths = ('10M', '20M', '30M', '40M', '50M',
                      '60M', '70M', '80M', '100M')
        phase_comps = ('Off', 'On')
        required_info = {'SubCarrier Spacing :': scsvalues, 'Center Frequency :': 'GHz(Eg. 3.6250)',
                         'External Gain :': 'dBm(Eg. 22.3)', 'Bandwidth': bandwidths, 'RU_Mac':'98:ae:71:01:91:91',
                        #  'Phase Compensation :': phase_comps, 
                         'VXT Address :': 'TCPIP0::172.17.95.2::inst0::INSTR','Eaxcid :': 'Space saprated Channel No.',
                         'Amplitude :': '60','Externaldelaytime :' :'Eg. 5ns/5ms', 
                         'Clgc_gain_calculation_time :':'10','EVM_limit :':'2.5','Power_limit :':'25', 
                         'Downlink Timing': None, 'DL C-Plane Timing :': '500000', 'DL U-Plane Timing :': '375000',
                         'Uplink Timing :': None, 'UL C-Plane Time(T1a_cp_ul) :':'5000',
                         'UL U-Plane Time Delay(Ta3_up_ul) :':'2000'}

        self.gethered_info = {}
        i = 1
        for key, val in required_info.items():
            if type(val) == tuple:
                self.formLabel = QtWidgets.QLabel(self.BasicConfContents)
                self.formLabel.setObjectName(key)
                self.formLabel.setText(key)
                self.formLayout.setWidget(
                    i, QtWidgets.QFormLayout.LabelRole, self.formLabel)
                self.formDropdownInput = QtWidgets.QComboBox(
                    self.BasicConfContents)
                self.formDropdownInput.setObjectName(key)
                self.formDropdownInput.addItems(val)
                self.formLayout.setWidget(
                    i, QtWidgets.QFormLayout.FieldRole, self.formDropdownInput)
                self.gethered_info[self.formLabel] = self.formDropdownInput
            elif val == None:
                self.labelHeading = QtWidgets.QLabel(self.BasicConfContents)
                self.labelHeading.setAlignment(QtCore.Qt.AlignCenter)
                self.labelHeading.setObjectName(key)
                self.labelHeading.setText(key)
                self.formLayout.setWidget(
                    i, QtWidgets.QFormLayout.SpanningRole, self.labelHeading)
                self.sapratedLine = QtWidgets.QFrame(self.BasicConfContents)
                self.sapratedLine.setMinimumSize(QtCore.QSize(0, 1))
                self.sapratedLine.setFrameShape(QtWidgets.QFrame.HLine)
                self.sapratedLine.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.sapratedLine.setObjectName("sapratedLine")
                self.formLayout.setWidget(
                    i+1, QtWidgets.QFormLayout.SpanningRole, self.sapratedLine)
                i += 1
            # elif val == '':
            #     self.formLabel = QtWidgets.QLabel(self.BasicConfContents)
            #     self.formLabel.setObjectName(key)
            #     self.formLabel.setText(key)
            #     self.formLayout.setWidget(
            #         i, QtWidgets.QFormLayout.LabelRole, self.formLabel)
            #     self.formInput = QtWidgets.QLabel(self.BasicConfContents)
            #     self.formInput.setObjectName(key)
            #     value = int(required_info['DL C-Plane Timing :'])- int(required_info['DL U-Plane Timing :'])
            #     self.formInput.setText(str(value))
            #     self.formInput.setStyleSheet("""
            #         border-radius:2px;
            #         border-bottom:1px solid black;
            #     """)
            #     self.formLayout.setWidget(
            #         i, QtWidgets.QFormLayout.FieldRole, self.formInput)
            #     self.gethered_info[self.formLabel] = self.formInput
            else:
                self.formLabel = QtWidgets.QLabel(self.BasicConfContents)
                self.formLabel.setObjectName(key)
                self.formLabel.setText(key)
                self.formLayout.setWidget(
                    i, QtWidgets.QFormLayout.LabelRole, self.formLabel)
                self.formInput = QtWidgets.QLineEdit(self.BasicConfContents)
                self.formInput.setObjectName(key)
                self.formInput.setPlaceholderText(val)
                self.formLayout.setWidget(
                    i, QtWidgets.QFormLayout.FieldRole, self.formInput)
                self.gethered_info[self.formLabel] = self.formInput
                pass
            i += 1
        # print(gethered_info)
        self.BasicConf.setWidget(self.BasicConfContents)
        self.verticalLayout_3.addWidget(self.BasicConf)

        # Submit Button -------------------------------------------
        self.submitBtn = QtWidgets.QPushButton(self.Configuration)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/zap.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.submitBtn.setIcon(icon1)
        self.submitBtn.setIconSize(QtCore.QSize(18, 18))
        self.submitBtn.setObjectName("submitBtn")
        self.submitBtn.setText('Submit')
        self.verticalLayout_3.addWidget(
            self.submitBtn, 0, QtCore.Qt.AlignHCenter)



         




        self.horizontalLayout.addWidget(self.Configuration)
        self.verticalLayout.addWidget(self.TestWindow)
        self.ExecutionWIndow = QtWidgets.QFrame(self.centralwidget)
        self.ExecutionWIndow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ExecutionWIndow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ExecutionWIndow.setObjectName("ExecutionWIndow")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ExecutionWIndow)
        self.verticalLayout_5.setContentsMargins(9, 0, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.executionLable = QtWidgets.QLabel(self.ExecutionWIndow)
        self.executionLable.setAlignment(QtCore.Qt.AlignCenter)
        self.executionLable.setObjectName("executionLable")
        self.verticalLayout_5.addWidget(
            self.executionLable, 0, QtCore.Qt.AlignTop)
        self.ExecFrame = QtWidgets.QFrame(self.ExecutionWIndow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ExecFrame.sizePolicy().hasHeightForWidth())
        self.ExecFrame.setSizePolicy(sizePolicy)
        self.ExecFrame.setStyleSheet("")
        self.ExecFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ExecFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ExecFrame.setObjectName("ExecFrame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.ExecFrame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.console = QtWidgets.QPlainTextEdit(self.ExecFrame)
        self.console.setObjectName("textBrowser")
        self.verticalLayout_9.addWidget(self.console)
        self.verticalLayout_5.addWidget(self.ExecFrame)
        self.verticalLayout.addWidget(self.ExecutionWIndow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Test Automation Suit"))
        self.TestCaseLabel.setText(_translate("MainWindow", "Test Case"))
        self.downlinkLabel.setText(_translate("MainWindow", "Downlink/Uplink"))
        self.Dl_selectAll.setText(_translate("MainWindow", "Select All"))
        # self.uplinkLabel.setText(_translate("MainWindow", "Uplink"))
        # self.ul_SelectAll.setText(_translate("MainWindow", "Select_All"))
        self.RunCases.setText(_translate("MainWindow", "Runing Test Case"))
        self.confLabel.setText(_translate("MainWindow", "Configuration"))
        self.executionLable.setText(_translate("MainWindow", "Execution"))


    def checked_all_dl(self,state):
        for check in self.Dl_checkboxes:
            if state:
                state = 2
                self.TestCaseData.append([check.text(),'Selected', '--'])
                check.setCheckState(state)	
            else:
                state = 0
                check.setCheckState(state)	
        # print(self.TestCaseData)
        pass

    def checked_all_ul(self, state):
        for check in self.ul_CheckBoxes:
            if state:
                state = 2
                self.TestCaseData.append([check.text(),'Selected', '--'])
                check.setCheckState(state)	
            else:
                state = 0
                check.setCheckState(state)	
        # print(self.TestCaseData)
        pass

    def checked_mul(self):
        self.TestCaseData = []
        self.checkboxes = self.Dl_checkboxes
        for check in self.checkboxes:
            if check.isChecked():
                self.TestCaseData.append([check.text(),'Selected', '--'])
            else:
                pass
        # print(self.TestCaseData)
    
    def added_case(self):
        self.checked_mul()
        row = 0
        self.Added_TC.setRowCount(len(self.TestCaseData))
        for data in self.TestCaseData:
            self.Added_TC.setItem(row,0,QtWidgets.QTableWidgetItem(data[0]))
            self.Added_TC.setItem(row,1,QtWidgets.QTableWidgetItem(data[1]))
            self.Added_TC.setItem(row,2,QtWidgets.QTableWidgetItem(data[2]))
            row+=1

    def result_test_case(self):
        row = 0
        self.Added_TC.setRowCount(len(self.TestCaseData))
        for data in self.TestCaseData:
            self.Added_TC.setItem(row,0,QtWidgets.QTableWidgetItem(data[0]))
            self.Added_TC.setItem(row,1,QtWidgets.QTableWidgetItem(data[1]))
            self.Added_TC.setItem(row,2,QtWidgets.QTableWidgetItem(data[2]))
            row+=1
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_CU_TDD_HomePage()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())