from rest_framework.serializers import ValidationError
from random import randint

class Cardano:
    def __init__(self, keys={}, **kwargs):
        self.key = keys.get('R')
        self.alph = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        cnt = 0
        # проеряем решетку на отсутствие симметрии
        for i in range(len(self.key)):
            for j in range(len(self.key[i])):
                if self.key[i][j] == 1:
                    cnt += 1
                    if (self.key[i][j] == self.key[i][-(j + 1)] or \
                    self.key[i][j] == self.key[-(i + 1)][j] or \
                    self.key[i][j] == self.key[-(i + 1)][-(j + 1)]):
                        raise ValidationError('Некорректная решетка')
        if cnt != (len(self.key) * len(self.key[0]) // 4):
            raise ValidationError('Некорректная решетка')
    
    # перевернуть по вертикали
    def rotate_vertical(self):
        for i in range(len(self.key)):
            for j in range(len(self.key[i]) // 2):
                self.key[i][j], self.key[i][-(j + 1)] = self.key[i][-(j + 1)], self.key[i][j]

    # перевернуть по горизонтали
    def rotate_horizontal(self):
        for i in range(len(self.key) // 2):
            self.key[i], self.key[-(i + 1)] = self.key[-(i + 1)], self.key[i]

        
    def create_table(self):
        table = []

        for i in range(len(self.key)):
            table.append([])
            for j in range(len(self.key[0])):
                table[i].append('')
            
        return table


    def __encrypt(self, mes):
        encrypted = ''
        max_len = len(self.key) * len(self.key[0])
        # дополняем сообщение, чтобы его длина была равна количеству ячеек ключа
        if len(mes) % max_len != 0:
            for i in range(max_len - len(mes) % max_len):
                mes += self.alph[randint(0, len(self.alph) - 1)]
        
        table = self.create_table()

        l = 0
        for r in range(4):
            for i, row in enumerate(self.key):
                # заполняем таблицу в соответствии с "выколотыми" ячейками
                for j, col in enumerate(row):
                    if int(col) == 1:
                        table[i][j] = mes[l]
                        l += 1
            if r == 0:
                # переворачиваем по диагонали
                self.rotate_horizontal()
                self.rotate_vertical()
                continue
            elif r == 1:
                # переворачиваем по вертикали
                self.rotate_vertical()
            elif r == 2:
                # переворачиваем по диагонали
                self.rotate_horizontal()
                self.rotate_vertical()
            else:
                self.rotate_vertical()

        for row in table:
            for col in row:
                encrypted += col
        
        return encrypted            

    def __decrypt(self, mes):
        decrypted = ''
        
        table = self.create_table()

        l = 0

        # заполняем таблицу
        for i in range(len(self.key)):
            for j in range(len(self.key[0])):
                table[i][j] = mes[l]
                l += 1

        for r in range(4):
            for i, row in enumerate(self.key):
                # считываем сообщение в соответствии с "выколотыми" ячейками
                for j, col in enumerate(row):
                    if int(col) == 1:
                        decrypted += table[i][j]
            if r == 0:
                # переворачиваем по диагонали
                self.rotate_horizontal()
                self.rotate_vertical()
                continue
            elif r == 1:
                # переворачиваем по вертикали
                self.rotate_vertical()
            elif r == 2:
                # переворачиваем по диагонали
                self.rotate_horizontal()
                self.rotate_vertical()
            else:
                self.rotate_vertical()

        return decrypted


    def encrypt(self, mes):
        encrypted = ''
        max_len = len(self.key) * len(self.key[0])
        # разбиваем сообщение на блоки
        blocks_cnt = len(mes) // max_len + 1 if len(mes) % max_len != 0 else len(mes) // max_len
        for i in range(blocks_cnt):
            encrypted += self.__encrypt(mes[i * max_len: i * max_len + max_len])
        
        return encrypted


    def decrypt(self, mes):
        decrypted = ''
        max_len = len(self.key) * len(self.key[0])
        # разбиваем сообщение на блоки
        blocks_cnt = len(mes) // max_len + 1 if len(mes) % max_len != 0 else len(mes) // max_len
        for i in range(blocks_cnt):
            decrypted += self.__decrypt(mes[i * max_len: i * max_len + max_len])

        return decrypted
