
class FileLoader:

  def save(self, data, path='result.txt'):
    with open(path, 'w', encoding="utf-8") as file:
      file.write(data)

  def read(self, path="text.txt"):
    with open(path, 'rb') as file:
      data = file.read().decode()
      return data

