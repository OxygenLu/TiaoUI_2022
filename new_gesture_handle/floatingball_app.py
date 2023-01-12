from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class FloatingBall_Test(QDialog):
    textChangeSignal = pyqtSignal(str)
    _startPos = None
    _endPos = None
    _isTracking = False
    main_ball_color = QColor(25, 118, 210, 255 // 2)
    main_ball_text = 'Hello!'

    def __init__(self, parent=None):
        super(FloatingBall_Test, self).__init__(parent)
        self._initUI()

    def set_ball_color(self, color_rgba: tuple):
        assert len(
            color_rgba) == 4, f"Failed to set ball color, color_rgba must be a tuple with 4 elements, but got {color_rgba}"
        self.main_ball_color = QColor(*color_rgba)
        self.update_ball()

    def set_ball_text(self, text: str):
        self.main_ball_text = text
        self.update_ball()

    def _initUI(self):
        self.setFixedSize(QSize(100, 100))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.update_ball()

        self._label.resize(self._pix.size())

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def update_ball(self):
        self._pix = QPixmap(self.size())
        self._pix.fill(Qt.transparent)
        painter = QPainter(self._pix)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.main_ball_color))
        painter.drawEllipse(self.rect())
        # Draw Text
        painter.setPen(QColor(255, 255, 255, 255))
        painter.setFont(QFont('SimSun', 25))
        painter.drawText(self.rect(), Qt.AlignCenter, f'{self.main_ball_text}')
        painter.end()
        self.setMask(self._pix.mask())
        # 显示self._pix
        self._label = QLabel(self)
        self._label.setPixmap(self._pix)

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
