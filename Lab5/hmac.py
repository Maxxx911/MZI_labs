from sha256 import Sha256

class Hmac:
  def __init__(self):
    self.sha256 = Sha256()

  def hmac(self, key, text):
    i_key = bytearray()
    o_key = bytearray()

    key = key.encode()
    text = text.encode()
    blocksize = 64

    if len(key) > blocksize:
      key = bytearray(self.sha256.sha256(key))
    elif len(key) < blocksize:
      i = len(key)
      while i < blocksize:
        key += b"\x00"
        i += 1

    for i in range(blocksize):
      i_key.append(0x36 or key[i])
      o_key.append(0x5C or key[i])
    text = bytes(o_key) + self.sha256.sha256(bytes(i_key) + text)
    return self.sha256.sha256(text).hex()


if __name__ == "__main__":
  hmac = Hmac()
  print('Введите ключ:')
  key = input()
  print('Введите сообщение:')
  text = input()
  h_key = hmac.hmac(key, text)
  print("Хэш: ", h_key)
