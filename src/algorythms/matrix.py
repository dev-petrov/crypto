import numpy as np
from random import randint
from rest_framework.serializers import ValidationError

class Matrix:
    def __init__(self, alph='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', keys={}, **kwargs):
        self.alph = alph
        self.matrix = np.array(keys.get('M'))
        # проверяем обратимость матрицы
        if np.linalg.det(self.matrix) == 0:
            raise ValidationError('Матрица необратима')

    def encrypt(self, mes):
        # кодируем сообщение индексами букв в афлавите
        mes = [
            self.alph.index(l) + 1
            for l in mes
        ]
        side = len(self.matrix) # сторона матрицы
        if len(mes) % side != 0: # если не делится на блоки, дописываем символы
            for i in range(side - (len(mes) % side)):
                mes.append(randint(1, len(self.alph)))

        blocks = np.array(mes).reshape(len(mes) // side, side) # разбиваем на блоки

        encrypted = np.array(
            [
                np.dot(self.matrix, block) # матричное умножение
                for block in blocks
            ]
        )

        encrypted = list(map(str, encrypted.reshape(encrypted.shape[0] * encrypted.shape[1])))

        return ' '.join(encrypted)

    def decrypt(self, mes):
        mes = list(map(int, mes.split(' ')))
        side = len(self.matrix)
        matrix = np.linalg.inv(self.matrix) # нахождение обратной матрицы
        blocks = np.array(mes).reshape(len(mes) // side, side) # разбиваем на блоки
        decrypted = np.array(
            [
                np.dot(matrix, block) # матричное умножение
                for block in blocks
            ]
        )
        # декодируем буквы
        decrypted = ''.join([
            self.alph[round(i) - 1]
            for i in decrypted.reshape(decrypted.shape[0] * decrypted.shape[1])
        ])

        return decrypted
