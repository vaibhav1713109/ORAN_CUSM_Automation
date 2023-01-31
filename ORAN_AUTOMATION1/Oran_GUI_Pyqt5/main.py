########################################################################
## IMPORTS
########################################################################
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont
import sys, time
import os
from PyQt5 import QtWidgets, QtCore, QtGui
import ipaddress, subprocess
from configparser import ConfigParser


########################################################################
# IMPORT GUI FILE
########################################################################

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir_path)
sys.path.append(dir_path)
from Oran_GUI_Pyqt5.HomePage import Ui_CU_HomePage
from WriteData import WriteData
# from GUI.run_all import Ui_Run_ALL
# from require.Write_Data import WriteData
########################################################################

###############################################################################
## For reading data from .ini file
###############################################################################
configur = ConfigParser()
try:
    configur.read('{}/Requirement/requirement.ini'.format(dir_path))
except Exception as e:
    print(e)
########################################################################
## MAIN WINDOW CLASS
########################################################################

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,dir_name=dir_path):
        QtWidgets.QMainWindow.__init__(self)
        self.ui_cu = Ui_CU_HomePage()
        self.ui_cu.setupUi(self)
        self.ui_cu.runBtn.clicked.connect(lambda : self.run_module(self.ui_cu.console))
        self.ui_cu.submitBtn.clicked.connect(self.submit_data)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('PopUp')
        self.msg.resize(1133,100)
        self.showMaximized()

    def submit_data(self):
        input_data = {}
        for key, val in self.ui_cu.gethered_info.items():
            if type(val) == QtWidgets.QLineEdit:
                if len(val.text().strip())!=0:
                    input_data['_'.join(key.text().split(':')[0].split())] = val.text()
                    print(key.text(), val.text())
                else:
                    self.msg.setText('Please Enter a valid value of {}'.format(key.text().split(':')[0]))
                    self.msg.exec_()
                    return False
            elif type(val) == QtWidgets.QComboBox:
                input_data['_'.join(key.text().split(':')[0].split())] = val.currentText()
                print(key.text(), val.currentText())
        input_data['C-Plane_Time(Tcp_adv_dl)'] = str(int(input_data['DL_C-Plane_Timing']) - int(input_data['DL_U-Plane_Timing']))
        WriteData(input_data,'{}/Requirement/requirement.ini'.format(dir_path))
        self.msg.setText('Data appended successfully..')
        self.msg.exec_()
        return True

    def message(self, s):
        self.ui_cu.console.append(s)

    def run_module(self,console):
        if len(self.ui_cu.TestCaseData) == 0:
            self.msg.setText('Please add atleast one test case!!')
            self.msg.exec_()
            return False
        else:
        # if submitbtn():
        # content = self.comboBox.currentText()
            for test_case in self.ui_cu.TestCaseData:
                test_case[1] = 'In Progress!!'
                self.ui_cu.result_test_case()
            self.p = None
            self.console = console
            self.console.clear()
            if self.p == None:
                self.message("Executing process")
                self.console.append('+'*100)
                self.p = QtCore.QProcess()
                self.result = self.p.start("python", ["{}/Script/Main_Script.py".format(dir_path)])
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.stateChanged.connect(self.handle_state)
                self.p.finished.connect(self.process_finished)  # Clean up once complete.

        
        # else:
        #     return False
            
    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)
        pass

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)
        # self.message(self.result)

    def handle_state(self, state):
        states = {
            QtCore.QProcess.NotRunning: 'Not running',
            QtCore.QProcess.Starting: 'Starting',
            QtCore.QProcess.Running: 'Running',
        }
        # print(state,'state')
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        # self.stopAni()
        self.p = None
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('PopUp')
        msg.resize(400,100)
        msg.setText('Logs are saved at {}.'.format('/home/vvdn/Music/ORAN_AUTOMATION1/Oran_GUI_Pyqt5/'))
        msg.exec_()

    def Loading(self,checkboxes,console,submitbtn):
        self.main_win = QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_win)
        
        self.main_win.setFixedSize(200,200)
        self.label_ani= QLabel(self.main_win)
        self.movie=QMovie("{}/GUI/Loading_1.gif".format(dir_path))
        self.label_ani.setMovie(self.movie)
        self.verticalLayout.addWidget(self.label_ani, 0, QtCore.Qt.AlignHCenter)
        self.main_win.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.main_win.setAttribute(QtCore.Qt.WA_TranslucentBackground,on=True)
        self.startani()
        self.main_win.showMaximized()
        self.timer= QTimer(self.main_win)
        # self.timer.singleShot(1000,self.stopAni)
        self.timer.singleShot(100,lambda: self.checked(checkboxes,console,submitbtn))

    def startani(self):
        self.movie.start()
        # self.start_process()
        
    def stopAni(self):
        self.movie.stop()
        self.main_win.close()


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())