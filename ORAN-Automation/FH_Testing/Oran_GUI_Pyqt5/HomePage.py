########################################################################
## IMPORTS
########################################################################
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QWidget, QLabel
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton,QHBoxLayout,QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont
import sys, time, shutil
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
from Oran_GUI_Pyqt5.HomePage_TDD import Ui_CU_TDD_HomePage
from Oran_GUI_Pyqt5.WriteData import WriteData

###############################################################################
## For reading data from .ini file
###############################################################################
configur = ConfigParser()
try:
    configur.read('{}/Requirement/input.ini'.format(dir_path))
except Exception as e:
    print(e)
########################################################################
## MAIN WINDOW CLASS
########################################################################

class MainWindow_tdd(QtWidgets.QMainWindow):
    def __init__(self,dir_name=dir_path):
        QtWidgets.QMainWindow.__init__(self)
        self.ui_cu = Ui_CU_TDD_HomePage()
        self.ui_cu.setupUi(self)
        self.ui_cu.runBtn.clicked.connect(lambda : self.run_module(self.ui_cu.console))
        self.ui_cu.submitBtn.clicked.connect(self.submit_data)
        self.ui_cu.savebtn.clicked.connect(self.save_input_file)
        self.ui_cu.uploadbtn.clicked.connect(self.upload_saved_configuration)
        self.ui_cu.pdfBtn.clicked.connect(self.openSaveDialog)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('PopUp')
        self.msg.resize(1133,100)
        self.showMaximized()

    def submit_data(self):
        input_data = {}
        for key, val in self.ui_cu.gethered_info.items():
            if type(val) == QtWidgets.QLineEdit:
                if 'Power_limit' in key.text() and len(val.text().strip())!=0 and val.text().isdigit():
                    input_data['_'.join(key.text().split(':')[0].split())] = '{0} {1}'.format(int(val.text())-1.5,int(val.text())+1.5)
                    print(key.text(), '{0} {1}'.format(int(val.text())-1.5,int(val.text())+1.5))
                elif 'Externaldelaytime' in key.text() and len(val.text().strip())!=0:
                    if 'ns' in val.text():
                        input_data['_'.join(key.text().split(':')[0].split())] = format((float(val.text()[:-2])*(10**(-9))),'.9f')
                        print(key.text(), int(val.text()[:-2])*(10**(-9)))
                    elif 'ms' in val.text():
                        input_data['_'.join(key.text().split(':')[0].split())] = format((float(val.text()[:-2])*(10**(-3))),'.3f')
                        print(key.text(), int(val.text()[:-2])*(10**(-3)))
                elif len(val.text().strip())!=0:
                    input_data['_'.join(key.text().split(':')[0].split())] = val.text()
                    print(key.text(), val.text())
                else:
                    self.msg.setText('Please Enter a valid value of {}'.format(key.text().split(':')[0]))
                    self.msg.exec_()
                    return False
            elif type(val) == QtWidgets.QComboBox:
                input_data['_'.join(key.text().split(':')[0].split())] = val.currentText()
                print(key.text(), val.currentText()) 
        WriteData(input_data,'{}/Requirement/input.ini'.format(dir_path))
        self.msg.setText('Data appended successfully..')
        self.msg.exec_()
        return True

    def message(self, s):
        self.ui_cu.console.append(s)

    def wrtdata(self):
        print('abschjfjgdhsj')
        test_cases = []
        for data in self.ui_cu.TestCaseData:
            test_cases.append(data[0])
        # lines = ['TestCaseData']
        print(test_cases)
        with open('{}/Requirement/TestCases.txt'.format(dir_path), 'w') as f:
            f.writelines('\n'.join(test_cases))    

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
            print(self.ui_cu.TestCaseData)
            self.wrtdata()

            # print(self.ui_cu.result_test_case)
            self.p = None
            self.console = console
            self.console.clear()
            if self.p == None:
                self.message("Executing process")
                self.ui_cu.console.append('+'*100)
                self.p = QtCore.QProcess()
                self.result = self.p.start("python", ["{}/TDD/TDD_Config_backup.py".format(dir_path)])
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.ui_cu.stopBtn.clicked.connect(self.p.kill)
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
        self.ui_cu.runBtn.setEnabled(False)
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
        for test_case in self.ui_cu.TestCaseData:
            test_case[1] = 'Completed'
            self.ui_cu.result_test_case()
        # self.stopAni()
        self.ui_cu.runBtn.setEnabled(True)
        self.p = None
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('PopUp')
        msg.resize(400,100)
        ### Test CASE COMPLETED
        # msg.setText('Logs are saved at {}.'.format('/home/vvdn/Music/ORAN_AUTOMATION1/Oran_GUI_Pyqt5/'))
        msg.setText('{}.'.format('TEST CASE COMPLETED, REPORT ARE SAVED AT {}/TDD/Results'.format(dir_path)))
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

    def openSaveDialog(self):
        option=QFileDialog.Options()
        #####################################################################
        # Append PDF file path here
        #####################################################################
        file_path = '{}/TDD/Results'.format(dir_path)
        option =QFileDialog.DontUseNativeDialog
        # l = 'hello world'
        file=QFileDialog.getSaveFileName(self.ui_cu.RunBtnFrame,"Save File Window Title","defualt","All Files (*)",options=option)
        print(file[0])
        try:
            shutil.copytree(file_path, file[0])
        except Exception as e:
            print(e)

    ####################### save input ########################
    def save_input_file(self):
        option=QFileDialog.Options()
        #####################################################################
        # Append PDF file path here
        #####################################################################
        option =QFileDialog.DontUseNativeDialog
        file=QFileDialog.getSaveFileName(self.ui_cu.RunBtnFrame,"Save File Window Title","defualt.ini","All Files (*)",options=option)
        self.submit_data()
        file_path = '{}/Requirement/input.ini'.format(dir_path)
        print(file[0])
        try:
            shutil.copyfile(file_path, file[0])
        except Exception as e:
            print(e)

    def upload_saved_configuration(self):
        try:
            name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            print(name[0])
            filenames = open(f"{name[0]}","r+")
            with filenames:
                text = filenames.read()
                data = text.split('\n')
                data.pop(0)
                for val1, val2 in zip(self.ui_cu.gethered_info.items(),data):
                    if type(val1[1]) == QtWidgets.QComboBox:
                        print(val2, val1[0].text(),val1[1].currentText())
                        val1[1].setCurrentText(val2.split('= ')[1])
                    else:
                        print(val2, val1[0].text(),val1[1].text())
                        val1[1].setText(val2.split('= ')[1])
        except Exception as e:
            print(e)


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_tdd()
    sys.exit(app.exec_())