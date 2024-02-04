import requests
from PIL import Image, PngImagePlugin
from ppretty import ppretty
from modules.Config import Config
from modules.WebuiImage import WebuiImage
from modules.util import scaleTo8
from modules.prompt import convert_prompt

class Webui:
  @classmethod
  def i2i_upscale(cls, img_path:str, setting:dict):

    print("--- file: " + img_path)

    WebuiImage.load_image(img_path)

    prompt = WebuiImage.get_prompt()

    if Config.debug_prompt or setting.get('debug_prompt', False):
      print("= prompt before =")
      print(prompt["positive"])
      print("--")
      print(prompt["negative"])

    prompt = convert_prompt(prompt, setting)

    if Config.debug_prompt or setting.get('debug_prompt', False):
      print("= prompt after =")
      print(prompt["positive"])
      print("--")
      print(prompt["negative"])
      return

    payload = {
      'prompt': prompt['positive'],
      'negative_prompt': prompt['negative'],
      'width': scaleTo8(WebuiImage.img.width, setting['upscale']),
      'height': scaleTo8(WebuiImage.img.height, setting['upscale']),
      'init_images': [WebuiImage.conver_to_b64()],
      **setting['api_params']
    }

    # プロンプトの変換確認のみなら抜ける
    if Config.debug_prompt or setting.get('debug_prompt', False):
      return

    response = requests.post(
      url = f'{Config.webui_url}/sdapi/v1/img2img',
      json = payload
    )
    res_json = response.json()

    if response.status_code == 200:
      cls.save_images(res_json)
    else:
      print ('=== ERROR ===')
      print(res_json)


  #
  # 画像保存
  #
  @classmethod
  def save_images(cls, res_json):
    count = 0

    for img_b64 in res_json['images']:
      pnginfo = cls.get_pnginfo(img_b64)
      WebuiImage.save_from_b64(img_b64, pnginfo, count)
      count += 1


  #
  # png info 作成
  #
  @classmethod
  def get_pnginfo(cls, img_b64):
    payload = {
      "image": "data:image/png;base64," + img_b64
    }

    pnginfo_res = requests.post(url=f'{Config.webui_url}/sdapi/v1/png-info', json=payload)
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", pnginfo_res.json().get("info"))

    return pnginfo
