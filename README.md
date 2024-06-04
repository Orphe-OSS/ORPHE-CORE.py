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
## Compatibility
 * ORPHE CORE v2,3の50Hz、200Hzモデルに対応しています。

## 動作確認
以下を実行して、センサーの値を取得することができます。
終了する場合は`Ctrl+C`で終了できます。
```bash
python get_acc.py
```

## ドキュメント
  * doc/index.html をブラウザで開くと、ドキュメントを閲覧できます。

### 生成方法
orphe_core.pyのdocstringからドキュメントを生成します。htmlファイルの生成には pdoc3 を利用しています。orphe_core.pyのdocstringを書き換えたり、機能を追加した場合は以下のコマンドでドキュメントを再生成してください。
```bash
pip install pdoc3
pdoc orphe_core --html -o doc --force
```

## 作業メモ
- [x] ORPHE COREのBLE通信をpythonで行う
- [x] orphe_core.pyでクラス化する
- [x] device informationのキャラクタリスティック対応
- [x] SENSOR VALUESの200Hzキャラクタリスティック対応
- [x] SENSOR VALUESの50Hzキャラクタリスティック対応
- [ ] STEP ANALYSISのキャラクタリスティック対応
- [ ] ドキュメントの整備
