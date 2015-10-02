from __future__ import division
import numpy
import scipy.stats
from math import log10
from math import sqrt
from datetime import datetime
"""#para teste inicio
#gera semper os mesmos vetores x, y, z com 128 valores de 0 a 255.
import random
random.seed(1)
x,y,z=[],[],[]
w=128
for i in range(1,129):
	x.append(random.randrange(255))
	y.append(random.randrange(255))
	z.append(random.randrange(255))
#para teste fim"""

def calc_curtose(x):
    return scipy.stats.kurtosis(x,fisher=False)

def calc_dp(x):
    o = numpy.std(x,ddof=1)
    return o

def calc_fft(sinal, fa, N):
    fx= numpy.fft.fft(sinal,N,axis=0)/N
    f = fa/2 * numpy.linspace(0,1,(N)/2 +1)
    return f, fx

def calc_em(x,y,z,w):
#verificar se X(i) no matlab=X(i) no python -> nao e, matlab inicia do indice 1.
    comp = len(x)
    em = 0

    f, X = calc_fft(x, 33 ,128)
    f, Y = calc_fft(y,33,128)
    f, Z = calc_fft(z,33,128)

    X_m = 0
    Y_m = 0
    Z_m = 0
    #for i in range(3,comp/2+2):
    for i in range(2,int(comp/2+1)):
        X_m += 2*abs(X[i])**2
        Y_m += 2*abs(Y[i])**2
        Z_m += 2*abs(Z[i])**2
    em = (X_m + Y_m + Z_m)/3
    return em

def calc_entropia(x):
    comp = len(x)
    f, X = calc_fft(x,33,128)
    P=[]
    for i in range(len(X)):
        P.append(2*abs(X[i])**2)
    X_m = 0
    for i in range(2,int(comp/2+1)):
        if P[i]>0:
            res = P[i]*log10(P[i])
            X_m += res
    return -X_m

def calc_media(x):
        return numpy.mean(x,axis=0)

def calc_seqsmovimento(x, tolerancia):
        #Dar credito a Gyllensten
        quant = 1
        for i in range(0,len(x)-1):
                lowi = i
                while abs(x[i]-x[lowi])<tolerancia and lowi>0:
                        lowi-=1
                if quant<(i-lowi):
                        quant = i- lowi
        return quant

def calc_variacao(x):
        return max(x) - min(x)
        
def calc_sma(x,y,z,w):
        sma=0
        for i in range(0,len(x)):
                sma += (abs(x[i]) + abs(y[i]) + abs(z[i]))
        return sma/w

def calc_svm(x,y,z,w):
        svm = 0
        for i in range(0,len(x)):
                svm += ((x[i]**2)+(y[i]**2)+(z[i]**2))
        return sqrt(svm)/w
    
def calc_max_f(x):
        f_x, X = calc_fft(x, 33, 128)

        magX = []
        for i in range(len(X)):
                magX.append(2*abs(X[i])**2)
                
        magX = magX[2:int(len(x)/2 +1)]
        mag, f = max(magX), numpy.argmax(magX)
        f+=3 #versao a atualizada
        #f+=2 #versao antiga
        #como os indices do python funcionam de forma diferente, aqui o valor
        #sera 1 a menos do que no matlab, mas como e um indice, por enquanto
        #deixo assim. Dependendo do uso de f posteriormente talvez tenha que mudar
        return f

def vetor_caracteristicas(x, y, z, w):
        vetor = []
        vetor.append(calc_dp(x))
        vetor.append(calc_variacao(y))
        vetor.append(calc_entropia(x))
        vetor.append(calc_entropia(y))
        vetor.append(calc_em(x,y,z,w))
        vetor.append(calc_dp(y))
        vetor.append(calc_variacao(x))
        vetor.append(calc_seqsmovimento(y, 5))
        vetor.append(calc_max_f(x))
        vetor.append(calc_svm(x,y,z,w))
        vetor.append(calc_seqsmovimento(z, 5))
        vetor.append(calc_seqsmovimento(x, 5))
        vetor.append(calc_max_f(y))
        vetor.append(calc_sma(x,y,z,w))
        vetor.append(calc_media(z))
        vetor.append(calc_variacao(z))
        vetor.append(calc_dp(z))
        vetor.append(calc_media(y))
        vetor.append(calc_media(x))
        return vetor

def time_test(x,y,z,w):
        start = datetime.now()
        vetor = vetor_caracteristicas(x,y,z,w)
        done = datetime.now()
        deltat = done-start
        return deltat.total_seconds()

def carrega_parametros(arquivo):
    arq_param = open(arquivo,'r')
    parametros = []
    for i,linha in enumerate(arq_param):
        dados = linha.split('|')
        md = float(dados[2])
        dp = float(dados[3])
        param = [md,dp]
        parametros.append(param)
    return parametros
    
def normaliza_caracteristica(dados, parametros):
        l = len(dados)
        resultado = []
        #m = numpy.mean(dados,axis=0)
        #dp = numpy.std(dados,ddof=1)
        for i in range(l):
            m = parametros[i][0]
            dp = parametros[i][1]
            res = (dados[i]-m)/dp
            resultado.append(res)
        return resultado

def obtem_janelas(sinal, tamanho_janela, sobreposicao):
        #obtem_janelas Segmenta o sinal fornecido em janelas com sobreposicao
        #Entradas:
        #sinal : strem de dados
        #tamanho: tamanho da janela (128, 256, 512....)
        #sobreposicao: quantidade de amostras superpostas
        #Saida:
        #amostras_janeladas : matriz com as janelas

        #inicializacao das variaveis
        pos_inicio = 0
        pos_fim = pos_inicio+tamanho_janela
        tamanho_sinal = len(sinal)
        janela = []
        amostras_janeladas = []
        
        #verifica se o sinal completa uma janela
        if ( tamanho_sinal < pos_fim ):
                pos_fim = len(sinal)
        #loop de segmentacao dos dados
        while pos_inicio<tamanho_sinal:
                #segmenta os dados
                janela = sinal[pos_inicio:pos_fim]
                
                #verifica se nao completou o tamanho da janela
                if (pos_fim-pos_inicio)<tamanho_janela:
                        for i in range(tamanho_janela - (pos_fim - pos_inicio)):
                                janela.append(0) #completa com zeros
                #atualiza vetor de saida
                amostras_janeladas.append(janela)
                
                #se houver janelamento aqui e o ponto
                #janela(amostras_janeladas)
                
                #atualiza os "ponteiros"
                pos_inicio = pos_inicio+tamanho_janela - sobreposicao
                if (pos_inicio + tamanho_janela) < tamanho_sinal:
                        pos_fim = pos_inicio+tamanho_janela
                else:
                        pos_fim = pos_inicio + (tamanho_sinal - pos_inicio)
                janela = []
        return amostras_janeladas
                
def carrega_dados(arquivo):
        """Abre um arquivo de dados e retorna 3 vetores: x,y,z, com tantos
        valores quanto houver no arquivo."""
        dados = open(arquivo, 'r')
        X=[]
        Y=[]
        Z=[]
        tempos = []
        for i,linha in enumerate(dados):
                listadados = linha.split('|')
                X.append(int(listadados[3]))
                Y.append(int(listadados[4]))
                Z.append(int(listadados[5]))
                tempos.append(listadados[0])
        return X,Y,Z,tempos
        
def carrega_dados2(arquivo):
        """Abre um arquivo de dados e retorna 3 vetores: x,y,z, com tantos
        valores quanto houver no arquivo."""
        dados = open(arquivo, 'r')
        dados.readline()
        X=[]
        Y=[]
        Z=[]
        mov=[]
        for i,linha in enumerate(dados):
                listadados = linha.split('|')
                X.append(int(listadados[5]))
                Y.append(int(listadados[6]))
                Z.append(int(listadados[7]))
                mov.append(int(listadados[8]))
        return X,Y,Z,mov
    
def ativ(arquivo):
    X,Y,Z,mov = carrega_dados2(arquivo)
    ativ = []
    janelas_mov = obtem_janelas(mov,128,64)
    for janelas in janelas_mov:
        tu = []
        tu.append(janelas[0])
        for i in janelas:
            if i in tu:
                pass
            else:
                tu.append(i)
        ativ.append(tu)
    return ativ
            
                    
