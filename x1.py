# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'x1.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TX11 = QtWidgets.QPushButton(self.centralwidget)
        self.TX11.setGeometry(QtCore.QRect(160, 490, 89, 28))
        self.TX11.setObjectName("TX11")
        self.tx22 = QtWidgets.QPushButton(self.centralwidget)
        self.tx22.setGeometry(QtCore.QRect(310, 490, 89, 28))
        self.tx22.setObjectName("tx22")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TX11.setText(_translate("MainWindow", "通讯"))
        self.tx22.setText(_translate("MainWindow", "配置表"))
