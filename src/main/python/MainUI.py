# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pachongui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 364)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 391, 321))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.listWidget = QtWidgets.QListWidget(self.tab_3)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 351, 241))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit.setGeometry(QtCore.QRect(10, 260, 271, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(290, 260, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 30, 161, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(300, 30, 41, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(90, 70, 161, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label = QtWidgets.QLabel(self.tab_4)
        self.label.setGeometry(QtCore.QRect(30, 30, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_4)
        self.label_2.setGeometry(QtCore.QRect(260, 30, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab_4)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_4)
        self.label_4.setGeometry(QtCore.QRect(260, 70, 41, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 70, 41, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 110, 111, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_5 = QtWidgets.QLabel(self.tab_4)
        self.label_5.setGeometry(QtCore.QRect(30, 150, 311, 20))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Chat"))
        self.label.setText(_translate("MainWindow", "Address:"))
        self.label_2.setText(_translate("MainWindow", "Port:"))
        self.label_3.setText(_translate("MainWindow", "Proxy:"))
        self.label_4.setText(_translate("MainWindow", "Port:"))
        self.pushButton_2.setText(_translate("MainWindow", "Test and Coonect"))
        self.label_5.setText(_translate("MainWindow", "No Status"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Setting"))

