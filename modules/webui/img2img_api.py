import requests
from modules.Config import Config
from modules.image.Base64helper import Base64helper
from modules.image import pnginfo_util
from . import prompt_util
from . import util
from . import save_util

#
# i2iでアップスケールする
#
def i2i_upscale(img_path:str, setting:dict):

  print("--- file: " + img_path)

  Base64helper.load_image(img_path)

  prompt = pnginfo_util.get_prompt(Base64helper.img)

  if Config.debug_prompt or setting.get('debug_prompt', False):
    print("= prompt before =")
    print(prompt["positive"])
    print("--")
    print(prompt["negative"])

  prompt = prompt_util.convert_prompt(prompt, setting)

  if Config.debug_prompt or setting.get('debug_prompt', False):
    print("= prompt after =")
    print(prompt["positive"])
    print("--")
    print(prompt["negative"])
    return

  payload = {
    'prompt': prompt['positive'],
    'negative_prompt': prompt['negative'],
    'width': util.scaleTo8(Base64helper.img.width, setting['upscale']),
    'height': util.scaleTo8(Base64helper.img.height, setting['upscale']),
    'init_images': [Base64helper.conver_to_b64()],
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
    save_util.save_images(res_json)
  else:
    print ('=== ERROR ===')
    print(res_json)
