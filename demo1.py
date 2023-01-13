import sys
from menu import Ui_MainWindow
from PyQt5.QtCore import Qt,QPropertyAnimation,QPoint
from PyQt5.QtWidgets import QMainWindow,QApplication



class mainWindd(QMainWindow):
    def __init__(self, parent=None, *args, **Kwargs):
        super().__init__(parent, *args, **Kwargs)
        self.ui = Ui_MainWindow()# Ui类实例化()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.setupUi(self)
        self.start_x = 0
        self.start_y = 0
        self.show()


    # 鼠标进入事件    鼠标移到窗口上将会执行这个事件
    def enterEvent(self, evt):
        # 判断y坐标是否等于 -498 是的话就说明它在外边，哪我们开启动画让他跑回来
        if self.y() == -498:
            # 开启动画
            animation = QPropertyAnimation(self, b"pos", self)
            animation.setStartValue(QPoint(self.x(), self.y()))  # 这是动画起始位置
            animation.setEndValue(
                QPoint(self.x(), 0))  # 这是结束位置  x 不变让y变成负数就会跑到屏幕外边去， 我的高是500，设置了498，剩下2，不要全部设置成500， 不然鼠标进不去窗口，就移不出来
            animation.setDuration(200)  # 设置动画时长
            animation.start()  # 启动动画

        print("鼠标进来了")


    # 鼠标离开事件    鼠标从窗口上移出将会执行这个事件
    def leaveEvent(self, evt):
        # 鼠标移出去，我们判断它的y坐标是否等于或小于0  如果是 说明窗口就在屏幕边缘 那我们就开启动画让它跑到屏幕外边去
        if self.y() <= 0:
            # 开启动画
            animation = QPropertyAnimation(self, b"pos", self)
            animation.setStartValue(QPoint(self.x(), self.y()))     # 这是动画起始位置
            animation.setEndValue(QPoint(self.x(), -498))   #这是结束位置  x 不变， 让y变成负数就会跑到屏幕外边去， 我的高是500，设置了498，剩下2，不要全部设置成500， 不然鼠标进不去窗口，就移不出来
            animation.setDuration(200)  # 设置动画时长
            animation.start()   # 启动动画
        print("鼠标出去了")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            super(mainWindd, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseMoveEvent(self, event):
        try:
            super(mainWindd, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainWindd()
    sys.exit(app.exec_())