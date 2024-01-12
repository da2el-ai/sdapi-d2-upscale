
KohakuNAI で作った画像を自動でアップスケールする。

単体で動作するスプリプトです。
StableDiffusion webui a1111 の機能拡張ではありません。


# Features

- プロンプト変換機能を付ける
  - これが必要で作り始めた

# Install

```
> git clone https://github.com/da2el-ai/sdapi-d2-upscale.git
> cd sdapi-d2-upscale
> python -m venv venv
> .\venv\Scripts\activate
> pip install -r requirements.txt
```

# Usage

まず仮想環境に入る。

```
> .\venv\Scripts\activate
```

`image` フォルダに変換したい画像を入れる

`setting.yml` をイイ感じに書き換える

スクリプトを実行する

```
> python all_upscale.py
```

`output` フォルダにアップスケールされた画像が保存される


