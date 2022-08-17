
import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
keyboard = Controller()
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
tipIDs = [4, 8, 12, 16, 20]
hands = mp_hands.Hands(min_detection_confidence=0.8,
                       min_tracking_confidence=0.5)
videoState = None

def countFingers(img,landmarks,handNum = 0):
    global videoState
    if landmarks :
        handLandmarks = landmarks[handNum].landmark
        fingers = []
        for tid in tipIDs :
            fingerTip_y = handLandmarks[tid].y
            fingerBottom_y = handLandmarks[tid-2].y
            if tid != 4:
                if fingerBottom_y > fingerTip_y :
                    fingers.append(1)
                elif fingerBottom_y < fingerTip_y :
                    fingers.append(0)
        totalFingers = fingers.count(1)
        if totalFingers == 4 :
            videoState = 'play'
        if totalFingers == 0 and videoState == 'play' :
            videoState = 'pause'
            keyboard.press(Key.space)

def drawLandmarks(img, landmarks):
    if (landmarks):
        for lm in landmarks:
            mp_drawing.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)


while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    results = hands.process(img)
    landmarks = results.multi_hand_landmarks
    drawLandmarks(img, landmarks)
    countFingers(img,landmarks)
    if cv2.waitKey(1) == 27 :
        break
cv2.destroyAllWindows()
