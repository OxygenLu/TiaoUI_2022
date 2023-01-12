import math
import sys
import time

import pynput.keyboard
from PyQt5.QtWidgets import QApplication, QWidget
from pynput.mouse import Button, Controller
import HandTrackingModule as htm
import numpy as np
import mediapipe
import cv2
from collections import deque
from floatingball_app import FloatingBall_Test
from pyqt_camera_temp import Ui_PyQtCameraTemp

def a():
    print("aaaaaaaaaaaaaa")

def pyqt_main():
    app = QApplication(sys.argv)
    # ball_win = FloatingBall_Test()
    # ball_win.show()
    v_win = Ui_PyQtCameraTemp()
    v_win.show()
    sys.exit(app.exec_())



# AI Virtual Mouse use mediapipe
if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = FloatingBall_Test()
    # window.show()
    # main()
    # sys.exit(app.exec_())
    pyqt_main()

