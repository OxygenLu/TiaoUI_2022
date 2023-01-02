import cv2
import time
import torch
import mediapipe as mp
import numpy as np
import threading


class Identify:
    def __init__(self, win):
        self.win = win

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        movement = {0: "点击", 1: "平移", 2: "缩放", 3: "抓取", 4: "旋转", 5: "无"}
        S = 0.05
        device = torch.device('cpu')

        if torch.cuda.is_available():
            device = torch.device('cuda:0')

        model = torch.load('model_bakk.pt').to(device)
        hidden_dim = 35
        num_layers = 2

        h_t = torch.zeros(num_layers, 1, hidden_dim)
        h_t = h_t.to(device)

        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ratio = cap.get(4) / cap.get(3)  # 高宽比
        print(cap.isOpened())

        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.65,
                min_tracking_confidence=0.5) as hands:

            start_time = time.time()

            while cap.isOpened():
                self.win.eventRunning.wait()

                in_dim = torch.zeros(126)

                wait_time = S - (time.time() - start_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                start_time = time.time()
                success, image = cap.read()

                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:

                    if len(results.multi_handedness) == 1 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 1:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_1 = []
                            for k in range(0, 21):
                                index_1.append(hand_landmarks.landmark[k].x)
                                index_1.append(hand_landmarks.landmark[k].y)
                                index_1.append(hand_landmarks.landmark[k].z)
                            for k_1 in range(0, 63):
                                index_1.append(0)
                        in_dim = torch.from_numpy(np.array(index_1))

                    elif len(results.multi_handedness) == 1 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 0:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_0 = []
                            for k_1 in range(0, 63):
                                index_0.append(0)
                            for k in range(0, 21):
                                index_0.append(hand_landmarks.landmark[k].x)
                                index_0.append(hand_landmarks.landmark[k].y)
                                index_0.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_0))
                    elif len(results.multi_handedness) == 2 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 1:
                        index_1_first = []
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                            for k in range(0, 21):
                                index_1_first.append(hand_landmarks.landmark[k].x)
                                index_1_first.append(hand_landmarks.landmark[k].y)
                                index_1_first.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_1_first))
                    elif len(results.multi_handedness) == 2 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 0:
                        results.multi_hand_landmarks.reverse()
                        index_0_first = []
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                            for k in range(0, 21):
                                index_0_first.append(hand_landmarks.landmark[k].x)
                                index_0_first.append(hand_landmarks.landmark[k].y)
                                index_0_first.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_0_first))
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # cv2.imshow('MediaPipe Hands', image)
                if self.win.eventRunning.isSet():
                    self.win.flash_img(image, ratio)
                # if (cv2.waitKey(1) & 0xFF) == ord('q'):
                #     break

                in_dim = in_dim.unsqueeze(dim=0)
                in_dim = in_dim.unsqueeze(dim=0)
                in_dim = in_dim.to(torch.float32).to(device)
                h_t = h_t.to(torch.float32).to(device)
                rel, h_t = model((in_dim, h_t))

                rel = torch.sigmoid(rel)
                confidence, rel = rel.max(1)

                # print(movement[rel.item()], '\t置信度：', round(confidence.item(), 2))
                self.win.set_gesture(movement[rel.item()])

                #
                # if self.win.eventRunning.isSet():
                #     self.win.flash_img(image, ratio)
                #
                # in_dim = in_dim.unsqueeze(dim=0)
                # in_dim = in_dim.unsqueeze(dim=0)
                #
                # in_dim = in_dim.to(torch.float32).to(device)
                # h_t = h_t.to(torch.float32).to(device)
                # rel, h_t = model((in_dim, h_t))
                #
                # rel = torch.sigmoid(rel)
                # confidence, rel = rel.max(1)
                #
                # # 对每个动作设置单独的置信度阈值
                # cfd = {'点击': 0.985, '平移': 0.997, '缩放': 0.99, '抓取': 0.975, '旋转': 0.99, '无': 0, '截图': 0.99}
                # if confidence > cfd[movement[rel.item()]]:  # 超过阈值的动作将会被输出
                #     now_gesture = last_gesture
                #     last_gesture = movement[rel.item()]
                #     if not (now_gesture == last_gesture):  # 判断是否与上次的输出相同，若相同则不输出
                #         if time.time() - prin_time > 2:  # 若距离上次输出时间小于2秒，则不输出
                #             # print(movement[rel.item()], ' \t置信度：', round(confidence.item(), 2))
                #             self.win.set_gesture(movement[rel.item()])
                #             prin_time = time.time()  # 重置输出时间
                #             h_t = torch.zeros(num_layers, 1, hidden_dim).to(device)
                #             time.sleep(1)

        cap.release()
