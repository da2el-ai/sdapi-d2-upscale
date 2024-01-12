from modules.Config import Config
from modules.FileSearch import FileSearch
from modules.Webui import Webui

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
    for imgPath in FileSearch.filesDict[name]:
      Webui.i2i_upscale(imgPath, Config.setting_list[name])


# ///////////////////////////
def main():
  # 設定ファイルを読み込む
  Config.loadSettingFile()

  # ディレクトリ探索して実行
  searchDir()


main()
