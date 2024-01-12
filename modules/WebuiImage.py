import json
import io
import os
import base64
from PIL import Image
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
  def save_from_b64(cls, img_b64, pnginfo):
    image = Image.open(io.BytesIO(base64.b64decode(img_b64.split(",",1)[0])))
    output_folder = os.path.join(cls.dir_name, 'output')

    if not os.path.exists(output_folder):
      os.makedirs(output_folder)

    img_path = os.path.join(output_folder, cls.file_name + Config.image_suffix + '.png')
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

    exif_data = cls.img.info['exif']
    exif = piexif.load(exif_data)

    exif_comment = (exif or {}).get('Exif', {}).get(piexif.ExifIFD.UserComment, b'')
    comment = piexif.helper.UserComment.load(exif_comment)

    prompt = {'positive':'', 'negative':''}

    # 生成アプリ毎にプロンプトの取得場所を変える
    if 'input' in comment:
      # input があったら KohakuNAI方式
      comment = comment.split(', Script: Kohaku NAI', 1)[0]
      json_info = json.loads(comment)
      prompt['positive'] = json_info.get('input', '')
      prompt['negative'] = json_info.get('parameters',{}).get('negative_prompt', '')

    return prompt
