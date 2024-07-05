# ORPHE-CORE.py
Happy hacking for ORPHE CORE with python!!

https://github.com/Orphe-OSS/ORPHE-CORE.py/assets/1846131/03c5f199-9a54-4307-a014-56b48d3ba373

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
### 周りのBLEデバイスをスキャンする
コアモジュールを特定のデバイスに接続したい場合は、orphe.connect()の引数にデバイスのアドレスを指定することができます。これを利用するにあたって、特定のコアモジュールのアドレスを知りたい場合は以下を実行して周りのBLEデバイスをすべてスキャンすることができます。
```bash
python scan_ble_devices.py
```

## ドキュメント
  * [ORPHE CORE Python API Reference](https://orphe-oss.github.io/ORPHE-CORE.py/api/orphe_core.html)

### 生成方法
orphe_core.pyのdocstringからドキュメントを生成します。htmlファイルの生成には pdoc3 を利用しています。orphe_core.pyのdocstringを書き換えたり、機能を追加した場合は以下のコマンドでドキュメントを再生成してください。
```bash
pip install pdoc3
pdoc orphe_core --html -o docs/api --force
```

## Compatibility
 * ORPHE CORE 50Hz、200Hzモデルに対応していますが、50Hzモデルではsensor valuesにおける加速度、ジャイロ、クオータニオンのタイムスタンプやシリアル番号、パケット番号は利用することができません。これはファームウェアの仕様によるものです。