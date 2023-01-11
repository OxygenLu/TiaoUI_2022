import HandTrackingModule as htm
import cv2
from pynput.mouse import Button, Controller
import pynput.keyboard
from collections import deque


MOUSE_SENSITIVE = 2
mouse = Controller()
keyboard = pynput.keyboard.Controller()

color_set = [(83, 109, 254), (124, 77, 255), (255, 64, 129), (255, 82, 82), (83, 109, 254)]
color_set_deep = [(197, 202, 233), (209, 196, 233), (225, 190, 231), (248, 187, 208), (255, 205, 210)]
offset = -90 - 25
MODE_NAME = ['Do Nothing', 'Move And Click', 'PPT Printer', 'AAA', 'BBB']

# Define Values
DO_NOTHING = 0
MOVE_AND_CLICK = 1
PPT_WRITE = 2
NOW_MODE = DO_NOTHING

NOW_MODE_COLOR = color_set[0]
pTime = 0
bef_clicked = 0
bef_selecting = 0
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
app = None
window = None
