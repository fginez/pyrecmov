__author__ = 'ginezf'


class Padrao:

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.caracteristicas = []

    def adiciona_caracteristica(self, valor):
        if self.obtem_quantidade_atual() < self.obtem_quantidade():
            self.caracteristicas.append(valor)
            return True
        else:
            return False

    def obtem_quantidade(self):
        return self.tamanho

    def obtem_quantidade_atual(self):
        return len(self.caracteristicas)

    def obtem_vetor_caracteristicas(self):
        return self.caracteristicas
