__author__ = 'ginezf'
import amostrador
import padrao
import resultado
import registro

def roda_sensor():
    amostras = []
    amostragem = amostrador.Amostrador(amostras)

    amostragem.inicia()
    if amostragem.esta_ativo():
        while True:
            if amostras:
                print "Amostra recebida!"

    else:
        print "Erro ao iniciar a amostragem"



"""////////////////////////////////////////////////////////////////////////////
 INICIO DO SCRIPT
////////////////////////////////////////////////////////////////////////////"""
# script para rodar a partir da amostragem do sensor
roda_sensor()
