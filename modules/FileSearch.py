import glob
import os
from modules.Config import Config


class FileSearch:
    filesDict = dict()

    # ///////////////////////////
    # 特定の拡張子の一覧をリストに追加
    @classmethod
    def searchFile(cls, path: str, ext: str):
        return glob.glob(os.path.join(path, "*." + ext))

    # ///////////////////////////
    # ディレクトリチェック
    # @return ディレクトリ内の画像点数
    @classmethod
    def searchDir(cls, name):
      folder = os.path.join(Config.image_folder, name)

      cls.filesDict[name] = list()
      cls.filesDict[name] = cls.filesDict[name] + cls.searchFile(folder, "png")
      cls.filesDict[name] = cls.filesDict[name] + cls.searchFile(folder, "jpg")
      cls.filesDict[name] = cls.filesDict[name] + cls.searchFile(folder, "webp")

      return len(cls.filesDict[name])


