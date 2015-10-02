__author__ = 'ginezf'


class Janela:

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.a = 0
        self.x = []
        self.y = []
        self.z = []

    def adiciona_amotra_array(self, amostra_array):
        if self.obtem_tamanho_atual() < self.obtem_tamanho():
            self.x.append(amostra_array[0])
            self.y.append(amostra_array[1])
            self.z.append(amostra_array[2])
            return True
        else:
            return False

    def adiciona_amostra(self, x, y, z):
        if self.obtem_tamanho_atual() < self.obtem_tamanho():
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
            return True
        else:
            return False

    def obtem_eixo(self, eixo):
        if eixo == 'x':
            return self.x
        elif eixo == 'y':
            return self.y
        elif eixo == 'z':
            return self.z
        else:
            return []

    def obtem_janela(self):
        return self.x, self.y, self.z

    def obtem_atividade(self):
        return self.a

    def obtem_tamanho(self):
        return self.tamanho

    def obtem_tamanho_atual(self):
        return len(self.x)