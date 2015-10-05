__author__ = 'ginezf'
import thread
import serial
from Aquisicaoserial import *


class Amostrador(thread.Thread):

    def __init__(self):
        thread.Thread.__init__(self, self.amostragem)
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
        self.sobreposicao = 0
        self.estado = 0
        self.pronto = 0
        self.dt_medio_aq = 0
        self.f_aq = 0
        self.t_aq = 0
        pass

    def inicia(self):
        self.estado = 1
        self.start()
        pass

    def finaliza(self):
        self.estado = 0
        self.join()
        pass

    def amostragem(self):
        janela_baixa = []
        janela_alta = []
        n_amostras = 0

        while self.estado == 1:
            amostra = []
            resultado = obtem_amostra(self.ser, amostra)
            if resultado == True:
                janela_alta.append(amostra)
                n_amostras += 1

                if n_amostras == self.sobreposicao:
                    pass

                pass

    def esta_ativo(self):
        if 0 == self.estado:
            return False
        else:
            return True
