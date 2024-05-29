# ORPHE-CORE.py
Happy hacking for ORPHE CORE with python!!


> [!IMPORTANT]
> このリポジトリはプライベートです。とりあえずコアモジュールをpythonでいじって遊んで、それをメンバー内で共有できるようにするためのリポジトリです。playgroundとしてまずは使います。ライブラリとして整えていくのはその後の課題です。

## Installation
```bash
git clone https://github.com/Orphe-OSS/ORPHE-CORE.py.git
cd ORPHE-CORE.py
pip install bleak
```
## Compatibility
 * ORPHE CORE v3, 200Hz対応モデルのみで動作を確認しています。
## 動作確認
以下を実行して、センサーの値を取得することができます。とりあえず200Hzで最初の加速度値だけを表示するようにしています。お試しあれ。
```bash
python monitoring_sensor_values.py
```