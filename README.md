# ORPHE-CORE.py
Happy hacking for ORPHE CORE with python!!


> [!IMPORTANT]
> このリポジトリはプライベートです。とりあえずコアモジュールをpythonでいじって遊んで、それをメンバー内で共有できるようにするためのリポジトリです。playgroundとしてまずは使います。徐々にライブラリ orphe_core.py として整備していきます。

## Installation
```bash
git clone https://github.com/Orphe-OSS/ORPHE-CORE.py.git
cd ORPHE-CORE.py
pip install bleak
```

## 動作確認

### LEDを点滅させる
以下を実行して、センサデバイスのLEDが点滅することを確認してください。
終了する場合は`Ctrl+C`で終了できます。
```bash
python blink_led.py
```

### sensor valuesの値を取得する
加速度センサ、ジャイロセンサ、クオータニオンセンサの値を取得することができます。
以下を実行して、sensor valuesの値を取得することができます。
終了する場合は`Ctrl+C`で終了できます。
```bash
python get_sensor_values.py
```

### step analysisの値を取得する
以下を実行して、step analysisの値を取得することができます。
終了する場合は`Ctrl+C`で終了できます。
```bash
python get_step_analysis.py
```

## ドキュメント
  * doc/index.html をブラウザで開くと、ドキュメントを閲覧できます。

### 生成方法
orphe_core.pyのdocstringからドキュメントを生成します。htmlファイルの生成には pdoc3 を利用しています。orphe_core.pyのdocstringを書き換えたり、機能を追加した場合は以下のコマンドでドキュメントを再生成してください。
```bash
pip install pdoc3
pdoc orphe_core --html -o doc --force
```

## Compatibility
 * ORPHE CORE 50Hz、200Hzモデルに対応していますが、50Hzモデルではsensor valuesにおける加速度、ジャイロ、クオータニオンのタイムスタンプやシリアル番号、パケット番号は利用することができません。これはファームウェアの仕様によるものです。

 
## 作業メモ
- [x] ORPHE COREのBLE通信をpythonで行う
- [x] orphe_core.pyでクラス化する
- [x] device informationのキャラクタリスティック対応
- [x] SENSOR VALUESの200Hzキャラクタリスティック対応
- [x] SENSOR VALUESの50Hzキャラクタリスティック対応
- [x] STEP ANALYSISのキャラクタリスティック対応
- [x] ドキュメントの整備
