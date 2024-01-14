
# SDAPI D2 Upscale

StableDiffusion webui a1111、ComfyUI、NovelAI、KohakuNAI で作った画像を一括でアップスケールする。

単体で動作するスプリプトです。
StableDiffusion webui a1111 の機能拡張ではありません。

- PNGinfoからプロンプトを取得して使用する
- 不要なプロンプトの削除、置換や、プロンプトの追加ができる
- NAI方式の weight を SD方式に変換できる


# 事前準備

StableDiffusion webui a1111 の API機能を使います。

webui の起動オプションに `--api` を付けて起動してください。


# インストール

```
> git clone https://github.com/da2el-ai/sdapi-d2-upscale.git
> cd sdapi-d2-upscale
> python -m venv venv
> .\venv\Scripts\activate
> pip install -r requirements.txt
```


# 設定

`setting.yml` を編集する。
共通設定と個別設定がある。
`setting_list` が個別設定。

```yaml
# webui url
webui_url: http://127.0.0.1:7860

# 画像フォルダ
image_folder: .\image

# ファイル名の最後に付ける識別子
image_suffix: _upscale

setting_list:
  # 設定名（フォルダ名にも使う）
  upscale1.5:
```

## 個別設定

複数の設定を記入することができる。

設定名は画像フォルダ名にもなるので、フォルダに使える名前にする。

下記の場合 `upscale1.5` が設定名になる。
画像は `image\upscale1.5` に入れる。


```yaml
setting_list:
  # 設定名
  upscale1.5:
    # apiパラメーター
    api_params:
      steps: 30
```

`api_params` は StableDiffusion webui a1111 の APIパラメーターを記載する。
詳細は公式ドキュメントを参照。
[http://127.0.0.1:7860/docs](http://127.0.0.1:7860/docs)


# 使い方


まず仮想環境に入る。

```
> .\venv\Scripts\activate
```

`image\{設定名}\` に元となる画像を置く。

スクリプトを実行する。

```
> python all_upscale.py
```

`image\{設定名}\output\` にアップスケールされた画像が保存される。


# アップデート

- 2024.01.14
  - StableDiffusion webui a1111、ComfyUI、NovelAIの画像に対応
  - KohakuNAIのバージョンでPNGinfoが違うようなので対応
- 2024.01.13
  - setting.yml 以外の設定ファイルを使用可能にした
  - api の batch_size に対応
- 2024.01.12
  - プロンプト変換機能追加
- 2024.01.11
  - とりあえず作った