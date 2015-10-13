__author__ = 'ginezf'


class Resultado:

    def __init__(self):
        self.classe = 0
        self.prob_classe = 0.0
        self.acc = []
        self.prob = []
        self.nome = []

    def det_classe(self, classe):
        self.classe = classe

    def det_acc(self, acc):
        self.acc = acc

    def det_prob(self, prob):
        self.prob = prob

    def det_nome(self, nome):
        self.nome = nome

    def det_prob_classe(self, prob):
        self.prob_classe = prob

    def obtem_classe(self):
        return self.classe

    def obtem_acc(self):
        return self.acc

    def obtem_prob(self):
        return self.prob

    def obtem_nome(self):
        return self.nome

    def obtem_prob_classe(self):
        return self.prob_classe