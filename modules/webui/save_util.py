from modules.Config import Config
from ..image.Base64helper import Base64helper
from ..image import pnginfo_util


#
# 画像保存
#
def save_images(res_json):
  count = 0

  for img_b64 in res_json['images']:
    pnginfo_data = pnginfo_util.create_pnginfo(img_b64, Config.webui_url)
    Base64helper.save_from_b64(img_b64, pnginfo_data, count)
    count += 1

