from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class FloatingBall_Test(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super(FloatingBall_Test, self).__init__()
        self._initUI()


    def _initUI(self):
        self.setFixedSize(QSize(100, 100))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 透明

        # 使用QPainter绘制圆形，附带抗锯齿
        self._pix = QPixmap(self.size())
        self._pix.fill(Qt.transparent)
        painter = QPainter(self._pix)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(25, 118, 210, 255 // 2)))
        painter.drawEllipse(self.rect())

        # Draw Text
        painter.setPen(QColor(255, 255, 255, 255))
        painter.setFont(QFont('SimSun', 25))
        painter.drawText(self.rect(), Qt.AlignCenter, "Hello")
        painter.end()

        self.setMask(self._pix.mask())


        # 显示self._pix
        self._label = QLabel(self)
        self._label.setPixmap(self._pix)
        self._label.resize(self._pix.size())
        self._label.move(0, 0)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.show()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._startPos is None:
            self._startPos = QPoint(e.x(), e.y())
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloatingBall_Test()

    sys.exit(app.exec_())
