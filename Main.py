import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import mediapipe as mp
import pyautogui as gui
import math
import time


def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    mpDraw = mp.solutions.drawing_utils
    mpDrawStyles = mp.solutions.drawing_styles

    fontpath = '.\data\msgothic.ttc'
    font = ImageFont.truetype(fontpath, 30)

    gui_w, gui_h = gui.size()

    CURSOR_INTERVAL = 0.1
    CLICK_THRESHOLD = 50

    go = True  # デバッグ用

    cursor_time = time.time()
    prev_distances = {'l': 999, 'r': 999}

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img.flags.writeable = False
        results = hands.process(imgRGB)
        img.flags.writeable = True
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:

                for id, landmark in enumerate(hand_landmark.landmark):
                    cv_h, cv_w, _ = img.shape

                    # カーソル移動用
                    if id == 0:  # 手の付け根
                        # モニター上の座標を計算
                        cursor_monitor_x, cursor_monitor_y = int(
                            landmark.x*gui_w), int(landmark.y*gui_h)

                        cursor_cv_x, cursor_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (cursor_cv_x, cursor_cv_y), (0, 255, 255),
                                       markerType=cv2.MARKER_CROSS, markerSize=10, thickness=5)

                    # マウス判定用
                        # トリガー
                    if id == 4:  # 親指の先端
                        trig_cv_x, trig_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (trig_cv_x, trig_cv_y), (192, 192, 192),
                                       markerType=cv2.MARKER_CROSS, markerSize=8, thickness=5)
                        # 左クリック
                    if id == 12:  # 中指の先端
                        l_cv_x, l_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (l_cv_x, l_cv_y), (0, 0, 255),
                                       markerType=cv2.MARKER_CROSS, markerSize=8, thickness=5)

                        # 右クリック
                    if id == 16:  # 薬指の先端
                        r_cv_x, r_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (r_cv_x, r_cv_y), (0, 128, 0),
                                       markerType=cv2.MARKER_CROSS, markerSize=8, thickness=5)

                # 距離を計算
                distances = {}
                distances['l'] = math.sqrt(
                    (trig_cv_x-l_cv_x)**2+(trig_cv_y-l_cv_y)**2)
                distances['r'] = math.sqrt(
                    (trig_cv_x-r_cv_x)**2+(trig_cv_y-r_cv_y)**2)

                # 描画
                cv2.line(img, (trig_cv_x, trig_cv_y), (l_cv_x, l_cv_y),
                         ((255, 255, 0) if distances['l'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.line(img, (trig_cv_x, trig_cv_y), (r_cv_x, r_cv_y),
                         ((255, 255, 0) if distances['r'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)

                # 数値表示
                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                draw.text((trig_cv_x, trig_cv_y + 10), str(int(distances['l'])),  fill=((255, 144, 30) if distances['l'] >= CLICK_THRESHOLD else (0, 0, 255)),
                          font=font,  stroke_width=1, stroke_fill=((255, 144, 30) if distances['l'] >= CLICK_THRESHOLD else (0, 0, 255)))
                draw.text((trig_cv_x, trig_cv_y + 45), str(int(distances['r'])),  fill=((255, 144, 30) if distances['r'] >= CLICK_THRESHOLD else (0, 0, 255)),
                          font=font,  stroke_width=1, stroke_fill=((255, 144, 30) if distances['r'] >= CLICK_THRESHOLD else (0, 0, 255)))
                img = np.array(img_pil)

                if go:
                    # カーソル移動
                    if (time.time() - cursor_time) > CURSOR_INTERVAL:
                        gui.moveTo(cursor_monitor_x, cursor_monitor_y)
                        cursor_time = time.time()

                    # 左クリック
                    if (prev_distances['l'] < CLICK_THRESHOLD) & (distances['l'] >= CLICK_THRESHOLD):
                        gui.click(button='left')
                        prev_distances['l'] = distances['l']
                    elif (prev_distances['l'] >= CLICK_THRESHOLD) & (distances['l'] < CLICK_THRESHOLD):
                        prev_distances['l'] = distances['l']

                    # 右クリック
                    if (prev_distances['r'] < CLICK_THRESHOLD) & (distances['r'] >= CLICK_THRESHOLD):
                        gui.click(button='right')
                        prev_distances['r'] = distances['r']
                    elif (prev_distances['r'] >= CLICK_THRESHOLD) & (distances['r'] < CLICK_THRESHOLD):
                        prev_distances['r'] = distances['r']

                # mpDraw.draw_landmarks(
                #     img,
                #     hand_landmarks,
                #     mpHands.HAND_CONNECTIONS,
                #     mpDrawStyles.get_default_hand_landmarks_style(),
                #     mpDrawStyles.get_default_hand_connections_style())
        else:
            for k in prev_distances.keys():
                prev_distances[k] = 999
        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    cap.release()


if __name__ == '__main__':
    main()
