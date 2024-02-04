# 　設定

import yaml
from ppretty import ppretty

class Config:
    # コマンドライン引数から取得する値
    setting_file = 'setting.yml'
    debug_prompt = False

    # 設定ファイルから取得する値
    webui_url = ''
    image_folder = ''
    image_suffix = ''
    setting_list = {}

    # 設定ファイルを読み込む
    @classmethod
    def loadSettingFile(cls, filepath):

      with open(filepath, "r", encoding="utf-8") as file:

        yaml_value = yaml.safe_load(file)

        # print("-------")
        # print(ppretty(yaml_value))

        cls.webui_url = yaml_value["webui_url"]
        cls.image_folder = yaml_value["image_folder"]
        cls.image_suffix = yaml_value["image_suffix"]
        cls.setting_list = yaml_value["setting_list"]
