
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

下記の場合 `upscale1.5`、`upscale2` が設定名になる。
画像は `image\upscale1.5`、`image\upscale2` に入れる。


```yaml
setting_list:
  # 設定名
  upscale1.5:
    # apiパラメーター
    api_params:
      steps: 30
  # 設定名
  upscale2:
    # apiパラメーター
    api_params:
      steps: 25
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

## アップスケールはせず、プロンプトの変換だけ確認したい

```
> python all_upscale.py -d
または
> python all_upscale.py --debug_prompt
```

## 別の設定ファイルを使いたい

```
> python all_upscale.py -c {設定ファイル}
または　
> python all_upscale.py --config_file {設定ファイル}
```

# 設定項目

`setting.yml` に記述します。
YAMLの書式については検索してください。

## 共通設定

| 設定名 | 設定値 | 説明 |
| --- | --- | --- |
| webui_url | 'http://127.0.0.1:7860' など | webuiのURL |
| image_folder | './image' | 画像フォルダ |
| image_suffix | '_upscale' | ファイル名の最後に付ける識別子 |

## 個別設定

| 設定名 | 設定値 | 説明 |
| --- | --- | -- |
| api_params | |  webui APIのパラメーター。詳細は {webui URL}/docs を参照 |
| upscale | 倍率を数値指定 | アップスケール比率 |
| convert_nai_weight | True / False | NAI weight を SD weight に変換するか |
| remove_weight | True / False | weight 自体を削除するか |
| debug_prompt | True / False | プロンプトの変換だけ確認して、生成は行わない |
| remove_positive_prompt |  | 削除プロンプト |
| replace_positive_prompt | | 置換プロンプト |
| add_positive_prompt | | 追加プロンプト |
| remove_negative_prompt |  | 削除ネガティブプロンプト |
| replace_negative_prompt | | 置換ネガティブプロンプト |
| add_negative_prompt | | 追加ネガティブプロンプト |

## 削除・追加プロンプトについて

`remove_positive_prompt`、`add_positive_prompt`、`remove_negative_prompt`、`add_negative_prompt` の記述方法です。

下記のようにリスト形式で記述します。

```yaml
remove_positive_prompt:
  - "{{{{{{{best quality,amazing quality,very aesthetic,absurdres}}}}}}}"
  - "削除・追加したいプロンプト"
```

## 置換プロンプトについて

`replace_positive_prompt`、`replace_negative_prompt` の記述方法です。

`before` `after` に置換前、置換後を記述します。


```yaml
replace_positive_prompt:
  -
    before: 'smile'
    after: 'angry'
  -
    before: 'red hair'
    after: 'black hair'
```

`type: regexp` を指定すると正規表現が使えます。

```yaml
  -
    type: 'regexp'
    before: '{*artist:xxxx}*,'
    after: ''
```

下記のような結果になります。

```
{{{{artist:xxxx}}}}, 1girl
👇
1girl
```



# アップデート

- 2024.02.04
  - feat: コマンドライン引数 `--debug_prompt` `--config_file` を追加
- 2024.01.18
  - feat: 個別設定項目 `replace_positive_prompt` で `type: 'regexp'` を指定すると正規表現で置換できる
  - feat: 個別設定項目 `remove_weight: True` を指定するとプロンプトのweightを除外できる。AnimagineXL系列でweight指定があると絵が破綻する事への対策
  - feat: 個別設定項目 `debug_prompt: True` を指定するとプロンプトの変換確認だけで、生成を行わない
  - fix: 追加プロンプトが無くても「,」を追加するのを修正
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