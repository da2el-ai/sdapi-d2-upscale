import io
import os
import base64
from PIL import Image
from ppretty import ppretty
from modules.Config import Config

class Base64helper:

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

