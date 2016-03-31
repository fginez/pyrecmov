__author__ = 'ginezf'
from feature_generation import *
import log
import logging
import numpy as np

cfgUseLibSVM = False

class Processador:

    def __init__(self):
        if cfgUseLibSVM:
            self.parametros_norm = carrega_parametros('classifier/features/parametros.txt')
        else:
            self.parametros_norm = importa_parametros("classifier/features/norm_params.npz")
            self.lista_caracteristicas = importa_listacaracteristicas("classifier/features/featuresel_list.npz")
        self.log = log.Log("features")
        pass

    def processa(self, janela):
        x = janela.obtem_eixo("x")
        y = janela.obtem_eixo("y")
        z = janela.obtem_eixo("z")
        vetor = vetor_caracteristicas(x, y, z, len(x))
        if False == cfgUseLibSVM:
            v = np.array(vetor)
            v = v[self.lista_caracteristicas]
            vetor = v.tolist()
        self.log.escreve(vetor, logging.DEBUG)
        return vetor

    def normaliza(self, padrao):
        vetor = normaliza_caracteristica(padrao, self.parametros_norm)
        self.log.escreve(vetor, logging.DEBUG)
        return vetor
