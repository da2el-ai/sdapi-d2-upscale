# 　設定

import yaml
from ppretty import ppretty

class Config:
    webui_url = ''
    image_folder = ''
    output_folder = ''
    image_suffix = ''
    upscale = 1
    add_positive_prompt = ''
    remove_positive_prompt = ''
    replace_positive_prompt = ''
    add_negative_prompt = ''
    remove_negative_prompt = ''
    replace_negative_prompt = ''

    # 設定ファイルを読み込む
    @classmethod
    def loadSettingFile(cls):
      filepath = "setting.yml"

      with open(filepath, "r", encoding="utf-8") as file:

        yaml_value = yaml.safe_load(file)

        print("-------")
        print(ppretty(yaml_value))

        cls.webui_url = yaml_value["webui_url"]
        cls.image_folder = yaml_value["image_folder"]
        cls.output_folder = yaml_value["output_folder"]
        cls.image_suffix = yaml_value["image_suffix"]
        cls.upscale = yaml_value["upscale"]
        cls.add_positive_prompt = yaml_value["add_positive_prompt"]
        cls.remove_positive_prompt = yaml_value["remove_positive_prompt"]
        cls.replace_positive_prompt = yaml_value["replace_positive_prompt"]
        cls.add_negative_prompt = yaml_value["add_negative_prompt"]
        cls.remove_negative_prompt = yaml_value["remove_negative_prompt"]
        cls.replace_negative_prompt = yaml_value["replace_negative_prompt"]

