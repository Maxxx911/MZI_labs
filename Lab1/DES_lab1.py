from converter import Converter
from file_loader import FileLoader

class DES:
  ENCRYPT = 0
  DECRYPT = 1

  left_rotation_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

  key_permutation_table_1 = [56, 48, 40, 32, 24, 16, 8,
                            0, 57, 49, 41, 33, 25, 17,
                            9, 1, 58, 50, 42, 34, 26,
                            18, 10, 2, 59, 51, 43, 35,
                            62, 54, 46, 38, 30, 22, 14,
                            6, 61, 53, 45, 37, 29, 21,
                            13, 5, 60, 52, 44, 36, 28,
                            20, 12, 4, 27, 19, 11, 3]

  key_permutation_table_2 = [13, 16, 10, 23, 0, 4,
                              2, 27, 14, 5, 20, 9,
                              22, 18, 11, 3, 25, 7,
                              15, 6, 26, 19, 12, 1,
                              40, 51, 30, 36, 46, 54,
                              29, 39, 50, 44, 32, 47,
                              43, 48, 38, 55, 33, 52,
                              45, 41, 49, 35, 28, 31]

  initial_permutation_table = [57, 49, 41, 33, 25, 17, 9, 1,
                                59, 51, 43, 35, 27, 19, 11, 3,
                                61, 53, 45, 37, 29, 21, 13, 5,
                                63, 55, 47, 39, 31, 23, 15, 7,
                                56, 48, 40, 32, 24, 16, 8, 0,
                                58, 50, 42, 34, 26, 18, 10, 2,
                                60, 52, 44, 36, 28, 20, 12, 4,
                                62, 54, 46, 38, 30, 22, 14, 6]

  final_permutation_table = [39, 7, 47, 15, 55, 23, 63, 31,
                            38, 6, 46, 14, 54, 22, 62, 30,
                            37, 5, 45, 13, 53, 21, 61, 29,
                            36, 4, 44, 12, 52, 20, 60, 28,
                            35, 3, 43, 11, 51, 19, 59, 27,
                            34, 2, 42, 10, 50, 18, 58, 26,
                            33, 1, 41, 9, 49, 17, 57, 25,
                            32, 0, 40, 8, 48, 16, 56, 24]

  expansion_table = [31, 0, 1, 2, 3, 4,
                    3, 4, 5, 6, 7, 8,
                    7, 8, 9, 10, 11, 12,
                    11, 12, 13, 14, 15, 16,
                    15, 16, 17, 18, 19, 20,
                    19, 20, 21, 22, 23, 24,
                    23, 24, 25, 26, 27, 28,
                    27, 28, 29, 30, 31, 0
]

  permutation_table = [15, 6, 19, 20, 28, 11, 27, 16,
                      0, 14, 22, 25, 4, 17, 30, 9,
                      1, 7, 23, 13, 31, 26, 2, 8,
                      18, 12, 29, 5, 21, 10, 3, 24]

  SBOX = [
    # S1
    [
      [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    # S2
    [
      [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    # S3
    [
      [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],

    # S4
    [
      [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    # S5
    [
      [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    # S6
    [
      [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],

    # S7
    [
      [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    # S8
    [
      [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
  ]

  def __init__(self, key):
    self.check_key_size(key)
    self.converter = Converter()
    self.file_loader = FileLoader()
    self.key = key # 1 x 56 бит
    self.sub_keys = [] # 16 x 48 бит

  def get_value_from_block(self, block, x):
    return block[x]

  def permutation(self, block, table):
    result = []
    for x in table:
      result.append(self.get_value_from_block(block, x))
    return result

  def left_shift(self, data, n):
    return data[n:] + data[:n]

  def supplement_data(self, data):
    length = len(data)
    if length % 8 != 0:
      data += '0' * (8 - length % 8)
    return data

  def generate_sub_keys(self):
    bits_key = self.converter.to_bin(self.key)
    key = self.permutation(bits_key, self.key_permutation_table_1)
    C_0 = key[:28]
    D_0 = key[28:]

    for shift_count in self.left_rotation_table:
      C_0 = self.left_shift(C_0, shift_count)
      D_0 = self.left_shift(D_0, shift_count)
      new_key = self.permutation(C_0 + D_0, self.key_permutation_table_2)
      self.sub_keys.append(new_key)


  def xor(self, arr1, arr2):
    bit_s = []
    for index, item in enumerate(arr1):
      bit_s.append(arr1[index] ^ arr2[index])
    return bit_s


  def get_blocks(self, data):
    blocks = []
    for i in range(0, len(data), 8):
      blocks.append(data[i: i + 8])
    return blocks


  def trans(self, R):
    B = []
    for i in range(0, len(R), 6):
      B.append(R[i:i + 6])  # b1, b2...b8 векторы по 6 бит
    C = []
    for i in range(8):
      Bi = B[i]
      Si = self.SBOX[i]
      m = int(str(Bi[0]) + str(Bi[5]), 2)  # номер строки
      l = int(''.join(map(str, Bi[1:5])), 2)  # номер столбца
      Bi = Si[m][l]
      Bi = self.converter.int_to_bits(Bi, 4)
      C.extend(Bi)
    return C


  def feistel(self, R, key):
    R = self.permutation(R, self.expansion_table)
    R = self.xor(R, key)
    C = self.trans(R)
    return self.permutation(C, self.permutation_table)

  def crypt(self, blocks, crypt_type=ENCRYPT):
    crypted_data = []
    for block in blocks:
      block = self.converter.to_bin(block)
      block = self.permutation(block, self.initial_permutation_table)
      L = block[:32]
      R = block[32:]
      if crypt_type == self.ENCRYPT:
        i = 0
        j = 1
      else:
        i = 15
        j = -1

      for o in range(16):
        next_L = R[:]
        feistel = self.feistel(R, self.sub_keys[i])
        next_R = self.xor(L, feistel)
        L = next_L
        R = next_R
        i += j

      block = self.permutation(R + L, self.final_permutation_table)
      str_block = self.converter.to_string(block)
      crypted_data.append(str_block)
    return ''.join(crypted_data)

  def encrypt(self, data):
    if not data:
      raise ValueError("Wrong data for encrypting")
    self.generate_sub_keys()
    data = self.supplement_data(data)
    blocks = self.get_blocks(data)
    return self.crypt(blocks)

  def decrypt(self, data):
    blocks = self.get_blocks(data)
    result = self.crypt(blocks, crypt_type=self.DECRYPT)
    return result[:-8] + result[-8:].rstrip('0')


  def check_key_size(self, key):
    if len(key) != 8:
      raise ValueError("Invalid DES key size.")

class DES3:
  def __init__(self, key1, key2, key3):
    self.check_key_size(key1)
    self.check_key_size(key2)
    self.check_key_size(key3)
    self.crypter1 = DES(key1)
    self.crypter2 = DES(key2)
    self.crypter3 = DES(key3)

  def encrypt(self, data):
    data = self.crypter1.encrypt(data)
    data = self.crypter2.encrypt(data)
    return self.crypter3.encrypt(data)

  def decrypt(self, data):
    data = self.crypter3.decrypt(data)
    data = self.crypter2.decrypt(data)
    return self.crypter1.decrypt(data)
  
  def check_key_size(self, key):
    if len(key) != 8:
      raise ValueError("Invalid DES key size.")

def main():
  file_loader = FileLoader()
  data = file_loader.read()
  print("Text from file ", data)

  key1 = "abcd1234"
  key2 = "12345678"
  key3 = "qwerty43"
  decrypted_file_name = "decrypted.txt"


  print(" DES 3 ")
  des3 = DES3(key1=key1, key2=key2, key3=key3)
  encrypted = des3.encrypt(data)
  file_loader.save(encrypted)
  print("Encrypted ", encrypted)

  decrypted = des3.decrypt(encrypted)
  file_loader.save(decrypted, decrypted_file_name)
  print("Decrypted ", decrypted)


if __name__ == '__main__':
  main()
