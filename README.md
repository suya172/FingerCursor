# FingerCursor
webカメラを使ったマウス操作
## 使い方
### 起動
下記のコマンドを実行して必要なモジュールをインストールした後、`Main.py`を実行

`C`を押して終了
```
pip install -r requirements.txt
```
|**引数**|**説明**|
|----|----|
|--help -h|引数の説明を表示|
|--debug|デバッグモード　マウス操作が行われなくなる|
|--device -d|デバイスを指定|
|-x0|検知枠の左端のx座標|
|-x1|検知枠の右端のx座標|
|-y0|検知枠の上端のy座標|
|-y1|検知枠の下端のy座標|
|--threshold|クリックを検知する距離の閾値|
|--scroll_amount|一度にスクロールする量|
|--cursor_interval|カーソルが動く間隔(秒)|
|--scroll_interval|スクロールする間隔(秒)|
|--cap_width|キャプチャする画像の幅|
|--cap_height|キャプチャする画像の高さ|
### 操作方法
//todo
## 参考サイト
- https://qiita.com/blueman/items/66ef82e3bf03dfca62bb
- https://yoppa.org/mit-design4-22/14113.html
- https://qiita.com/run1000dori/items/301bb63c8a69c3fcb1bd
- https://techceed-inc.com/engineer_blog/6921/
- https://pyautogui.readthedocs.io/en/latest/quickstart.html#
- https://blog.capilano-fw.com/?p=9955
- https://qiita.com/taashi/items/07bf75201a074e208ae5
- https://github.com/takeyamayuki/NonMouse
- https://github.com/Kazuhito00/simple-virtual-mouse-using-mediapipe
## todo
- ジェスチャー検出で緊急停止等
- 手ぶれ補正
- どうやったらぬるぬる動くん？
- 効果音
- GUI化
- 画面をcv2.resizeでコンパクトに(撮影時は大きくしておく)

[Youtubeに進捗を載せています](https://www.youtube.com/playlist?list=PLl4iqWGjZ6vj1kTsjoRaQfSLEqe33ie3V)
