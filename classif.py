import sys
#from Aquisicaoserial import *
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

def classificar(arquivo):
    """funcao de classificacao feita para os arquivos de dados no novo formato"""
    X,Y,Z = carrega_dados(arquivo)
    janelasX = obtem_janelas(X,128,64)
    janelasY = obtem_janelas(Y,128,64)
    janelasZ = obtem_janelas(Z,128,64)
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

def classificar5(arquivo,sobre):
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
    model = svm_load_model('svm_model2')
    #model = svm_load_model('recmov.model')
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
            
    return classif,atividades

def erros3(arquivo):
    """mesmo que erros() mas utilizando classificar5()"""
    classif, ativ = classificar5(arquivo,64)
    count = 0
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