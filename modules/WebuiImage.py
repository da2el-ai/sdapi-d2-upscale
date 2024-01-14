import json
import io
import os
import re
import base64
from PIL import Image
from ppretty import ppretty
import piexif
import piexif.helper
from modules.Config import Config

class WebuiImage:

  file_name: str
  dir_name: str
  img = Image.new('RGB', (100,100), 'white')

  #
  # 画像読み込み
  #
  @classmethod
  def load_image(cls, img_path:str):
    cls.dir_name, cls.file_name = os.path.split(img_path)
    cls.file_name = os.path.splitext(cls.file_name)[0]
    cls.img = Image.open(img_path)


  #
  # base64から画像を保存
  #
  @classmethod
  def save_from_b64(cls, img_b64, pnginfo, count=0):
    image = Image.open(io.BytesIO(base64.b64decode(img_b64.split(",",1)[0])))
    output_folder = os.path.join(cls.dir_name, 'output')

    if not os.path.exists(output_folder):
      os.makedirs(output_folder)

    img_path = os.path.join(output_folder, f"{cls.file_name}{Config.image_suffix}_{count}.png")
    image.save(img_path, pnginfo=pnginfo)


  #
  # i2i用にテキスト変換
  #
  @classmethod
  def conver_to_b64(cls):
    with io.BytesIO() as buffer:
      cls.img.save(buffer, format='PNG')
      buffer = base64.b64encode(buffer.getvalue()).decode()

    return buffer


  #
  # 画像からプロンプトを取り出す
  #
  # @param imagePath 画像パス
  # @return {positive:str, negative:str}
  #
  @classmethod
  def get_prompt(cls):

    items = (cls.img.info or {}).copy()
    prompt = {'positive':'', 'negative':''}

    # print("items ///////////////")
    # print(ppretty(items, seq_length=99))

    if "exif" in items:
      exif = cls.img.info['exif']
      exif_data = piexif.load(exif)

      exif_comment = (exif_data or {}).get('Exif', {}).get(piexif.ExifIFD.UserComment, b'')
      comment = piexif.helper.UserComment.load(exif_comment)

      # print("comment ///////////////")
      # print(ppretty(comment, seq_length=99))

      if 'Script: Kohaku NAI Client' in comment:
        (prompt['positive'], prompt['negative']) = cls.__get_prompt_kohaku(comment)

      elif 'Steps: ' in comment:
        (prompt['positive'], prompt['negative']) = cls.__get_prompt_a1111(comment)

    elif "workflow" in items:
      (prompt['positive'], prompt['negative']) = cls.__get_prompt_comfy(items)

    elif items.get("Software", None) == "NovelAI":
      (prompt['positive'], prompt['negative']) = cls.__get_prompt_nai(items)

    return prompt

  #
  # KohakuNAI 画像からプロンプト取得
  #
  @classmethod
  def __get_prompt_kohaku(cls, comment:str):
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
  @classmethod
  def __get_prompt_a1111(cls, comment:str):
    params = re.split(r'Negative prompt: |Steps: ', comment)

    return (
      params[0],
      params[1] if 'Negative prompt: ' in comment else ''
    )

  #
  # NovelAI 画像からプロンプト取得
  #
  @classmethod
  def __get_prompt_nai(cls, items:dict):
    json_info = json.loads(items["Comment"])

    return (
      json_info.get('prompt', ''),
      json_info.get('uc','')
    )

  #
  # ComfyUI 画像からプロンプト取得
  #
  @classmethod
  def __get_prompt_comfy(cls, items:dict):
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
