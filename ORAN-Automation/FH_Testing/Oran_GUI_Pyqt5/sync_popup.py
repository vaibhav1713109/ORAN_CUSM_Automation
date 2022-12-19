import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize


class Ui_popup_sync(QtWidgets.QMainWindow):
    
    def check_sync(self,message):
        self.setMinimumSize(QSize(1400,800))
        self.choice = QtWidgets.QMessageBox.question(self, 'Extract!',
                                            f"{message}",
                                            QtWidgets.QMessageBox.Yes |QtWidgets.QMessageBox.No)            
    
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    ui = Ui_popup_sync()
    ui.check_sync('ckdnskkjdnkkjn')        