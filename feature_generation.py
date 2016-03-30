from __future__ import division
import numpy
import scipy.stats
from math import log10
from math import sqrt
from datetime import datetime

"""
  *** Esta faltando a implementacao do filtro media movel para remocao de DC ***
  https://www.researchgate.net/publication/272085935_Accelerometer_Signal_Features_and_Classification_Algorithms_for_Positioning_Applications

  * Funcoes de processamento intermediario
    FFT -> calc_fft
    Norma do sinal -> calc_normasinal

  *	Feature | Portada?
	SMA       calc_sma
	Media     calc_media
	D.P.      calc_dp
	Obliq.    calc_obliq
	Curtose   calc_curtose
    SVM       calc_svm
    E.M.      calc_em
    Entropia  calc_entropia
    Corr.C.   calc_corrcruzada
    Var.      calc_variacao
    S.S.Mov   calc_seqsmovimento
    Max.F     calc_max_f

  * Vetor completo de features
  	x -> Amostras brutas do eixo "x"
  	y -> Amostras brutas do eixo "y"
  	z -> Amostras brutas do eixo "z"
  	w -> Numero de amostras utilizado no janelamento
  	n -> Sinal norma obtido pela funcao calc_normasinal

  	00		calc_sma(x,y,z)
  	01		calc_media(x)
  	02		calc_media(y)
  	03		calc_media(z)
  	04		calc_dp(x)
  	05		calc_dp(y)
  	06		calc_dp(z)
  	07		calc_obliq(x)
  	08		calc_obliq(y)
  	09		calc_obliq(z)
  	10		calc_curtose(x)
  	11		calc_curtose(y)
  	12		calc_curtose(z)
  	13		calc_svm(x,y,z,w)
  	14		calc_em(x,y,z,w)
  	15		calc_corrcruzada(x,y)
  	16		calc_corrcruzada(x,z)
  	17		calc_corrcruzada(y,z)
  	18		calc_variacao(x)
  	19		calc_variacao(y)
  	20		calc_variacao(z)
  	21		calc_entropia(x)
  	22		calc_entropia(y)
  	23		calc_entropia(z)
  	24		[f_x] calc_max_f(x)
  	25		[m_x]
  	26		[f_y] calc_max_f(y)
  	27		[m_y]
  	28		[f_z] calc_max_f(z)
  	29		[m_z]
  	30		calc_seqsmovimento(x)
  	31		calc_seqsmovimento(y)
  	32		calc_seqsmovimento(z)
  	33		calc_media(n)
  	34		calc_dp(n)
  	35		calc_obliq(n)
  	36		calc_curtose(n)
  	37		calc_variacao(n)
  	38		calc_entropia(n)
  	39		calc_seqsmovimento(n)

"""


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

def filtro_media_movel(x, n):
	x_f = []
	for i in range(0, len(x)):
		# Calcula o residuo
		r = 0
		for j in range(0, n):
			# Protecao contra indices negativos
			p = i - j
			if p >= 0:
				r += x[p]
		r = r/n
		x_f.append((x[i] - r))
	return x_f

def calc_normasinal(x,y,z):
	n = []
	for i in range(len(x)):
		n.append(sqrt(x[i]**2 + y[i]**2 + z[i]**2))
	return n


def calc_corrcruzada(x,y):
	return numpy.correlate(x,y)[0]

def calc_curtose(x):
    return scipy.stats.kurtosis(x,fisher=False)

def calc_obliq(x):
	return scipy.stats.skew(x)

def calc_dp(x):
    o = numpy.std(x,ddof=1)
    return o

def calc_fft(sinal, fa, N):
    fx= numpy.fft.fft(sinal,N,axis=0)/N
    f = fa/2 * numpy.linspace(0,1,(N)/2 +1)
    return f, fx

def calc_em(x,y,z,w):
	em = 0
	n = calc_normasinal(x,y,z)
	for i in range(0, len(n)):
		em += n[i]**2
	return em/w

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
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)

        f = int(numpy.argmax(magX))
        mag = magX[f]
        f = f_x[f]

        return f, mag

def calc_vetormagF(x):
        f_x, X = calc_fft(x, 33, 128)
        magX = []
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)
        return magX

def calc_energia_bzero(x):
        f_x, X = calc_fft(x, 33, 128)
        magX = []
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)

        e = 0
        for j in range(0, 16):
            e += magX[j]

        return e/16

def calc_energia_bbaixa(x):
        f_x, X = calc_fft(x, 33, 128)
        magX = []
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)

        e = 0
        for j in range(16, 32):
            e += magX[j]

        return e/16

def calc_energia_bmedia(x):
        f_x, X = calc_fft(x, 33, 128)
        magX = []
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)

        e = 0
        for j in range(32, 48):
            e += magX[j]

        return e/16

def calc_energia_balta(x):
        f_x, X = calc_fft(x, 33, 128)
        magX = []
        ri = int(len(X)/2)-1
        rf = int(len(X))
        for i in range(ri, rf, 1):
                magX.append(2*abs(X[i])**2)

        e = 0
        for j in range(48, 65):
            e += magX[j]

        return e/17

def vetor_caracteristicas(x, y, z, w, filtragem=False):
    if True==filtragem:
        x = filtro_media_movel(x, 3)
        y = filtro_media_movel(y, 3)
        z = filtro_media_movel(z, 3)

    n = calc_normasinal(x, y, z)
    X = calc_vetormagF(x)
    Y = calc_vetormagF(y)
    Z = calc_vetormagF(z)
    f_x, m_x = calc_max_f(x)
    f_y, m_y = calc_max_f(y)
    f_z, m_z = calc_max_f(z)

    vetor = []
    vetor.append(calc_svm(x, y, z, w))
    vetor.append(calc_media(x))
    vetor.append(calc_media(y))
    vetor.append(calc_media(z))
    vetor.append(calc_dp(x))
    vetor.append(calc_dp(y))
    vetor.append(calc_dp(z))
    vetor.append(calc_obliq(x))
    vetor.append(calc_obliq(y))
    vetor.append(calc_obliq(z))
    vetor.append(calc_curtose(x))
    vetor.append(calc_curtose(y))
    vetor.append(calc_curtose(z))
    vetor.append(calc_svm(x,y,z,w))
    vetor.append(calc_em(x,y,z,w))
    vetor.append(calc_corrcruzada(x,y))
    vetor.append(calc_corrcruzada(x,z))
    vetor.append(calc_corrcruzada(y,z))
    vetor.append(calc_variacao(x))
    vetor.append(calc_variacao(y))
    vetor.append(calc_variacao(z))
    vetor.append(calc_entropia(x))
    vetor.append(calc_entropia(y))
    vetor.append(calc_entropia(z))
    vetor.append(f_x)
    vetor.append(m_x)
    vetor.append(f_y)
    vetor.append(m_y)
    vetor.append(f_z)
    vetor.append(m_z)
    vetor.append(calc_seqsmovimento(x, 5))
    vetor.append(calc_seqsmovimento(y, 5))
    vetor.append(calc_seqsmovimento(z, 5))
    vetor.append(calc_media(n))
    vetor.append(calc_dp(n))
    vetor.append(calc_obliq(n))
    vetor.append(calc_curtose(n))
    vetor.append(calc_variacao(n))
    vetor.append(calc_entropia(n))
    vetor.append(calc_seqsmovimento(n, 5))
    vetor.append(calc_obliq(X))
    vetor.append(calc_obliq(Y))
    vetor.append(calc_obliq(Z))
    vetor.append(calc_curtose(X))
    vetor.append(calc_curtose(Y))
    vetor.append(calc_curtose(Z))
    vetor.append(calc_corrcruzada(X,Y))
    vetor.append(calc_corrcruzada(X,Z))
    vetor.append(calc_corrcruzada(Y,Z))
    vetor.append(calc_energia_bzero(x))
    vetor.append(calc_energia_bzero(y))
    vetor.append(calc_energia_bzero(z))
    vetor.append(calc_energia_bzero(n))
    vetor.append(calc_energia_bbaixa(x))
    vetor.append(calc_energia_bbaixa(y))
    vetor.append(calc_energia_bbaixa(z))
    vetor.append(calc_energia_bbaixa(n))
    vetor.append(calc_energia_bmedia(x))
    vetor.append(calc_energia_bmedia(y))
    vetor.append(calc_energia_bmedia(z))
    vetor.append(calc_energia_bmedia(n))
    vetor.append(calc_energia_balta(x))
    vetor.append(calc_energia_balta(y))
    vetor.append(calc_energia_balta(z))
    vetor.append(calc_energia_balta(n))
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

def gera_normalizacao_caracteristicas(dados):
    parametros = []
    dados_normalizados = dados.copy()

    for i in range(0, dados.shape[1]):
        m = numpy.mean(dados[:, i])
        sd = numpy.std(dados[:, i], ddof=1)

        for j in range(0, dados.shape[0]):
            dados_normalizados[j, i] = (dados[j, i] - m) / sd
        p = numpy.array([m, sd])
        if 0 == len(parametros):
            parametros = p
        else:
            parametros = numpy.vstack([parametros, p])

    return dados_normalizados, parametros

def obtem_janelas(sinal, tamanho_janela, sobreposicao):
        #obtem_janelas Segmenta o sinal fornecido em janelas com sobreposicao
        #Entradas:
        #sinal : stream de dados
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
