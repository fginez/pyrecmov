import sys
from Aquisicaoserial import *
from feature_generation import *
#from os import path
#dirname = path.dirname(path.abspath(__file__))
#dirname = path.join(dirname, 'libsvm-3.20/python')
import os
#dirname = os.getcwd()
#dirname = os.path.join(dirname,'libsvm-3.20/python')
#sys.path.append(dirname)
from svmutil import *
from svm import *

def classificar(arquivo,modelo = 'Modelos/pymodel.model'):
    """funcao de classificacao feita para os arquivos de dados no novo formato"""
    X,Y,Z,tempos = carrega_dados(arquivo)
    janelasX = obtem_janelas(X,128,64)
    janelasY = obtem_janelas(Y,128,64)
    janelasZ = obtem_janelas(Z,128,64)
    janelas_tempo = obtem_janelas(tempos,128,64)
    fronteiras_tempo = []
    for i in range(len(janelas_tempo)):
        fronteiras_tempo.append(['',''])
    for i in range(len(janelas_tempo)):
        fronteiras_tempo[i][0]+= str(janelas_tempo[i][0])
        fronteiras_tempo[i][1]+= str(janelas_tempo[i][-1])
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    classif =[]
    model = svm_load_model(modelo)
    for vetor in vetores_caracteristicas:
        classif.append(svm_predict([0],[vetor],model,'-b 1'))
    return classif,fronteiras_tempo
    
    
def classificar2(arquivo,sobre):
    """funcao de classificacao feita para os arquivos .dat do fernando"""
    X,Y,Z,mov = carrega_dados2(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    classif =[]
    model = svm_load_model('svm_model2')
    for vetor in vetores_caracteristicas:
        classif.append(svm_predict([0],[vetor],model,'-b 1'))
    return classif

def classificar3(arquivo,sobre):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado"""
    X,Y,Z,mov = carrega_dados2(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #classif =[]
    model = svm_load_model('svm_model2')
    #for vetor in vetores_caracteristicas:
        #classif.append(svm_predict([0],[vetor],model,'-b 1'))
    #for i in range(len(vetores_caracteristicas)):
        #if len(atividades[i]) == 1:
            #classif.append(svm_predict(atividades[i],[vetores_caracteristicas[i]],model,'-b 1'))
    janelas_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            janelas_a_remover.append(i)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')
            
    return classif,atividades

def erros(arquivo):
    classif, ativ = classificar3(arquivo,64)
    count = 0
    total = len(ativ)
    for i in range(len(ativ)):
        if classif[0][i] != ativ[i]:
            print 'classificou',classif[0][i],'correto',ativ[i]
            count += 1
    print'acertos: %f' %(100*(total-count)/float(total)),'(%d/%d)'%(total-count,total)
    print'erros: %f' %(100*count/float(total)),'(%d/%d)'%(count,total)
    
    
    
def classificar4(arquivo,sobre):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado e que tenham
    movimento tipo 9"""
    X,Y,Z,mov = carrega_dados2(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #classif =[]
    model = svm_load_model('svm_model2')
    #for vetor in vetores_caracteristicas:
        #classif.append(svm_predict([0],[vetor],model,'-b 1'))
    #for i in range(len(vetores_caracteristicas)):
        #if len(atividades[i]) == 1:
            #classif.append(svm_predict(atividades[i],[vetores_caracteristicas[i]],model,'-b 1'))
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            janelas_a_remover.append(i)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index) 
    classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')

    return classif,atividades

def erros2(arquivo):
    """mesmo que erros() mas utilizando classificar4()"""
    classif, ativ = classificar4(arquivo,64)
    count = 0
    total = len(ativ)
    for i in range(len(ativ)):
        if classif[0][i] != ativ[i]:
            #print 'classificou',classif[0][i],'correto',ativ[i]
            count += 1
    print'acertos: %f' %(100*(total-count)/float(total)),'(%d/%d)'%(total-count,total)
    print'erros: %f' %(100*count/float(total)),'(%d/%d)'%(count,total)

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def classificar5(arquivo,sobre, modelo):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado, que tenham
    movimento tipo 9 e removendo 5 segundos antes e depois das trocas de atividades"""
    X,Y,Z,mov = carrega_dados2(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    model = svm_load_model(modelo)
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            if i>0:
                janelas_a_remover.append(i)
            janelas_a_remover.append(i)
            if i<len(atividades)-1:
                janelas_a_remover.append(i+1)
    janelas_a_remover = remove_duplicates(janelas_a_remover)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index) 
    classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')
    #classif = svm_predict(atividades,vetores_caracteristicas,model)
            
    return classif,atividades

def erros3(arquivo, modelo):
    """mesmo que erros() mas utilizando classificar5()"""
    classif, ativ = classificar5(arquivo,64, modelo)
    """count = 0
    total = len(ativ)
    for i in range(len(ativ)):
        if classif[0][i] != ativ[i]:
            #print 'classificou',classif[0][i],'correto',ativ[i]
            count += 1
    print'acertos: %f' %(100*(total-count)/float(total)),'(%d/%d)'%(total-count,total)
    print'erros: %f' %(100*count/float(total)),'(%d/%d)'%(count,total)

print "ERROR STATISTICS"
erros3("all_users_nf.txt")
"""
erros2("User1.dat")
erros3('User1.dat')
erros2('User2.dat')
erros3('User2.dat')
erros2('User2_2.dat')
erros3('User2_2.dat')
erros2('User2_3.dat')
erros3('User2_3.dat')
erros2('User3.dat')
erros3('User3.dat')
"""

###FUNCOES PARA MECHER COM O ARQUIVO all_users_nf.txt APENAS>
def carrega_dados_nf(arquivo):
        """Abre um arquivo de dados e retorna 3 vetores: x,y,z, com tantos
        valores quanto houver no arquivo."""
        dados = open(arquivo, 'r')
        #dados.readline()
        X=[]
        Y=[]
        Z=[]
        mov=[]
        for i,linha in enumerate(dados):
                listadados = linha.split('|')
                X.append(int(listadados[4]))
                Y.append(int(listadados[5]))
                Z.append(int(listadados[6]))
                mov.append(int(listadados[7]))
        return X,Y,Z,mov

def ativ_nf(arquivo):
    X,Y,Z,mov = carrega_dados_nf(arquivo)
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

def classificar_nf(arquivo,modelo,sobre):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado e que tenham
    movimento tipo 9"""
    X,Y,Z,mov = carrega_dados_nf(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ_nf(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #classif =[]
    model = svm_load_model(modelo)
    #for vetor in vetores_caracteristicas:
        #classif.append(svm_predict([0],[vetor],model,'-b 1'))
    #for i in range(len(vetores_caracteristicas)):
        #if len(atividades[i]) == 1:
            #classif.append(svm_predict(atividades[i],[vetores_caracteristicas[i]],model,'-b 1'))
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            janelas_a_remover.append(i)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index) 
    classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')
            
    return classif,atividades

def classificar_nf2(arquivo,model,sobre=64):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado, que tenham
    movimento tipo 9 e removendo 5 segundos antes e depois das trocas de atividades"""
    X,Y,Z,mov = carrega_dados_nf(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ_nf(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #model = svm_load_model('svm_model2')
    modelo = svm_load_model(model)
    """janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            if i>0:
                janelas_a_remover.append(i)
            janelas_a_remover.append(i)
            if i<len(atividades)-1:
                janelas_a_remover.append(i+1)
    janelas_a_remover = remove_duplicates(janelas_a_remover)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)"""
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
        """
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index)"""
    classif = svm_predict(atividades,vetores_caracteristicas,modelo,'-b 1')
    #classif = svm_predict(atividades,vetores_caracteristicas,modelo)
            
    return classif,atividades

def erros_nf(arquivo,model):
    """mesmo que erros() mas utilizando classificar4()"""
    classif, ativ = classificar_nf(arquivo,model,64)
    count = 0
    total = len(ativ)
    for i in range(len(ativ)):
        if classif[0][i] != ativ[i]:
            #print 'classificou',classif[0][i],'correto',ativ[i]
            count += 1
    print'acertos: %f' %(100*(total-count)/float(total)),'(%d/%d)'%(total-count,total)
    print'erros: %f' %(100*count/float(total)),'(%d/%d)'%(count,total)

def erros_nf2(arquivo,model):
    """mesmo que erros() mas utilizando classificar5()"""
    classif, ativ = classificar_nf2(arquivo,model,64)
    """count = 0
    total = len(ativ)
    for i in range(len(ativ)):
        if classif[0][i] != ativ[i]:
            #print 'classificou',classif[0][i],'correto',ativ[i]
            count += 1
    print'acertos: %f' %(100*(total-count)/float(total)),'(%d/%d)'%(total-count,total)
    print'erros: %f' %(100*count/float(total)),'(%d/%d)'%(count,total)
    """
    
def treinar_nf2(arquivo,model,sobre=64):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado, que tenham
    movimento tipo 9 e removendo 5 segundos antes e depois das trocas de atividades"""
    X,Y,Z,mov = carrega_dados_nf(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ_nf(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #model = svm_load_model('svm_model2')
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            if i>0:
                janelas_a_remover.append(i)
            janelas_a_remover.append(i)
            if i<len(atividades)-1:
                janelas_a_remover.append(i+1)
    janelas_a_remover = remove_duplicates(janelas_a_remover)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index) 
    #classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')
    #param = '-c 0.5 -g 0.125 -t 2 -b 1'
    param = '-c 2048 -g 2 -t 2 -b 1'
    modelo = svm_train(atividades,vetores_caracteristicas,param)
    svm_save_model(model,modelo)
    return

def treinar(arquivo,model,sobre=64):
    """funcao de classificacao feita para os arquivos .dat do fernando, mas
    removendo janelas que tenham mais de um tipo de movimento marcado, que tenham
    movimento tipo 9 e removendo 5 segundos antes e depois das trocas de atividades"""
    X,Y,Z,mov = carrega_dados2(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #model = svm_load_model(modelo)
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            if i>0:
                janelas_a_remover.append(i)
            janelas_a_remover.append(i)
            if i<len(atividades)-1:
                janelas_a_remover.append(i+1)
    janelas_a_remover = remove_duplicates(janelas_a_remover)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index) 
    #classif = svm_predict(atividades,vetores_caracteristicas,model,'-b 1')
    #param = '-c 0.5 -g 0.125 -t 2 -b 1'
    param = '-c 2048 -g 2 -t 2 -b 1'
    modelo = svm_train(atividades,vetores_caracteristicas,param)
    svm_save_model(model,modelo)
    return

def criar_problema_nf(arquivo_problema,arquivo='all_users_nf.txt',sobre=64):
    X,Y,Z,mov = carrega_dados_nf(arquivo)
    janelasX = obtem_janelas(X,128,sobre)
    janelasY = obtem_janelas(Y,128,sobre)
    janelasZ = obtem_janelas(Z,128,sobre)
    janelasmov = obtem_janelas(mov, 128, sobre)
    vetores_caracteristicas = []
    param = carrega_parametros('parametros.txt')
    atividades = ativ_nf(arquivo)
    for i in range(len(janelasX)):
        vetornorm = vetor_caracteristicas(janelasX[i],janelasY[i],janelasZ[i],len(janelasX[i]))
        vetornorm = normaliza_caracteristica(vetornorm, param)
        vetores_caracteristicas.append(vetornorm)
    #model = svm_load_model(modelo)
    janelas_a_remover = []
    noves_a_remover = []
    atividades_removidas = []
    vetores_removidos = []
    for i in range(len(atividades)):
        if len(atividades[i]) != 1:
            if i>0:
                janelas_a_remover.append(i)
            janelas_a_remover.append(i)
            if i<len(atividades)-1:
                janelas_a_remover.append(i+1)
    janelas_a_remover = remove_duplicates(janelas_a_remover)
    for index in reversed(janelas_a_remover):
        aremov = atividades.pop(index)
        vremov = vetores_caracteristicas.pop(index)
        atividades_removidas.append(aremov)
        vetores_removidos.append(vremov)
    for i in range(len(atividades)):
        atividades[i]=atividades[i][0]
    for i in range(len(atividades)):
        if atividades[i] == 9:
            noves_a_remover.append(i)
    for index in reversed(noves_a_remover):
        anremov = atividades.pop(index)
        vnremov = vetores_caracteristicas.pop(index)
    problema = open(arquivo_problema,'w')
    for i in range(len(vetores_caracteristicas)):
        problema.write('%d '%(atividades[i]))
        for j in range(len(vetores_caracteristicas[i])):
            problema.write('%d:%f '%(j+1,vetores_caracteristicas[i][j]))
        problema.write('\n')
    problema.close()

def criar_problema():
    pass

def mov(arquivo):
    a, fronteiras_tempo = classificar(arquivo)
    for i in range(len(a)):
        if a[i][0]==[1.0]:
            mov = 'deitado'
        elif a[i][0]==[2.0]:
            mov = 'sentado'
        elif a[i][0]==[3.0]:
            mov = 'em pe'
        elif a[i][0]==[4.0]:
            mov = 'andando'
        elif a[i][0]==[5.0]:
            mov = 'correndo'
        elif a[i][0]==[6.0]:
            mov = 'subindo escada'
        elif a[i][0]==[7.0]:
            mov = 'descendo escada'
        elif a[i][0]==[8.0]:
            mov = 'no computador'
        else:
            mov = 'sem class'
        print fronteiras_tempo[i][0], fronteiras_tempo[i][-1],mov

model = 'Modelos/pymodel.model'
