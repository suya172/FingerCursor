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
## 使い方
下記のコマンドを実行して必要なモジュールをインストールした後、`Main.py`を実行

`C`を押して終了
```
pip install -r requirements.txt
```
引数に`--debug`を追加するとデバッグモードになり、マウス操作が行われません
## todo
- ジェスチャー検出でスクロール(?)(人差し指を回す動き等)
- 手ぶれ補正
- コマンドライン引数で指定できる値を増やす
- カーソル移動枠の設定をやりやすくする(ex:縦横比はモニターのそれと同じものに固定して大きさの倍率のみ指定し、位置はあらかじめ決まっているものを番号で指定)
