from number_generate import NumberGenerate
import random

class Rsa:
  
  def gen_rsa_key(self):
    num_generate = NumberGenerate()
    prime = num_generate.generate(1000)
    print(prime[-80:-1])
    while 1:
      prime_str = input("Выберите два числа из представленных выше ").split(",")
      p, q = [int(x) for x in prime_str]
      if (p in prime) and (q in prime):
        break
      else:
        print("Неверное число, чило должно быть простым.")

    N = p * q
    r = (p - 1) * (q - 1)
    r_prime = num_generate.generate(r)
    r_len = len(r_prime)
    e = r_prime[int(random.uniform(0, r_len))]
    d = 0
    for n in range(2,r):
      if (e * n) % r == 1:
        d = n
        break

    return ((N, e), (N, d))

  def encrypt(self, pub_key,origal):
    N, e = pub_key
    return (origal ** e ) % N

  def decrypt(self, pri_key,encry):
    N, d = pri_key
    return (encry ** d) % N

if __name__ == '__main__':

  rsa = Rsa()
  pub_key, pri_key = rsa.gen_rsa_key()
  print("Ваш публичный ключ:",pub_key)
  print("Ваш секретный ключ",pri_key)

  origal_text = input("Введите сообщение: ")
  encrypt_text = [rsa.encrypt(pub_key, ord(x)) for x in origal_text]
  decrypt_text = [chr(rsa.decrypt(pri_key, x)) for x in encrypt_text]

  encrypt_show = "".join([chr(x) for x in encrypt_text])
  decrypt_show = "".join(decrypt_text)

  print("Зашифованый текст: ", encrypt_show)
  print("Оригинальный текст: ", decrypt_show)
