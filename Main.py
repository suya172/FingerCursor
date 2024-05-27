import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import mediapipe as mp
import pyautogui as gui
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mpDrawStyles = mp.solutions.drawing_styles

fontpath = 'C:\Windows\Fonts\msgothic.ttc'
font = ImageFont.truetype(fontpath, 30)

gui_w ,gui_h =  gui.size()

CLICK_THRESHOLD = 60

go = True

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        #最後の要素のみ抽出
        for _ in results.multi_hand_landmarks:
            hand_landmarks = _
        
        for id,landmark in enumerate(hand_landmarks.landmark):
            cv_h,cv_w, _ = img.shape

            #カーソル移動用
            if id == 8: #人差し指の先端
                #モニター上の座標を計算
                cursor_monitor_x, cursor_monitor_y = int(landmark.x*gui_w), int(landmark.y*gui_h)
                #描画
                cursor_cv_x, cursor_cv_y = int(landmark.x*cv_w), int(landmark.y*cv_h)
                cv2.drawMarker(img, (cursor_cv_x, cursor_cv_y), (0, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=5)

            #マウス判定用
            if id == 4: #親指の先端
                a_cv_x , a_cv_y = int(landmark.x*cv_w), int(landmark.y*cv_h)
                cv2.drawMarker(img, (a_cv_x, a_cv_y), (192, 192, 192), markerType=cv2.MARKER_CROSS, markerSize=8, thickness=5)
            if id == 12: #中指の先端
                un_cv_x , un_cv_y = int(landmark.x*cv_w), int(landmark.y*cv_h)
                cv2.drawMarker(img, (un_cv_x, un_cv_y), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=8, thickness=5)

        #描画
        cv2.line(img,(a_cv_x,a_cv_y),(un_cv_x,un_cv_y),(0,0,0),thickness=1,lineType=cv2.LINE_8)

        #距離を計算
        distance = math.sqrt((a_cv_x-un_cv_x)**2+(a_cv_y-un_cv_y)**2)

        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((10, 5), str(distance),  fill=(0, 0, 255), font=font,  stroke_width=1, stroke_fill=(0, 0, 255)) 
        img = np.array(img_pil)

        
        if go:
            #カーソル位置を適用
            gui.moveTo(cursor_monitor_x,cursor_monitor_y)

            if distance < CLICK_THRESHOLD:
                gui.mouseDown(button='left')
            else:
                gui.mouseUp(button='left')


        # mpDraw.draw_landmarks(
        #     img,
        #     hand_landmarks,
        #     mpHands.HAND_CONNECTIONS,
        #     mpDrawStyles.get_default_hand_landmarks_style(),
        #     mpDrawStyles.get_default_hand_connections_style())
    else:
        gui.mouseUp(button='left')
    cv2.imshow('MediaPipe Hands', img)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
gui.mouseUp(button='left')
cap.release()
