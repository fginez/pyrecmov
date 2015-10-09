__author__ = 'ginezf'
import amostrador
import processador
import classificador
import padrao
import resultado
import registro

def roda_sensor():
    amostras = []  # lista para recebimento de amostras
    registros =[]  # lista de armazenamento dos resultados

    # Instancia objetos de execucao
    amostragem = amostrador.Amostrador(amostras)
    processamento = processador.Processador()
    classificacao = classificador.Classificador()

    amostragem.inicia()
    if amostragem.esta_ativo():
        while True:
            if amostras:    # Verifica lista por novas amostras
                # Cria registro para armazenar os dados
                r = registro.Registro()
                r.janela = amostras.pop(0)  # Inclui amostras de aceleracao x, y e z
                vetor = processamento.processa(r.janela)  # Extrai caracteristicas
                vetor = processamento.normaliza(vetor)    # Normaliza

                r.padrao = padrao.Padrao(19)  # Cria objeto de padrao
                r.padrao.adiciona_caracteristica(vetor)  # Armazena padrao gerado

                r.resultado = classificacao.classifica(r.padrao)  # Classifica o padrao

                registros.append(r)
                pass
    else:
        print "Erro ao iniciar a amostragem"



"""////////////////////////////////////////////////////////////////////////////
 INICIO DO SCRIPT
////////////////////////////////////////////////////////////////////////////"""
# script para rodar a partir da amostragem do sensor
roda_sensor()
