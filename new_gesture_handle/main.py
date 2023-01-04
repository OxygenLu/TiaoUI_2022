import math
import time

from pynput.mouse import Button, Controller
import HandTrackingModule as htm
import numpy as np
import mediapipe
import cv2
from collections import deque

MOUSE_SENSITIVE = 2
mouse = Controller()


def main():
    pTime = 0
    bef_clicked = 0
    frameR = 100  # Frame Reduction
    smoothening = 8
    detector = htm.HandDetector(maxHands=1)
    # MediaPipe
    mp_drawing = mediapipe.solutions.drawing_utils
    mp_hands = mediapipe.solutions.hands
    hands = mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1
    )
    cap = cv2.VideoCapture(0)
    wCam, hCam = (0, 0)
    wScr, hScr = 1920, 1080
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    # Points
    mouse_points = deque(maxlen=smoothening)
    if cap.isOpened():
        success, img = cap.read()
        wCam, hCam = img.shape[1], img.shape[0]
    while cap.isOpened():
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        all_hands, img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 取食指和中指的尖端
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            print(fingers)
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)

            # 一根手指：移动指针
            if fingers[1] == 1 and fingers[2] == 0:
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # x3 = np.interp(x1, (wCam - frameR, frameR), (0, wScr))
                # y3 = np.interp(y1, (hCam - frameR, frameR), (0, hScr))

                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                # mouse move

                mouse_points.append((x3, y3))
                xx3_sum, yy3_sum = 0, 0
                for xx3, yy3 in mouse_points:
                    xx3_sum += xx3
                    yy3_sum += yy3
                mouse.position = (xx3_sum // smoothening, yy3_sum // smoothening)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            if fingers[1] == 1 and fingers[2] == 1:
                leng, img, _ = detector.findDistance(8, 12, img)
                print(leng)
                if leng < 50:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    if time.time() - bef_clicked > 0.5:
                        mouse.click(Button.left, 1)
                        bef_clicked = time.time()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Display
        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(5) & 0xFF == 27:
            break


# AI Virtual Mouse use mediapipe
if __name__ == '__main__':
    main()
