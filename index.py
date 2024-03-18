import sys, os, argparse
from modules.Config import Config
from modules.FileSearch import FileSearch
from modules import webui


# 総画像数、現在のカウント
countTotal = 0
countNow = 0


# ///////////////////////////
# ディレクトリチェック
def searchDir():
  global countTotal

  # 設定と同じ名前のディレクトリがあるか検索
  # 画像のリストを作る
  for name in Config.setting_list:
    countTotal += FileSearch.searchDir(name)

  # 設定毎に処理を実行
  for name in Config.setting_list:
    # api options があれば実行
    if(Config.setting_list[name].get("api_options", None)):
      webui.option_api.set_options(Config.setting_list[name])

    for imgPath in FileSearch.filesDict[name]:
      webui.img2img_api.i2i_upscale(imgPath, Config.setting_list[name])


# ///////////////////////////
# オプションをチェック
def parseOptions():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug_prompt', action="store_true", help="アップスケールは行わずプロンプト変換の確認のみ")
  parser.add_argument('-c', '--config_file', type=str, help="設定ファイルを指定")
  args = parser.parse_args()

  if(args.config_file):
    Config.setting_file = args.config_file

  if not os.path.exists(Config.setting_file):
    print("設定ファイルがありません")
    sys.exit()
    return

  Config.debug_prompt = args.debug_prompt


# ///////////////////////////
def main():
  parseOptions()

  # 設定ファイルを読み込む
  Config.loadSettingFile(Config.setting_file)

  # ディレクトリ探索して実行
  searchDir()


main()
