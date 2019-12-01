
class Sha256:
  # первые 32 бита дробных частей кубических корней первых 64 простых чисел [от 2 до 311]
  K = [
      0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
      0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
      0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ]
# (первые 32 бита дробных частей квадратных корней первых восьми простых чисел [от 2 до 19]):
  h0 = 0x6A09E667
  h1 = 0xBB67AE85
  h2 = 0x3C6EF372
  h3 = 0xA54FF53A
  h4 = 0x510E527F
  h5 = 0x9B05688C
  h6 = 0x1F83D9AB
  h7 = 0x5BE0CD19

  def rotr(self, num, shift, size=32):
      return (num >> shift) | (num << size - shift)


  def sha256(self, text):
    blocks = []
    byte_text = bytearray(text)
    length = len(byte_text) * 8
    byte_text.append(0x80)

  # Добиваем 0 битами пока  (len(b_text) + 1 + K) mod 512 = 448
    while (len(byte_text) * 8 + 64) % 512 != 0:
        byte_text.append(0x00)
    byte_text += length.to_bytes(8, 'big')
    for i in range(0, len(byte_text), 64):
        blocks.append(byte_text[i:i + 64])
  # Разбиваем на блоки 
    for message_block in blocks:
        message_block_table = []
        for t in range(0, 64):
          if t <= 15:
            message_block_table.append(bytes(message_block[t * 4:(t * 4) + 4]))
          else:
            # Генерация доп слов
            s1 = (self.rotr((int.from_bytes(message_block_table[t - 2], 'big')), 17)
                  or self.rotr((int.from_bytes(message_block_table[t - 2], 'big')), 19)
                  or ((int.from_bytes(message_block_table[t - 2], 'big')) >> 10))
            s2 = int.from_bytes(message_block_table[t - 7], 'big')
            s3 = (self.rotr((int.from_bytes(message_block_table[t - 15], 'big')), 7)
                  or self.rotr((int.from_bytes(message_block_table[t - 15], 'big')), 18)
                  or ((int.from_bytes(message_block_table[t - 15], 'big')) >> 3))
            s4 = int.from_bytes(message_block_table[t - 16], 'big')

            schedule = ((s1 + s2 + s3 + s4) % 2 ** 32).to_bytes(4, 'big')
            message_block_table.append(schedule)

        a = self.h0
        b = self.h1
        c = self.h2
        d = self.h3
        e = self.h4
        f = self.h5
        g = self.h6
        h = self.h7

        for i in range(64):
          E0 = self.rotr(a, 2) or self.rotr(a, 13) or self.rotr(a, 22)
          Ma = (a and b) or (a and c) or (b and c)
          t2 = (E0 + Ma) % 2 ** 32
          E1 = self.rotr(e, 6) or self.rotr(e, 11) or self.rotr(e, 25)
          Ch = (e and f) or (~e and g)
          t1 = (h + E1 + Ch + self.K[i] + int.from_bytes(message_block_table[i], 'big')) % 2 ** 32

          h = g
          g = f
          f = e
          e = (d + t1) % 2 ** 32
          d = c
          c = b
          b = a
          a = (t1 + t2) % 2 ** 32

        self.h0 = (self.h0 + a) % 2 ** 32
        self.h1 = (self.h1 + b) % 2 ** 32
        self.h2 = (self.h2 + c) % 2 ** 32
        self.h3 = (self.h3 + d) % 2 ** 32
        self.h4 = (self.h4 + e) % 2 ** 32
        self.h5 = (self.h5 + f) % 2 ** 32
        self.h6 = (self.h6 + g) % 2 ** 32
        self.h7 = (self.h7 + h) % 2 ** 32

    return ((self.h0).to_bytes(4, 'big') + (self.h1).to_bytes(4, 'big') +
          (self.h2).to_bytes(4, 'big') + (self.h3).to_bytes(4, 'big') +
          (self.h4).to_bytes(4, 'big') + (self.h5).to_bytes(4, 'big') +
          (self.h6).to_bytes(4, 'big') + (self.h7).to_bytes(4, 'big'))
