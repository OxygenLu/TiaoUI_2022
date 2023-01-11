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

def pyqt_main():
    app = QApplication(sys.argv)
    v_win = Ui_PyQtCameraTemp()
    v_win.show()
    sys.exit(app.exec_())


def main():
    global plocY, NOW_MODE, wCam, hCam, plocX, bef_clicked, leftDown, pTime, NOW_MODE_COLOR, bef_selecting, app, window
    if cap.isOpened():
        success, img = cap.read()
        wCam, hCam = img.shape[1], img.shape[0]
    while cap.isOpened():
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        all_hands, img = detector.findHands(img)
        lmList, bbox, depth_radius = detector.findPosition(img)

        # 取食指和中指的尖端
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp(lmList)
            print(fingers)
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)

            if NOW_MODE == MOVE_AND_CLICK:
                img = MOVE_AND_CLICK_FUNC(fingers, hCam, img, wCam, x1, y1)

            elif NOW_MODE == PPT_WRITE:
                PPT_WRITER_FUNC(hCam, img, lmList, wCam)

            # Selecting Mode
            if fingers == [0, 1, 1, 1, 1]:
                if bef_selecting == 0:
                    bef_selecting = time.time()
                if time.time() - bef_selecting > 0.8:
                    NOW_MODE, NOW_MODE_COLOR = select_mode(img, lmList, offset, x2, y2)
            else: bef_selecting = 0

        if not success:
            print("Ignoring empty camera frame.")
            continue

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.putText(img, MODE_NAME[NOW_MODE], (20, 90), cv2.FONT_HERSHEY_PLAIN, 3,
                    (NOW_MODE_COLOR[2], NOW_MODE_COLOR[1], NOW_MODE_COLOR[0]), 3)

        # Display
        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break




# AI Virtual Mouse use mediapipe
if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = FloatingBall_Test()
    # window.show()
    # main()
    # sys.exit(app.exec_())
    pyqt_main()

