# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_popup(object):
    def setupUi(self, popup):
        popup.setObjectName("popup")
        popup.resize(354, 136)
        self.centralwidget = QtWidgets.QWidget(popup)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 60, 331, 17))
        self.label.setObjectName("label")
        popup.setCentralWidget(self.centralwidget)

        self.retranslateUi(popup)
        QtCore.QMetaObject.connectSlotsByName(popup)

    def retranslateUi(self, popup):
        _translate = QtCore.QCoreApplication.translate
        popup.setWindowTitle(_translate("popup", "MainWindow"))
        self.label.setText(_translate("popup", "PLEASE ENTER CORRECT CREDENTIALS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    popup = QtWidgets.QMainWindow()
    ui = Ui_popup()
    ui.setupUi(popup)
    popup.show()
    sys.exit(app.exec_())