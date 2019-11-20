import math

class NumberGenerate:

  def generate(self,max):
    num = []
    for i in range(2, max):
      temp = 0
      sqrt_max_num = int(math.sqrt(i)) + 1
      for j in range(2, sqrt_max_num):
        if i % j == 0:
          temp = j
          break
      if temp == 0:
        num.append(i)
    return num
