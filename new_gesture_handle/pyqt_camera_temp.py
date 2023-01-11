import math
import sys
import os
import time

import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import config_values as cfg
from pynput.mouse import Button, Controller
import numpy as np


class Ui_PyQtCameraTemp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_PyQtCameraTemp, self).__init__(parent)

        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0

    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
        self.__layout_fun_button = QtWidgets.QHBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()  # QVBoxLayout类垂直地摆放小部件

        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_close = QtWidgets.QPushButton(u'退出')

        # button颜色修改
        button_color = [self.button_open_camera, self.button_close]
        for i in range(2):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                           "QPushButton:hover{color:red}"
                                           "QPushButton{background-color:rgb(78,255,255)}"
                                           "QpushButton{border:2px}"
                                           "QPushButton{border_radius:10px}"
                                           "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # move()方法是移动窗口在屏幕上的位置到x = 500，y = 500的位置上
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.label_move)

        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'摄像头')

        '''
        # 设置背景颜色
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(),QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

    def slot_init(self):  # 建立通信连接
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)

    def button_open_camera_click(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                msg = QtWidgets.QMessageBox.Warning
                # if msg==QtGui.QMessageBox.Cancel:
                #                     pass
            else:
                success, img = self.cap.read()
                cfg.wCam, cfg.hCam = img.shape[1], img.shape[0]
                self.label_show_camera.resize(cfg.wCam, cfg.hCam)
                self.label_show_camera.setFixedSize(cfg.wCam, cfg.hCam)
                print(cfg.wCam, cfg.hCam)
                self.timer_camera.start(30)
                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')

    def PPT_WRITER_FUNC(self, hCam, img, lmList, wCam):
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
        cv2.rectangle(img, (cfg.frameR, cfg.frameR), (wCam - cfg.frameR, hCam - cfg.frameR), (255, 0, 255), 2)
        x3 = np.interp(cx, (cfg.frameR, wCam - cfg.frameR), (0, cfg.wScr))
        y3 = np.interp(cy, (cfg.frameR, hCam - cfg.frameR), (0, cfg.hScr))
        # x3 = np.interp(x1, (wCam - cfg.frameR, cfg.frameR), (0, wScr))
        # y3 = np.interp(y1, (hCam - cfg.frameR, cfg.frameR), (0, hScr))
        # Smoothen Values
        clocX = cfg.plocX + (x3 - cfg.plocX) / cfg.smoothening
        clocY = cfg.plocY + (y3 - cfg.plocY) / cfg.smoothening
        # mouse move
        cfg.mouse_points.append((cfg.wScr - x3, y3))
        xx3_sum, yy3_sum = 0, 0
        for xx3, yy3 in cfg.mouse_points:
            xx3_sum += xx3
            yy3_sum += yy3
        cfg.mouse.position = (xx3_sum // cfg.smoothening, yy3_sum // cfg.smoothening)
        cfg.plocX, cfg.plocY = clocX, clocY
        if length <= 25:
            # 模拟左键一直按下
            # 如果左键已经按下，就不再按下
            if not cfg.leftDown:
                cfg.mouse.press(Button.left)
                cfg.leftDown = True
        if length > 45:
            # 模拟左键松开
            if cfg.leftDown:
                cfg.mouse.release(Button.left)
                cfg.leftDown = False

    def MOVE_AND_CLICK_FUNC(self, fingers, hCam, img, wCam, x1, y1):
        # 一根手指：移动指针
        if fingers[1] == 1 and fingers[2] == 0:
            cv2.rectangle(img, (cfg.frameR, cfg.frameR), (wCam - cfg.frameR, hCam - cfg.frameR), (255, 0, 255), 2)
            x3 = np.interp(x1, (cfg.frameR, wCam - cfg.frameR), (0, cfg.wScr))
            y3 = np.interp(y1, (cfg.frameR, hCam - cfg.frameR), (0, cfg.hScr))
            # x3 = np.interp(x1, (wCam - cfg.frameR, cfg.frameR), (0, wScr))
            # y3 = np.interp(y1, (hCam - cfg.frameR, cfg.frameR), (0, hScr))

            # Smoothen Values
            clocX = cfg.plocX + (x3 - cfg.plocX) / cfg.smoothening
            clocY = cfg.plocY + (y3 - cfg.plocY) / cfg.smoothening
            # mouse move

            cfg.mouse_points.append((x3, y3))
            xx3_sum, yy3_sum = 0, 0
            for xx3, yy3 in cfg.mouse_points:
                xx3_sum += xx3
                yy3_sum += yy3
            cfg.mouse.position = (cfg.wScr - (xx3_sum // cfg.smoothening), yy3_sum // cfg.smoothening)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cfg.plocX, cfg.plocY = clocX, clocY
        if fingers[1] == 1 and fingers[2] == 1:
            leng, img, _ = cfg.detector.findDistance(8, 12, img)
            print(leng)
            if leng < 40:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                if time.time() - cfg.bef_clicked > 0.5:
                    cfg.mouse.click(Button.left, 1)
                    cfg.bef_clicked = time.time()
        # if fingers == [1, 1, 1, 1, 1]:
        #     # 模拟Enter
        #     if time.time() - bef_clicked > 0.5:
        #         keyboard.press(pynput.keyboard.Key.enter)
        #         bef_clicked = time.time()
        return img

    def select_mode(self, img, lmList, offset, x2, y2):
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
                zip(range(0 + offset, int(12 * 5 + offset), 10), cfg.color_set, cfg.color_set_deep)):
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

    def show_camera(self):
        success, img = self.cap.read()
        all_hands, img = cfg.detector.findHands(img)
        lmList, bbox, depth_radius = cfg.detector.findPosition(img)

        # 取食指和中指的尖端
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = cfg.detector.fingersUp(lmList)
            print(fingers)
            cv2.rectangle(img, (cfg.frameR, cfg.frameR), (cfg.wCam - cfg.frameR, cfg.hCam - cfg.frameR),
                          (255, 0, 255), 2)

            if cfg.NOW_MODE == cfg.MOVE_AND_CLICK:
                img = self.MOVE_AND_CLICK_FUNC(fingers, cfg.hCam, img, cfg.wCam, x1, y1)

            elif cfg.NOW_MODE == cfg.PPT_WRITE:
                self.PPT_WRITER_FUNC(cfg.hCam, img, lmList, cfg.wCam)

            # Selecting Mode
            if fingers == [0, 1, 1, 1, 1]:
                if cfg.bef_selecting == 0:
                    cfg.bef_selecting = time.time()
                if time.time() - cfg.bef_selecting > 0.8:
                    cfg.NOW_MODE, cfg.NOW_MODE_COLOR = self.select_mode(img, lmList, cfg.offset, x2, y2)
            else:
                cfg.bef_selecting = 0

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - cfg.pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.putText(img, cfg.MODE_NAME[cfg.NOW_MODE], (20, 90), cv2.FONT_HERSHEY_PLAIN, 3,
                    (cfg.NOW_MODE_COLOR[2], cfg.NOW_MODE_COLOR[1], cfg.NOW_MODE_COLOR[0]), 3)
        self.image = img

        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setScaledContents(True)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()