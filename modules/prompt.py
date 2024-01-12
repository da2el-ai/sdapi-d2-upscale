

# プロンプトを削除
def remove_prompt(prompt, items):
  for item in items:
    prompt = prompt.replace(item, '')
  return prompt


# プロンプトを追加
def add_prompt(prompt, items):
  prompt = prompt + ',' + ','.join(items)
  return prompt


# プロンプトを置き換え
def replace_prompt(prompt, items):
  for item in items:
    prompt = prompt.replace(item["before"], item["after"])
  return prompt


# def convert_prompt(prompt, setting):

