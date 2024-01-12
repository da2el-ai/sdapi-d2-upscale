import math

# 8の倍数に丸める
def scaleTo8(number, scale):
  number = number * scale
  return 8 * math.floor(number / 8)
