# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\controlDevice.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(981, 697)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.GrpBoxSettings = QtWidgets.QGroupBox(self.centralwidget)
        self.GrpBoxSettings.setGeometry(QtCore.QRect(700, 10, 261, 551))
        self.GrpBoxSettings.setObjectName("GrpBoxSettings")
        self.GrpBoxDevList = QtWidgets.QGroupBox(self.centralwidget)
        self.GrpBoxDevList.setGeometry(QtCore.QRect(300, 10, 391, 551))
        self.GrpBoxDevList.setObjectName("GrpBoxDevList")
        self.LstViewDevices = QtWidgets.QListWidget(self.GrpBoxDevList)
        self.LstViewDevices.setGeometry(QtCore.QRect(30, 30, 351, 511))
        self.LstViewDevices.setObjectName("LstViewDevices")
        self.PushBtnClose = QtWidgets.QPushButton(self.centralwidget)
        self.PushBtnClose.setGeometry(QtCore.QRect(880, 620, 75, 23))
        self.PushBtnClose.setObjectName("PushBtnClose")
        self.GrpBoxLastCommands = QtWidgets.QGroupBox(self.centralwidget)
        self.GrpBoxLastCommands.setGeometry(QtCore.QRect(10, 190, 281, 371))
        self.GrpBoxLastCommands.setObjectName("GrpBoxLastCommands")
        self.LstViewLastCommands = QtWidgets.QListView(self.GrpBoxLastCommands)
        self.LstViewLastCommands.setGeometry(QtCore.QRect(10, 20, 261, 341))
        self.LstViewLastCommands.setObjectName("LstViewLastCommands")
        self.TxtEditCommand = QtWidgets.QTextEdit(self.centralwidget)
        self.TxtEditCommand.setGeometry(QtCore.QRect(20, 50, 261, 91))
        self.TxtEditCommand.setObjectName("TxtEditCommand")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 30, 47, 13))
        self.label.setObjectName("label")
        self.PushBtSendCommand = QtWidgets.QPushButton(self.centralwidget)
        self.PushBtSendCommand.setGeometry(QtCore.QRect(94, 160, 91, 23))
        self.PushBtSendCommand.setObjectName("PushBtSendCommand")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 981, 21))
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
        self.GrpBoxSettings.setTitle(_translate("MainWindow", "Einstellungen"))
        self.GrpBoxDevList.setTitle(_translate("MainWindow", "Geräteliste"))
        self.PushBtnClose.setText(_translate("MainWindow", "Schließen"))
        self.GrpBoxLastCommands.setTitle(_translate("MainWindow", "Letzte Befehle"))
        self.label.setText(_translate("MainWindow", "Befehl"))
        self.PushBtSendCommand.setText(_translate("MainWindow", "Befehl senden"))

