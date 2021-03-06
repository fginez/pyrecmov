__author__ = 'ginezf'
cfgUsingLibSVM = False

import resultado
import os
import log
import logging
import math
if cfgUsingLibSVM:
    from svmutil import *
    from svm import *
else:
    from sklearn.externals import joblib

class Classificador:

    def __init__(self):
        self.model = None
        if cfgUsingLibSVM:
            self.model = svm_load_model('classifier/model/pymodel.model')  # TODO: Colocar isso num arquivo de configuracao
        else:
            self.model = joblib.load("classifier/model/scikit-learn-svm-model.pkl")
        self.log = log.Log("svm")
        pass

    def classifica(self, padrao):
        r = resultado.Resultado()

        if cfgUsingLibSVM:
            svm_result = svm_predict([0], padrao.obtem_vetor_caracteristicas(), self.model, '-b 1')
            Classe = svm_result[0][0]
            Acc = svm_result[1][0]
            Prob = svm_result[2][0]
            Prob_classe = Prob[self.encontra_indice(Classe)]
            self.log.escreve("Saida LibSVM > Classe=%d Prob=%f" % (Classe, Prob_classe), logging.DEBUG)
        else:
            Acc = 0
            Classe = self.model.predict(padrao.obtem_vetor_caracteristicas())
            Prob = self.model.predict_proba(padrao.obtem_vetor_caracteristicas())
            Classe = int(Classe)
            Prob = Prob[0]
            Prob_classe = Prob[Classe-1]

        # Pos processamento da saida da SVM
        Pos_Classe = self.pos_classificacao(Classe, Prob)

        # Cria objeto de resultado com os valores obtidos
        r.det_classe(Pos_Classe)
        r.det_acc(Acc)
        r.det_prob(Prob)
        r.det_prob_classe(Prob_classe)

        return r
        pass

    def encontra_indice(self, classe):

        # A sequencia de labels e dada por: (visto no model utilizado)
        # TODO: Como automatizar essa busca?
        # label 2 4 6 5 1 3 7 8
        lista_label = [2, 4, 6, 5, 1, 3, 7, 8]
        for x in lista_label:
            if x == classe:
                return lista_label.index(x)
        return -1
        pass

    def pos_classificacao(self, classe, vetor_prob):
        # TODO: Elaborar melhores regras de pos processamento
        limiar = 0.50
        if cfgUsingLibSVM:
            Prob_classe = vetor_prob[self.encontra_indice(classe)]
        else:
            Prob_classe = vetor_prob[classe-1]
        if Prob_classe < limiar:
            classe = 9 # Nao reconhecido
        self.log.escreve("Saida Pos_Classe > Classe=%d Prob=%f (limiar=%f)" % (classe, Prob_classe, limiar), logging.DEBUG)
        return classe

    def traduz_classe(self, classe):
        if classe == 1:
            return "Deitado"
        elif classe == 2:
            return "Sentado"
        elif classe == 3:
            return "Em pe"
        elif classe == 4:
            return "Andando"
        elif classe == 5:
            return "Correndo"
        elif classe == 6:
            return "Subindo escada"
        elif classe == 7:
            return "Descendo escada"
        elif classe == 8:
            return "Trabalhando no computador"
        else:
            return "---"
