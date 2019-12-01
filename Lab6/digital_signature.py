from number_generate import NumberGenerate
from hashlib import sha256
import random

class DigitalSignature:
  def is_prime(self, first, second):
    while second != 0:
        first, second = second, first % second
    return first
  
  def mod_inv(self, a, m):
    g, x, y = self.extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

  def extended_gcd(self, aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

  def generate_key_pair(self, p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = self.is_prime(e, phi)
    while g != 1:
      e = random.randrange(1, phi)
      g = self.is_prime(e, phi)
    d = self.mod_inv(e, phi)
    return (e, n), (d, n)

  def encrypt(self, private_key, plain_text):
    key, n = private_key
    #  a^b mod m
    cipher = [pow(ord(char), key, n) for char in plain_text]
    return cipher


  def decrypt(self, public_key, cipher_text):
    key, n = public_key
    #  a^b mod m
    plain = [chr(pow(char, key, n)) for char in cipher_text]
    return ''.join(plain)

  def verify(self, received_hashed, message):
    our_hashed = sha256(message.encode()).hexdigest()
    if received_hashed == our_hashed:
      print("Подлино")
    else:
      print("Были изменения")

if __name__ == "__main__":
  prime = NumberGenerate().generate(1000)
  print(prime)
  while 1:
    prime_str = input("Выберите два числа из представленных выше ").split(",")
    p, q = [int(x) for x in prime_str]
    if (p in prime) and (q in prime):
      break
    else:
      print("Неверное число, чило должно быть простым.")
  dig = DigitalSignature()
  pub_key, private_key = dig.generate_key_pair(p, q)
  print("Приватный ключ:", private_key, "Общедоступный ключ:", pub_key)
  print("Введите сообщение")
  message = input()
  hash = sha256(message.encode()).hexdigest()
  print("Полученный хэш", hash)
  encrypted_msg = dig.encrypt(private_key, hash)
  print("Полученый зашифрованый хэш: ", encrypted_msg, '\n')
  decrypted_msg = dig.decrypt(pub_key, encrypted_msg)
  print("Your decrypted message is:")
  print(decrypted_msg)
  dig.verify(decrypted_msg, message)
