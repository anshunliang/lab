# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 's1.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 140, 72, 15))
        self.label.setObjectName("label")
        self.TX = QtWidgets.QPushButton(Dialog)
        self.TX.setGeometry(QtCore.QRect(180, 210, 89, 28))
        self.TX.setObjectName("TX")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "hello"))
        self.TX.setText(_translate("Dialog", "prt"))
    
    