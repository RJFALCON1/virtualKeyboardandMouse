import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui
import math

mouse = Controller()
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawingUtils = mp.solutions.drawing_utils
(screenWidth,screenHeight) = pyautogui.size()
hands = mp_hands.Hands(min_detection_confidence=0.8,
                       min_tracking_confidence=0.5)
pinch = False
tipIDs = [4,8,12,16,20]
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
def countFingers(img,landmarks,handNum = 0):
    global pinch
    if landmarks :
        handLandmarks = landmarks[handNum].landmark
        fingers = []
        for tid in tipIDs :
            fingertip_y = handLandmarks[tid].y
            fingerbottom_y = handLandmarks[tid-2].y
            if fingertip_y > fingerbottom_y :
                fingers.append(0)
            elif fingertip_y < fingerbottom_y :
                fingers.append(1)
        totalFingers = fingers.count(1)
        #drawing line between fingertip and thumbtip
        fingertip_x = int((handLandmarks[8].x)* width)
        fingertip_y = int((handLandmarks[8].y)*height)
        thumbtip_x = int((handLandmarks[4].x)*width)
        thumbtip_y = int((handLandmarks[4].y)*height)
        cv2.line(img,(fingertip_x,fingertip_y),(thumbtip_x,thumbtip_y),(255,0,0),2)
        centerX = int((fingertip_x + thumbtip_x)/2)
        centerY = int((fingertip_y + thumbtip_y)/2)
        cv2.circle(img,(centerX,centerY),2,(0,0,255),2)
        distance = math.sqrt(((fingertip_x - thumbtip_x)**2)+((fingertip_y - thumbtip_y)**2))
        print(mouse.position)
        cameraMouseX = (centerX/width)*screenWidth
        cameraMouseY = (centerY/height)*screenHeight
        mouse.position = (cameraMouseX, cameraMouseY)
        if distance <= 40 :
            if pinch == False :
                pinch = True
                mouse.press(Button.left)
        if distance >= 40 :
            if pinch == True:
                pinch = False
                mouse.release(Button.left )


            




            
    
def drawLandmarks(img,landmarks) :
    if (landmarks) :
        for lm in landmarks:
            mp_drawingUtils.draw_landmarks(img,lm,mp_hands.HAND_CONNECTIONS)

while True :
    ret, img = cam.read()
    img = cv2.flip(img,1)
    results = hands.process(img)
    landmarks = results.multi_hand_landmarks
    drawLandmarks(img,landmarks)
    countFingers(img,landmarks)
    cv2.imshow('cam',img)
    if cv2.waitKey(1) == 32 :
        break