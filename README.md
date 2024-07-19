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
カメラに手の平を写すとカーソルが動き始めます
|**動作**|**方法**|
|----|----|
|カーソル移動|手を動かす|
|左クリック|中指を親指に付ける→離す|
|右クリック|人差し指を親指に付ける→離す|
|左ドラッグ|人差し指を親指に付けたまま手を動かす|
|上スクロール|小指を親指に付ける|
|下スクロール|小指の付け根を親指に付ける|

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
- 効果音(?)
- GUI化
- 操作方法に分かりやすいように画像を載せる

[Youtubeに進捗を載せています](https://www.youtube.com/playlist?list=PLl4iqWGjZ6vj1kTsjoRaQfSLEqe33ie3V)
