import numpy as np  # Pillowの出力をOpenCVで扱えるようにするためにインポート
from PIL import Image, ImageDraw, ImageFont  # 結果の出力の文字列を日本語にするためにインポート
import cv2  # 出力用にインポート
import mediapipe as mp  # Googleの機械学習ライブラリであるmediapipeをインポート
import matplotlib.pyplot as plt  # 指の先端の軌跡をグラフ化するためにインポート

# 親指の先端のx,y座標を格納する配列
cx_thumb = []
cy_thumb = []

# 人差し指の先端のx,y座標を格納する配列
cx_index = []
cy_index = []

# 中指の先端のx,y座標を格納する配列
cx_middle = []
cy_middle = []

# 薬指の先端のx,y座標を格納する配列
cx_ring = []
cy_ring = []

# 小指の先端のx,y座標を格納する配列
cx_pinky = []
cy_pinky = []

fontpath = 'C:\Windows\Fonts\msgothic.ttc'  # 日本語フォントのパス(コードでは、MSゴシック)
font = ImageFont.truetype(fontpath, 30)  # フォントの設定(文字の大きさを30にしている)

cap = cv2.VideoCapture(0)  # webカメラの設定

mpHands = mp.solutions.hands  # mediapipe handsの読み込み
hands = mpHands.Hands()  # Handsインスタンスを生成
mpDraw = mp.solutions.drawing_utils  # mediapipe drawing_utilsの読み込み

while True:
    success, img = cap.read()  # webカメラの映像を読み込み
    img = cv2.flip(img, 1)  # webカメラの映像を左右反転(動かしている手を一致させるため)
    # BGR画像をRGB画像に変換(OpenCVの画像はBGR画像であり推論するためにはRGB画像にする必要があるため)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)  # 手の推論

    # 手のランドマークが検出されたらTrue(if文の中を実行する)、検出されなかったらFalse(if文の中を実行しない)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # 変数handLmsが手のランドマークの配列の間、実行
            # 手のランドマークのリスト(handLms.landmark)の中のすべてのインデックスと要素を取得
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape  # webカメラ画像の幅と高さを取得(チャネルは取得しないので3つ目を_にする)
                # 手のランドマークを補正(lm.xは画像の幅、lm.yは画像の高さで正規化されているのでwebカメラ画像の幅と高さをそれぞれかけることで位置を補正させている)
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:  # ランドマークのインデックスが4(親指の先端)の場合
                    cx_thumb.append(cx)  # 親指の先端のx座標を順次cx_thumbに格納
                    cy_thumb.append(cy)  # 親指の先端のy座標を順次cy_thumbに格納
                    # webカメラの画像の(cx,cy)の座標に青(255,0,0)のサイズが10px、太さが10pxの十字のマーカー(cv2.MARKER_CROSS)をプロット
                    cv2.drawMarker(
                        img, (cx, cy), (255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=10)
                    img_pil = Image.fromarray(img)  # webカメラの映像をPillowで扱える形式に変換
                    # ImageDrawオブジェクトをDraw()メソッドに渡すことで描画の準備をする
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 5), '親指',  fill=(255, 0, 0), font=font, stroke_width=1, stroke_fill=(
                        255, 0, 0))  # 「親指」という文字列を(10,5)の座標に出力(枠線の太さが1px、色が文字色と同一(太字を表現))
                    img = np.array(img_pil)  # OpenCVで扱える形式に変換
                if id == 8:  # ランドマークのインデックスが8(人差し指の先端)の場合
                    cx_index.append(cx)  # 人差し指の先端のx座標を順次cx_indexに格納
                    cy_index.append(cy)  # 人差し指の先端のy座標を順次cy_indexに格納
                    # webカメラの画像の(cx,cy)の座標に緑(0,255,0)のサイズが10px、太さが10pxの十字のマーカー(cv2.MARKER_CROSS)をプロット
                    cv2.drawMarker(
                        img, (cx, cy), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=10)
                    img_pil = Image.fromarray(img)  # webカメラの映像をPillowで扱える形式に変換
                    # ImageDrawオブジェクトをDraw()メソッドに渡すことで描画の準備をする
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 40), '人差し指',  fill=(0, 255, 0), font=font,  stroke_width=1, stroke_fill=(
                        0, 255, 0))  # 「人差し指」という文字列を(10,40)の座標に出力(枠線の太さが1px、色が文字色と同一(太字を表現))
                    img = np.array(img_pil)  # OpenCVで扱える形式に変換
                if id == 12:  # ランドマークのインデックスが12(中指の先端)の場合
                    cx_middle.append(cx)  # 中指の先端のx座標を順次cx_middleに格納
                    cy_middle.append(cy)  # 中指の先端のy座標を順次cy_middleに格納
                    # webカメラの画像の(cx,cy)の座標に赤(0,0,255)のサイズが10px、太さが10pxの十字のマーカー(cv2.MARKER_CROSS)をプロット
                    cv2.drawMarker(
                        img, (cx, cy), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=10)
                    img_pil = Image.fromarray(img)  # webカメラの映像をPillowで扱える形式に変換
                    # ImageDrawオブジェクトをDraw()メソッドに渡すことで描画の準備をする
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 75), '中指',  fill=(0, 0, 255), font=font,  stroke_width=1, stroke_fill=(
                        0, 0, 255))  # 「中指」という文字列を(10,75)の座標に出力(枠線の太さが1px、色が文字色と同一(太字を表現))
                    img = np.array(img_pil)  # OpenCVで扱える形式に変換
                if id == 16:  # ランドマークのインデックスが16(薬指の先端)の場合
                    cx_ring.append(cx)  # 薬指の先端のx座標を順次cx_ringに格納
                    cy_ring.append(cy)  # 薬指の先端のy座標を順次cy_ringに格納
                    # webカメラの画像の(cx,cy)の座標に水色(255,255,0)のサイズが10px、太さが10pxの十字のマーカー(cv2.MARKER_CROSS)をプロット
                    cv2.drawMarker(img, (cx, cy), (255, 255, 0),
                                   markerType=cv2.MARKER_CROSS, markerSize=10, thickness=10)
                    img_pil = Image.fromarray(img)  # webカメラの映像をPillowで扱える形式に変換
                    # ImageDrawオブジェクトをDraw()メソッドに渡すことで描画の準備をする
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 110), '薬指',  fill=(255, 255, 0), font=font,  stroke_width=1, stroke_fill=(
                        255, 255, 0))  # 「薬指」という文字列を(10,110)の座標に出力(枠線の太さが1px、色が文字色と同一(太字を表現))
                    img = np.array(img_pil)  # OpenCVで扱える形式に変換
                if id == 20:  # ランドマークのインデックスが20(小指の先端)の場合
                    cx_pinky.append(cx)  # 小指の先端のx座標を順次cx_pinkyに格納
                    cy_pinky.append(cy)  # 小指の先端のy座標を順次cy_pinkyに格納
                    # webカメラの画像の(cx,cy)の座標に黄色(0,255,255)のサイズが10px、太さが10pxの十字のマーカー(cv2.MARKER_CROSS)をプロット
                    cv2.drawMarker(img, (cx, cy), (0, 255, 255),
                                   markerType=cv2.MARKER_CROSS, markerSize=10, thickness=10)
                    img_pil = Image.fromarray(img)  # webカメラの映像をPillowで扱える形式に変換
                    # ImageDrawオブジェクトをDraw()メソッドに渡すことで描画の準備をする
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 145), '小指',  fill=(0, 255, 255), font=font,  stroke_width=1, stroke_fill=(
                        0, 255, 255))  # 「小指」という文字列を(10,145)の座標に出力(枠線の太さが1px、色が文字色と同一(太字を表現))
                    img = np.array(img_pil)  # OpenCVで扱える形式に変換

    cv2.imshow("Image", img)  # 結果の出力
    if cv2.waitKey(1) & 0xFF == ord('c'):  # キーボードで「c」キーが押されたら
        cv2.destroyWindow('Image')  # 出力結果の画面を閉じる
        break  # 手の推論と結果の出力の処理を終了

plt.plot(cx_thumb, cy_thumb, linestyle="solid",
         color=(0, 0, 1), label="親指")  # 親指の先端の座標の軌跡をグラフ化
plt.plot(cx_index, cy_index, linestyle="dashed", color=(
    0, 1, 0), label="人差し指")  # 人差し指の先端の座標の軌跡をグラフ化
plt.plot(cx_middle, cy_middle, linestyle="dashdot",
         color=(1, 0, 0), label="中指")  # 中指の先端の座標の軌跡をグラフ化
plt.plot(cx_ring, cy_ring, linestyle="dotted", color=(
    0, 1, 1), label="薬指")  # 薬指の先端の座標の軌跡をグラフ化
plt.plot(cx_pinky, cy_pinky, color=(1, 1, 0), label="小指")  # 小指の先端の座標の軌跡をグラフ化
# matplotlibで日本語が使えるように設定
plt.legend(prop={"family": "MS Gothic", "weight": "bold"})
plt.show()  # グラフの表示
