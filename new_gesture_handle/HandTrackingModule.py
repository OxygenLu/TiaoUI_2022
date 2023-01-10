import cv2
import mediapipe as mp
import math


class HandDetector:

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, lmList):
        # fingers = []
        # # Thumb
        # if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)
        #
        # # Fingers
        # for id in range(1, 5):
        #     if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
        #         fingers.append(1)
        #     else:
        #         fingers.append(0)

            # totalFingers = fingers.count(1)

        # return fingers

        fingerList = []
        id, originx, originy = lmList[0]
        keypoint_list = [[2, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingerList.append(1)
        else:
            fingerList.append(0)
        for point in keypoint_list[1:]:
            id, x1, y1 = lmList[point[0]]
            id, x2, y2 = lmList[point[1]]
            if math.hypot(x2 - originx, y2 - originy) > math.hypot(x1 - originx, y1 - originy):
                fingerList.append(1)
            else:
                fingerList.append(0)


        return fingerList


    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = 0
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    def findPosition(self, img, handNo=0, draw=True):
        """
        Find the position of a hand in the image.
        :param img: Image to find the hand in.
        :param handNo: Hand number to find.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        radius = -1
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]
            # 获取手腕处的z
            cz0 = myHand.landmark[0].z
            print(f'Depth: {cz0}')
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                cz = myHand.landmark[id].z
                depth_z = cz0 - cz
                radius = int(6 * (1 + depth_z*5))
                # print(f'Radius: {radius}')
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                # if draw:
                #     cv2.circle(img, (cx, cy), radius, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
        return self.lmList, bbox, radius

