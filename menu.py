# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 534)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 200, 91, 91))
        self.pushButton.setStyleSheet("background-color: rgb(170, 255, 0);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px; \n"
"\n"
"border-style: outset;\n"
"\n"
"\n"
"font: 15pt \"MV Boli\";")
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 100, 100, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(60)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px;  \n"
"\n"
"border-style: outset;\n"
"font: 15pt \"MV Boli\";")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(300, 290, 100, 100))
        self.pushButton_4.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_4.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px;  \n"
"border-style: outset;\n"
"font: 15pt \"MV Boli\";")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(530, 100, 100, 100))
        self.pushButton_7.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px;  \n"
"\n"
"border-style: outset;\n"
"font: 15pt \"MV Boli\";")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(530, 290, 100, 100))
        self.pushButton_8.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px;\n"
"\n"
"border-style: outset;\n"
"font: 15pt \"MV Boli\";")
        self.pushButton_8.setObjectName("pushButton_8")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(480, 190, 41, 41))
        self.label.setStyleSheet("background-color: rgb(170, 255, 0);\n"
"border-radius: 30px; ")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(480, 270, 41, 41))
        self.label_2.setStyleSheet("background-color: rgb(170, 255, 0);\n"
"border-radius: 30px; ")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 270, 41, 41))
        self.label_3.setStyleSheet("background-color: rgb(170, 255, 0);\n"
"border-radius: 30px; ")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 190, 41, 41))
        self.label_4.setStyleSheet("background-color: rgb(170, 255, 0);\n"
"border-radius: 30px; ")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_4.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.toggled['bool'].connect(self.pushButton_2.setHidden) # type: ignore
        self.pushButton.toggled['bool'].connect(self.pushButton_7.setHidden) # type: ignore
        self.pushButton.toggled['bool'].connect(self.pushButton_4.setHidden) # type: ignore
        self.pushButton.toggled['bool'].connect(self.pushButton_8.setHidden) # type: ignore
        self.pushButton.toggled['bool'].connect(self.label.show) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Menu"))
        self.pushButton_2.setText(_translate("MainWindow", "MOVE"))
        self.pushButton_4.setText(_translate("MainWindow", "CLICK"))
        self.pushButton_7.setText(_translate("MainWindow", "BBB"))
        self.pushButton_8.setText(_translate("MainWindow", "PPT"))