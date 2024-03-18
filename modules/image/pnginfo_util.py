import json
import re
import requests
from PIL import Image, PngImagePlugin
import piexif
import piexif.helper



#
# png info 作成
# @param img_b64: Base64変換された画像
#
def create_pnginfo(img_b64, webui_url):
  payload = {
    "image": "data:image/png;base64," + img_b64
  }

  pnginfo_res = requests.post(url=f'{webui_url}/sdapi/v1/png-info', json=payload)
  pnginfo = PngImagePlugin.PngInfo()
  pnginfo.add_text("parameters", pnginfo_res.json().get("info"))

  return pnginfo


#
# 画像からプロンプトを取り出す
#
# @param imagePath 画像パス
# @return {positive:str, negative:str}
#
def get_prompt(img:Image.Image):

  items = (img.info or {}).copy()
  prompt = {'positive':'', 'negative':''}

  # print("items ///////////////")
  # print(ppretty(items, seq_length=99))

  if "exif" in items:
    exif = img.info['exif']
    exif_data = piexif.load(exif)

    exif_comment = (exif_data or {}).get('Exif', {}).get(piexif.ExifIFD.UserComment, b'')
    comment = piexif.helper.UserComment.load(exif_comment)

    # print("comment ///////////////")
    # print(ppretty(comment, seq_length=99))

    if 'Script: Kohaku NAI Client' in comment:
      (prompt['positive'], prompt['negative']) = __get_prompt_kohaku(comment)

    elif 'Steps: ' in comment:
      (prompt['positive'], prompt['negative']) = __get_prompt_a1111(comment)

  elif "workflow" in items:
    (prompt['positive'], prompt['negative']) = __get_prompt_comfy(items)

  elif items.get("Software", None) == "NovelAI":
    (prompt['positive'], prompt['negative']) = __get_prompt_nai(items)

  return prompt


#
# KohakuNAI 画像からプロンプト取得
#
def __get_prompt_kohaku(comment:str):
  comment = comment.split(', Script: Kohaku NAI', 1)[0]

  # KohakuNAIのバージョンによってPNGinfoが違うぽいので対応
  try:
    json_info = json.loads(comment)

    return (
      json_info.get('input', ''),
      json_info.get('parameters',{}).get('negative_prompt', '')
    )
  except:
    params = re.split(r'Negative prompt: |Steps: ', comment)

    return (
      params[0],
      params[1] if 'Negative prompt: ' in comment else ''
    )


#
# webui a1111 画像からプロンプト取得
#
def __get_prompt_a1111 (comment:str):
  params = re.split(r'Negative prompt: |Steps: ', comment)

  return (
    params[0],
    params[1] if 'Negative prompt: ' in comment else ''
  )


#
# NovelAI 画像からプロンプト取得
#
def __get_prompt_nai(items:dict):
  json_info = json.loads(items["Comment"])

  return (
    json_info.get('prompt', ''),
    json_info.get('uc','')
  )


#
# ComfyUI 画像からプロンプト取得
#
def __get_prompt_comfy(items:dict):
  try:
    json_info = json.loads(items.get('prompt', {}))
  except json.JSONDecodeError:
    return '',''

  if not isinstance(json_info, dict):
    return '',''

  for key, val in json_info.items():
    if 'positive_text' in val['inputs']:
      return (
        val['inputs']['positive_text'],
        val['inputs']['negative_text']
      )
      break

  return '',''
