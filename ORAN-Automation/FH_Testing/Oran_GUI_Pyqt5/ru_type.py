from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys,os
from HomePage import MainWindow_tdd
# from popup import Ui_popup
dir_name = os.path.dirname(os.path.abspath(__file__))


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('{}/Page.ui'.format(dir_name), self)
        self.tdd_pushButton = self.findChild(QtWidgets.QPushButton, 'tdd_pushButton')
        self.fdd_pushButton = self.findChild(QtWidgets.QPushButton, 'fdd_pushButton_2')
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        self.tdd_pushButton.setGraphicsEffect(shadow)
        self.tdd_pushButton.clicked.connect(self.openWindow_tdd)
        # self.fdd_pushButton.clicked.connect(self.openWindow_fdd)
        self.showMaximized()

    def openWindow_tdd(self):
        # file1 = open("{}/myfile.ini".format(dir_name), "w")
        self.window = QtWidgets.QMainWindow()
        self.ui = MainWindow_tdd()
        print(self.tdd_pushButton.text())
        window.hide()

    def openWindow_fdd(self):
        # file1 = open("{}/myfile.ini".format(dir_name), "w")
        self.window = QtWidgets.QMainWindow()
        self.ui = MainWindow_tdd()
        window.hide()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application
