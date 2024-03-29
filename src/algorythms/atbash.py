class Atbash:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', **kwargs):
        self.alph = alph
        array = list(alph)
        array.reverse()
        self.reverse_alph = ''.join(array)

    # функция шифрования
    def encrypt(self, mes):
        encoded = ''
        for l in mes:
            encoded += self.reverse_alph[self.alph.index(l)]
        
        return encoded

    # функция расшифрования
    def decrypt(self, mes):
        decoded = ''
        for l in mes:
            decoded += self.alph[self.reverse_alph.index(l)]
        
        return decoded
