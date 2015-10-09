__author__ = 'ginezf'
import resultado
import os
import log
import logging
import math
from svmutil import *
from svm import *

class Classificador:

    def __init__(self):
        self.model = None
        self.model = svm_load_model('classifier/model/svm_model2')
        self.log = log.Log("svm")
        pass

    def classifica(self, padrao):
        r = resultado.Resultado()

        svm_result = svm_predict([0], padrao.obtem_vetor_caracteristicas(), self.model, '-b 1')
        Classe = svm_result[0][0]
        r.det_classe(Classe)

        Acc = svm_result[1][0]
        r.det_acc(Acc)

        Prob = svm_result[2][0]
        r.det_prob(Prob)

        Prob_classe = Prob[self.encontra_indice(Classe)]
        self.log.escreve("Classe=%d Prob=%f" % (Classe, Prob_classe), logging.DEBUG)
        return r
        pass

    def encontra_indice(self, classe):

        # A sequencia de labels e dada por: (visto no model utilizado)
        # TODO: Como automatizar essa busca?
        # label 2 4 6 5 1 3 7 8
        lista_label = [2,4,6,5,1,3,7,8]
        for x in lista_label:
            if x == classe:
                return lista_label.index(x)
        pass