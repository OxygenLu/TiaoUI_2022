from Log import Ui_logWindow
from Lu import Ui_initWindow
from interface import Window
from process import Identify
from client import Client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import time
from app import App

progressBarValue = 3


class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_initWindow() #Ui类实例化()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.appProgress)
        self.timer.start(20)
        self.ui.begin.clicked.connect(self.Begin)  # 将信号连接到槽
        self.show()

#初始化界面的进度条定义：
    def appProgress(self):
        global progressBarValue
        self.ui.progressBar.setValue(progressBarValue)
        if progressBarValue > 100:
            self.timer.stop()
            # self.close()# 加载完后关闭该界面
        progressBarValue += 1


    def Begin(self):
        if progressBarValue > 100:
            self.close()
            self.logIn = LogWindow()  # 将第二个窗口换个名字
            self.logIn.show()  # 经第二个窗口显示出来

# 登录界面
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_logWindow() #Ui类实例化()
        self.ui.setupUi(self)
        self.ui.Log.clicked.connect(self.LogIn)  # 将信号连接到槽
        self.show()

    def LogIn(self):
        if self.ui.lineEdit.text() == "lxj" and self.ui.lineEdit_2.text() == "123":
            # 关闭当前窗口，打开App窗口
            app = App()
            self.close()
            app.run(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = InitWindow()
    sys.exit(app.exec_())
