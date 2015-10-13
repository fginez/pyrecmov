__author__ = 'ginezf'
from feature_generation import *
import log
import logging

class Processador:

    def __init__(self):
        self.parametros_norm = carrega_parametros('classifier/features/parametros.txt')
        self.log = log.Log("features")
        pass

    def processa(self, janela):
        x = janela.obtem_eixo("x")
        y = janela.obtem_eixo("y")
        z = janela.obtem_eixo("z")
        vetor = vetor_caracteristicas(x, y, z, len(x))
        self.log.escreve(vetor, logging.DEBUG)
        return vetor

    def normaliza(self, padrao):
        vetor = normaliza_caracteristica(padrao, self.parametros_norm)
        self.log.escreve(vetor, logging.DEBUG)
        return vetor
