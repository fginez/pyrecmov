__author__ = 'ginezf'


class Resultado:

    def __init__(self):
        self.classe = 0
        self.acc = []
        self.prob = []

    def det_classe(self, classe):
        self.classe = classe

    def det_acc(self, acc):
        self.acc = acc

    def det_prob(self, prob):
        self.prob = prob

    def obtem_classe(self):
        return self.classe

    def obtem_acc(self):
        return self.acc

    def obtem_prob(self):
        return self.prob
