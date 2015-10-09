__author__ = 'ginezf'
import random
import serial
import janela
import log
import platform
import logging
from mythread import *
from Aquisicaoserial import *


class Amostrador(Threadable):

    def __init__(self, fila):
        Threadable.__init__(self, self.amostragem)
        self.testMode = False   # Todo: Colocar isso num arquivo de configuracao
        self.estado = 0
        self.filtragem = 0
        self.fila = fila
        self.log = log.Log("sensor")

        if platform.system() == 'Windows':
            self.porta = "COM4"
        else:
            self.porta = '/dev/ttyACM0'
        try:
            self.ser = serial.Serial(self.porta, 115200, timeout = 1)
        except serial.SerialException as e:
            print e.message
        except:
            print "Erro na abertura da porta serial %s." % self.porta
            exit()

    def inicia(self):
        startAccessPoint(self.ser)
        getStatus(self.ser)
        status = getStatus(self.ser)
        if status == '\x03':
            self.log.escreve("Aquisicao iniciada.", logging.DEBUG)
            self.estado = 1
            self.start()
        else:
            self.log.escreve("Erro na inicializacao. O protocolo nao esta sincronizado.", logging.ERROR)
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

    def amostragem(self):
        print "Iniciando amostragem"
        n_aq_geral  = 0
        n_aq_janela = 0

        pronto = 0

        x_baixa = []
        y_baixa = []
        z_baixa = []

        x_alta  = []
        y_alta  = []
        z_alta  = []

        frame_atual     = [0, 0, 0]
        frame_n_menos_1 = [0, 0, 0]
        frame_n_menos_2 = [0, 0, 0]

        while self.estado == 1:

            # TODO: Precisamos de um flush aqui para nao processar amostras velhas

            if self.testMode == False:
                resultado = obtem_amostra(self.ser, frame_atual)
            else:
                frame_atual[0] = random.randrange(255)
                frame_atual[1] = random.randrange(255)
                frame_atual[2] = random.randrange(255)
                resultado = True

            if resultado == True:

                n_aq_geral += 1  # atualiza contador geral de amostras

                self.log.escreve("%03d|%03d|%03d|)" % (frame_atual[0], frame_atual[1], frame_atual[2]), logging.DEBUG)

                if (pronto == 0) & (n_aq_geral == 65):
                    pronto = 1

                if self.filtragem & n_aq_geral > 3:
                    frame_atual[0] = (frame_atual[0]+frame_n_menos_1[0]+frame_n_menos_2[0])/3
                    frame_atual[1] = (frame_atual[1]+frame_n_menos_1[1]+frame_n_menos_2[1])/3
                    frame_atual[2] = (frame_atual[2]+frame_n_menos_1[2]+frame_n_menos_2[2])/3
                    pass

                frame_n_menos_2 = frame_n_menos_1
                frame_n_menos_1 = frame_atual

                n_aq_janela += 1

                x_alta.append(frame_atual[0])
                y_alta.append(frame_atual[1])
                z_alta.append(frame_atual[2])

                if n_aq_janela == 64:
                    # Concatena as partes baixa e alta para formar uma janela
                    x = x_baixa + x_alta
                    y = y_baixa + y_alta
                    z = z_baixa + z_alta

                    if pronto == 1:
                        # Cria um objeto janela e insere na lista
                        janela_atual = janela.Janela(128)
                        janela_atual.adiciona_amostra(x,y,z)
                        self.fila.append(janela_atual)

                    # Limpa e transfere as partes
                    del x_baixa[:]
                    del y_baixa[:]
                    del z_baixa[:]
                    x_baixa = x_alta
                    y_baixa = y_alta
                    z_baixa = z_alta
                    del x_alta[:]
                    del y_alta[:]
                    del z_alta[:]

                    n_aq_janela = 0


