import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import mediapipe as mp
import pyautogui as gui
import math
import time
import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--device',type=int,default=0)

    args = parser.parse_args()
    return args


def main():
    def clamp(x, MIN, MAX): return max(MIN, min(x, MAX))

    # 引数解析
    args = get_args()

    debug = args.debug
    cap_device = args.device

    # Webカメラ設定
    WINDOW_NAME = 'FingerCursor'
    cv2.namedWindow(WINDOW_NAME)
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap_fps = int(cap.get(cv2.CAP_PROP_FPS))
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

    font = cv2.FONT_HERSHEY_SIMPLEX

    gui_w, gui_h = gui.size()

    CURSOR_INTERVAL = 0.1
    SCROLL_INTERVAL = 0.5
    SCROLL_AMOUNT = 300
    CLICK_THRESHOLD = 40

    cursor_time = time.perf_counter()
    cursor_aria = {'x': [0.25, 0.75], 'y': [0.25, 0.75]}
    prev_distances = {'l': 999, 'r': 999, 'ld': 999}

    scroll_time = time.perf_counter()

    while True:
        p_a = time.perf_counter()
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
                        # モニター上の座標(割合)を計算
                        cursor_x, cursor_y = clamp((landmark.x-cursor_aria['x'][0])/(cursor_aria['x'][1]-cursor_aria['x'][0]), 0, 1), clamp(
                            (landmark.y-cursor_aria['y'][0])/(cursor_aria['y'][1]-cursor_aria['y'][0]), 0, 1)
                        # モニター上の座標を計算
                        cursor_monitor_x, cursor_monitor_y = int(
                            cursor_x*gui_w), int(cursor_y*gui_h)
                        # [0,MONITOR_SIZE]->[1,MONITOR_SIZE-2] pyautogui.FailSafeExceptionを回避
                        cursor_monitor_x = clamp(cursor_monitor_x, 1, gui_w-2)
                        cursor_monitor_y = clamp(cursor_monitor_y, 1, gui_h-2)

                        # 描画
                        cursor_cv_x, cursor_cv_y = int(
                            clamp(landmark.x, cursor_aria['x'][0], cursor_aria['x'][1])*cv_w), int(clamp(landmark.y, cursor_aria['y'][0], cursor_aria['y'][1])*cv_h)
                        cv2.circle(img, (cursor_cv_x, cursor_cv_y), 5, (0, 0, 255),
                                   lineType=cv2.LINE_8, thickness=5)

                        cv2.drawMarker(img, (int(landmark.x*cv_w), int(landmark.y*cv_h)), (0, 165, 255),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                    # マウス判定用
                        # トリガー
                    if id == 4:  # 親指の先端
                        trig_cv_x, trig_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (trig_cv_x, trig_cv_y), (192, 192, 192),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)
                        # 左クリック
                    if id == 12:  # 中指の先端
                        l_cv_x, l_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (l_cv_x, l_cv_y), (0, 255, 255),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                        # 右クリック
                    if id == 16:  # 薬指の先端
                        r_cv_x, r_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (r_cv_x, r_cv_y), (0, 128, 0),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                        # 左ドラッグ
                    if id == 8:  # 人差し指の先端
                        ld_cv_x, ld_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (ld_cv_x, ld_cv_y), (205, 90, 106),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                        # 上スクロール
                    if id == 20:  # 小指の先端
                        mu_cv_x, mu_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (mu_cv_x, mu_cv_y), (45, 82, 160),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                        # 下スクロール
                    if id == 17:  # 小指の付け根
                        md_cv_x, md_cv_y = int(
                            landmark.x*cv_w), int(landmark.y*cv_h)
                        cv2.drawMarker(img, (md_cv_x, md_cv_y), (250, 235, 215),
                                       markerType=cv2.MARKER_CROSS, markerSize=3, thickness=5)

                # 距離を計算
                distances = {}
                distances['l'] = math.sqrt(
                    (trig_cv_x-l_cv_x)**2+(trig_cv_y-l_cv_y)**2)
                distances['r'] = math.sqrt(
                    (trig_cv_x-r_cv_x)**2+(trig_cv_y-r_cv_y)**2)
                distances['ld'] = math.sqrt(
                    (trig_cv_x-ld_cv_x)**2+(trig_cv_y-ld_cv_y)**2)
                distances['mu'] = math.sqrt(
                    (trig_cv_x-mu_cv_x)**2+(trig_cv_y-mu_cv_y)**2)
                distances['md'] = math.sqrt(
                    (trig_cv_x-md_cv_x)**2+(trig_cv_y-md_cv_y)**2)

                # 描画
                cv2.line(img, (trig_cv_x, trig_cv_y), (l_cv_x, l_cv_y),
                         ((255, 255, 0) if distances['l'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.line(img, (trig_cv_x, trig_cv_y), (r_cv_x, r_cv_y),
                         ((255, 255, 0) if distances['r'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.line(img, (trig_cv_x, trig_cv_y), (ld_cv_x, ld_cv_y),
                         ((255, 255, 0) if distances['ld'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.line(img, (trig_cv_x, trig_cv_y), (mu_cv_x, mu_cv_y),
                         ((255, 255, 0) if distances['mu'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.line(img, (trig_cv_x, trig_cv_y), (md_cv_x, md_cv_y),
                         ((255, 255, 0) if distances['md'] >= CLICK_THRESHOLD else (255, 0, 255)), thickness=1, lineType=cv2.LINE_8)

                cv2.rectangle(img, (int(cursor_aria['x'][0]*cv_w), int(cursor_aria['y'][0]*cv_h)), (int(
                    cursor_aria['x'][1]*cv_w), int(cursor_aria['y'][1]*cv_h)), (0, 0, 0), thickness=3, lineType=cv2.LINE_8)
                

                if not debug:
                    # カーソル移動
                    if (time.perf_counter() - cursor_time) > CURSOR_INTERVAL:
                        gui.moveTo(cursor_monitor_x, cursor_monitor_y)
                        cursor_time = time.perf_counter()

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

                    # 左ドラッグ
                    if (prev_distances['ld'] < CLICK_THRESHOLD) & (distances['ld'] >= CLICK_THRESHOLD):
                        gui.mouseUp(button='left')
                        prev_distances['ld'] = distances['ld']
                    elif (prev_distances['ld'] >= CLICK_THRESHOLD) & (distances['ld'] < CLICK_THRESHOLD):
                        gui.mouseDown(button='left')
                        prev_distances['ld'] = distances['ld']

                    # 上スクロール
                    if (distances['mu'] < CLICK_THRESHOLD) & ((time.perf_counter() - scroll_time) > SCROLL_INTERVAL):
                        gui.scroll(SCROLL_AMOUNT)
                        scroll_time = time.perf_counter()

                    # 下スクロール
                    if (distances['md'] < CLICK_THRESHOLD) & ((time.perf_counter() - scroll_time) > SCROLL_INTERVAL):
                        gui.scroll(SCROLL_AMOUNT*-1)
                        scroll_time = time.perf_counter()

                
                # 数値表示
                    # 距離
                cv2.putText(img, str(int(distances['l'])), (trig_cv_x, trig_cv_y + 10), font, 0.3, ((
                    255, 144, 30) if distances['l'] >= CLICK_THRESHOLD else (0, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.putText(img, str(int(distances['r'])), (trig_cv_x, trig_cv_y + 20), font, 0.3, ((
                    255, 144, 30) if distances['r'] >= CLICK_THRESHOLD else (0, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.putText(img, str(int(distances['ld'])), (trig_cv_x, trig_cv_y + 30), font, 0.3, ((
                    255, 144, 30) if distances['ld'] >= CLICK_THRESHOLD else (0, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.putText(img, str(int(distances['mu'])), (trig_cv_x, trig_cv_y + 40), font, 0.3, ((
                    255, 144, 30) if distances['mu'] >= CLICK_THRESHOLD else (0, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                cv2.putText(img, str(int(distances['md'])), (trig_cv_x, trig_cv_y + 50), font, 0.3, ((
                    255, 144, 30) if distances['md'] >= CLICK_THRESHOLD else (0, 0, 255)), thickness=1, lineType=cv2.LINE_8)
                    # FPS
                cv2.putText(img, "cameraFPS:"+str(cap_fps), (20, 40),font, 1, (0, 255, 0), thickness=2, lineType=cv2.LINE_8)
                p_un = time.perf_counter()
                fps = str(int(1/(float(p_un)-float(p_a))))
                cv2.putText(img, "FPS:"+fps, (20, 80),font, 1, (0, 255, 0), 2, lineType=cv2.LINE_8)

                # mpDraw.draw_landmarks(
                #     img,
                #     hand_landmarks,
                #     mpHands.HAND_CONNECTIONS,
                #     mpDrawStyles.get_default_hand_landmarks_style(),
                #     mpDrawStyles.get_default_hand_connections_style())
        else:
            if prev_distances['ld'] >= CLICK_THRESHOLD:
                gui.mouseUp(button='left')
            for k in prev_distances.keys():
                prev_distances[k] = 999
        cv2.imshow(WINDOW_NAME, img)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    cap.release()


if __name__ == '__main__':
    main()
