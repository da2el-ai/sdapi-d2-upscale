from modules.Config import Config
from modules.FileSearch import FileSearch
from modules.Webui import Webui

# ///////////////////////////
# ディレクトリチェック
def searchDir():
  global countTotal

  # 対象ファイル一覧と個数を取得
  countTotal = FileSearch.searchDir('')

  for imgPath in FileSearch.filesDict['']:
    Webui.i2i_upscale(imgPath)


# ///////////////////////////
def main():
  # 設定ファイルを読み込む
  Config.loadSettingFile()

  # ディレクトリ探索して実行
  searchDir()


main()
