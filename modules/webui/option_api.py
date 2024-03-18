import requests
from modules.Config import Config

#
# オプション設定
#
def set_options(setting:dict):
  payload = setting['api_options']

  response = requests.post(
    url = f'{Config.webui_url}/sdapi/v1/options',
    json = payload
  )
  res_json = response.json()

  if response.status_code == 200:
    return True
  else:
    print ('=== ERROR ===')
    print(res_json)
    return False

