from random import randint

def text_from_int(n, encoding='ASCII', errors='surrogatepass'):
	return n.to_bytes(
	    (n.bit_length() + 7) // 8, 'big').decode( errors='ignore') or '\0'

class Gamal:
	def __init__(self):
		self.p = 65353
		self.phi = self.p - 1
		self.g = randint(2, self.phi)
		self.x = randint(1, self.p - 1)
		self.y = pow(self.g, self.x, self.p)
		self.open_key = [self.p, self.g, self.y]
		self.k = randint(1, self.p - 1)
		self.a = pow(self.g, self.k, self.p)

	def encrypt(self, text):
		crypt = [self.a]
		for M in text:
			crypt += [(pow(self.y, self.k) * ord(M)) % self.p]
		return crypt
	
	def decrypt(self,  crypt):
		encrypt = ""
		for b in crypt[1::]:
			encrypt+=text_from_int((b * pow(crypt[0], self.p - 1 - self.x, self.p)) % self.p)
		return encrypt

encryptor = Gamal()
text = input('Введите ваш текст:')
crypt = encryptor.encrypt(text)

print("Публичный ключ:",encryptor.open_key)
print("Зашифрованный текст:")

for i in crypt[1::]: 
  print(text_from_int(i))
  
print('\n')
encrypt = encryptor.decrypt(crypt)

print("Закрытый ключ:", encryptor.x)
print("Расшифрованный текст:", encrypt)
