# FingerCursor
webカメラを使ったマウス操作
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
## 使い方
下記のコマンドを実行して必要なモジュールをインストールした後、`Main.py`を実行

`C`を押して終了
```
pip install -r requirements.txt
```
引数に`--debug`を追加するとデバッグモードになり、マウス操作が行われません
## todo
- ジェスチャー検出で緊急停止等
- 手ぶれ補正
- どうやったらぬるぬる動くん？
- 効果音
- GUI化
- 画面をcv2.resizeでコンパクトに(撮影時は大きくしておく)
