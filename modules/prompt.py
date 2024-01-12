import re


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


# NAI weight を SD weight に変換
def nai_to_sd(prompt):
    RATE = 1.05

    def replace_function(match):
      tag = match.group()
      count = 0

      # 文字列の両端から '{}' を削除
      while tag.startswith(bra_start) and tag.endswith(bra_end):
          tag = tag[1:-1]
          count += 1

      weight = RATE ** count  if weight_type >= 1 else 1 / (RATE ** count)
      return f"({tag}:{weight})"

    weight_type = 1
    bra_start = '{'
    bra_end = '}'
    prompt = re.sub(r'{+[^{}]+}+', replace_function, prompt)

    weight_type = -1
    bra_start = '['
    bra_end = ']'
    prompt = re.sub(r'\[+[^\[\]]+\]+', replace_function, prompt)

    return prompt


# プロンプトを変換
# @param prompt: {positive:str, negative:str}
#
def convert_prompt(prompt:dict, setting:dict):
  positive = prompt['positive'];
  negative = prompt['negative'];

  # print("---------- positive")
  # print(positive)
  # print("---------- negative")
  # print(negative)

  positive = remove_prompt(positive, setting.get('remove_positive_prompt', []))
  positive = replace_prompt(positive, setting.get('replace_positive_prompt', []))
  positive = add_prompt(positive, setting.get('add_positive_prompt', []))

  negative = remove_prompt(negative, setting.get('remove_negative_prompt', []))
  negative = replace_prompt(negative, setting.get('replace_negative_prompt', []))
  negative = add_prompt(negative, setting.get('add_negative_prompt', []))

  if setting.get('convert_nai_weight', False):
    positive = nai_to_sd(positive)
    negative = nai_to_sd(negative)

  # print("---------- positive")
  # print(positive)
  # print("---------- negative")
  # print(negative)

  return {'positive':positive, 'negative':negative}

