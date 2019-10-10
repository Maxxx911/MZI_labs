class Converter:

  def to_bin(self, data):
    array = list()
    for char in data:
      binval = self.bin_value(char, 8)  # Get the char value on one byte
      array.extend([int(x) for x in list(binval)])
    return array

  def bin_value(self, val, bitsize):  # binary value as a string of the given size
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    while len(binval) < bitsize:
      binval = "0" + binval
    return binval

  def to_string(self, data):
    chars = []
    for i in range(len(data) // 8):
      byte = data[i * 8:(i + 1) * 8]
      byte_str = ''.join(map(str, byte))
      chars.append(chr(int(byte_str, 2)))
    return ''.join(chars)

  def int_to_bits(self, n, bits_count):
    bits = []
    for digit in bin(n)[2:]:
      bits.append(int(digit))
    while len(bits) < bits_count:
      bits.insert(0, 0)
    return bits
