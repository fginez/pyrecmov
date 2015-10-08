__author__ = 'ginezf'
import amostrador
import processador
#import classificador
import padrao
import resultado
import registro

def roda_sensor():
    amostras = []
    amostragem = amostrador.Amostrador(amostras)
    processamento = processador.Processador()
    #classificacao = classificador.Classificador()

    amostragem.inicia()
    if amostragem.esta_ativo():
        while True:
            if amostras:    # Verifica lista por novas amostras
                print "Amostra recebida!"

                # Cria registro para armazenar os dados
                r = registro.Registro()
                r.janela = amostras.pop(0)  # Inclui amostras de aceleracao x, y e z
                r.padrao.adiciona_caracteristica(processamento.processa(r.janela))  # Extrai caracteristicas
                r.padrao = processamento.normaliza(r.padrao)  # Normaliza
                #r.resultado = classificacao.classifica(r.padrao)  # Classifica o padrao
                pass
    else:
        print "Erro ao iniciar a amostragem"



"""////////////////////////////////////////////////////////////////////////////
 INICIO DO SCRIPT
////////////////////////////////////////////////////////////////////////////"""
# script para rodar a partir da amostragem do sensor
roda_sensor()
