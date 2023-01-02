import cv2

# 摄像头
cap = cv2.VideoCapture(0)
# 显示摄像头画面
while True:
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

if __name__ == '__main__':
    pass