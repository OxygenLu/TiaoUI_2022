import math
import time

import pynput.keyboard
from pynput.mouse import Button, Controller
import HandTrackingModule as htm
import numpy as np
import mediapipe
import cv2
from collections import deque

MOUSE_SENSITIVE = 2
mouse = Controller()
keyboard = pynput.keyboard.Controller()

color_set = [(83, 109, 254), (124, 77, 255), (255, 64, 129), (255, 82, 82), (83, 109, 254)]
color_set_deep = [(197, 202, 233), (209, 196, 233), (225, 190, 231), (248, 187, 208), (255, 205, 210)]
offset = -90 - 25
MODE_NAME = ['Do Nothing', 'Move And Click', 'PPT Printer', 'AAA', 'BBB']


# Update Push

def main():
    DO_NOTHING = 0
    MOVE_AND_CLICK = 1
    PPT_WRITE = 2
    NOW_MODE = DO_NOTHING


    NOW_MODE_COLOR = color_set[0]
    pTime = 0
    bef_clicked = 0
    frameR = 100  # Frame Reduction
    smoothening = 8
    detector = htm.HandDetector(maxHands=1)


    cap = cv2.VideoCapture(0)
    wCam, hCam = (0, 0)
    wScr, hScr = 1920, 1080
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    leftDown = False
    # Colors Set When Select Mode

    # Points
    mouse_points = deque(maxlen=smoothening)
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
                    mouse.position = (wScr - (xx3_sum // smoothening), yy3_sum // smoothening)
                    cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                if fingers[1] == 1 and fingers[2] == 1:
                    leng, img, _ = detector.findDistance(8, 12, img)
                    print(leng)
                    if leng < 40:
                        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        if time.time() - bef_clicked > 0.5:
                            mouse.click(Button.left, 1)
                            bef_clicked = time.time()

                # if fingers == [1, 1, 1, 1, 1]:
                #     # 模拟Enter
                #     if time.time() - bef_clicked > 0.5:
                #         keyboard.press(pynput.keyboard.Key.enter)
                #         bef_clicked = time.time()

            elif NOW_MODE == PPT_WRITE:
                # 食指和大拇指的坐标
                x_shi, y_shi = lmList[8][1:]
                x_damu, y_damu = lmList[4][1:]
                # 两个手指之间连线
                cx = (x_shi + x_damu) // 2
                cy = (y_shi + y_damu) // 2
                cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                # 两个手指之间的距离
                length = math.hypot(x_damu - x_shi, y_damu - y_shi)
                print(length)
                # 中点

                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                x3 = np.interp(cx, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(cy, (frameR, hCam - frameR), (0, hScr))
                # x3 = np.interp(x1, (wCam - frameR, frameR), (0, wScr))
                # y3 = np.interp(y1, (hCam - frameR, frameR), (0, hScr))

                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                # mouse move

                mouse_points.append((wScr - x3, y3))
                xx3_sum, yy3_sum = 0, 0
                for xx3, yy3 in mouse_points:
                    xx3_sum += xx3
                    yy3_sum += yy3
                mouse.position = (xx3_sum // smoothening, yy3_sum // smoothening)
                plocX, plocY = clocX, clocY

                if length <= 25:
                    # 模拟左键一直按下
                    # 如果左键已经按下，就不再按下
                    if not leftDown:
                        mouse.press(Button.left)
                        leftDown = True
                if length > 45:
                    # 模拟左键松开
                    if leftDown:
                        mouse.release(Button.left)
                        leftDown = False

            if fingers == [0, 1, 1, 1, 1]:
                NOW_MODE, NOW_MODE_COLOR = select_mode(img, lmList, offset, x2, y2)

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
        if cv2.waitKey(5) & 0xFF == 27:
            break


def select_mode(img, lmList, offset, x2, y2):
    # 获取手掌的位置 WRIST
    x0, y0 = lmList[0][1:]
    # 在 x0, y0 建立极坐标系
    # 计算x0, y0 到 x2, y2 的角度
    angle = math.atan2(y2 - y0, x2 - x0) * 180 / math.pi
    # 计算x0, y0 到 x2, y2 的距离
    distance = math.sqrt((x2 - x0) ** 2 + (y2 - y0) ** 2)
    print(f'Angle = {angle}')
    # 求解x_mode, y_mode，其中，在x0, y0 建立的极坐标系中，x3, y3 与 x2, y2 的距离0.1 distance
    x_mode = x0 + 1.1 * distance * math.cos(angle * math.pi / 180)
    y_mode = y0 + 1.1 * distance * math.sin(angle * math.pi / 180)
    # 绘制模式切换的圆圈
    cv2.circle(img, (int(x_mode), int(y_mode)), 15, (0, 255, 0), cv2.FILLED)
    # 模式切换
    # 每隔15度就绘制1个圆圈，共绘制5个
    nearest = 10000000
    nearest_i_angle = -1
    nearest_i_color_deep = -1
    nearest_i_color = -1
    nearest_i_MODE = -1

    for i, (angle_i, color, color_deep) in enumerate(
            zip(range(0 + offset, int(12 * 5 + offset), 10), color_set, color_set_deep)):
        x_select = x0 + 1.1 * distance * math.cos(angle_i * math.pi / 180)
        y_select = y0 + 1.1 * distance * math.sin(angle_i * math.pi / 180)
        # 圆圈，不填充

        cv2.circle(img, (int(x_select), int(y_select)), 25, (color[2], color[1], color[0]), thickness=10)
        bef_near = nearest
        nearest = min(nearest, math.sqrt((x_mode - x_select) ** 2 + (y_mode - y_select) ** 2))
        if nearest != bef_near:
            nearest_i_angle = angle_i
            nearest_i_color_deep = color_deep
            nearest_i_MODE = i
            nearest_i_color = color

    x_selected = x0 + 1.1 * distance * math.cos(nearest_i_angle * math.pi / 180)
    y_selected = y0 + 1.1 * distance * math.sin(nearest_i_angle * math.pi / 180)

    cv2.circle(img,
               (int(x_selected), int(y_selected)),
               25,
               (nearest_i_color_deep[2], nearest_i_color_deep[1], nearest_i_color_deep[0]),
               thickness=10)
    return nearest_i_MODE, (nearest_i_color[2], nearest_i_color[1], nearest_i_color[0])


# AI Virtual Mouse use mediapipe
if __name__ == '__main__':
    main()
