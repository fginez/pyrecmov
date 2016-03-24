import scipy as sp
import numpy as np
import feature_generation as featuregen
from sklearn import svm, grid_search

# Formato do arquivo .dat
# 0 file header (pular)
# 1 Dados da amostra #1
# 2 Dados da amostra #2
# ....

# Formato dos dados da amostra
#     0           1           2          3    4   5   6   7     8        9
# Timestamp | Contador | Ticks jitter | spc | ? | X | Y | Z | Classe | vazio


def importa_arquivo(filename):
    data = sp.genfromtxt(filename, delimiter="|", skip_header=1,  usecols=(5, 6, 7, 8))
    return data


def separa_vetores(data):
    amostras = data[:,0:3:1]
    classes = data[:,3]
    return amostras, classes


def remove_amostras_classe(amostras, classes, remover):
    amostras = amostras[~(classes==remover), :]
    classes  = classes[~(classes==remover)]
    return amostras, classes


def agrupa_classes(amostras, classes):
    grupos = []
    classes_g =  []
    grupo_amostras = []
    classe_g = []
    k = 0
    linhas = amostras.shape[0]
    for i in range(0,linhas):
        if i > 0:
            if classes[i-1] == classes[i]:
                #grupo_amostras.append(amostras[i,:])
                grupo_amostras = np.vstack((grupo_amostras, amostras[i, :]))
                #classe_g.append(classes[i])
                classe_g = np.append(classe_g, classes[i])

                # Tratamento para a ultima linha do arquivo
                if i == (linhas-1):
                    grupos.insert(k, grupo_amostras)
                    classes_g.insert(k, classe_g)

            else:
                grupos.insert(k, grupo_amostras)
                classes_g.insert(k, classe_g)
                grupo_amostras = []
                classe_g = []
                grupo_amostras = np.array(amostras[i, :])
                classe_g = np.array(classes[i])
                k += 1
        else:
            # Primeira amostra
            #grupo_amostras.append(amostras[i,:])
            grupo_amostras = np.array(amostras[i, :])
            #classe_g.append(classes[i])
            classe_g = np.array(classes[i])

    print "agrupa_classes: %d grupos\n" % (k+1)
    return grupos, classes_g


def extrai_janelas(grupo, classes_g, tamanho, sobreposicao):
    janelas = []
    classes_j = []
    len_grupo = grupo.__len__()
    k = 0
    for p in xrange(0, len_grupo, sobreposicao):
        janela = grupo[p:p+min(tamanho, len_grupo-p), :]
        if janela.shape[0] < tamanho:
            return k, janelas, classes_j

        janelas.insert(k, janela)
        classes_j.insert(k, classes_g[p])
        k+=1
    return k, janelas, classes_j

#====================================================================================================
# SCRIPT PARA TREINAMENTO DE MODELO DE SVM (UTILIZANDO A LIBSVM)
#====================================================================================================
# TESTE FUNCIONAL DO SKLEARN SVM
filename = "data/master/master.dat"
#filename = "data/sample_database/window_test.dat"

# Importa o arquivo bruto de amostras
data = importa_arquivo(filename)

# Extrai as matrizes de dados de interesse
amostras, classes = separa_vetores(data)

# Remocao de classes indesejadas (sem classificao / sem movimento definido)
# Sendo:
#        0 - Sem movimento definido
#        9 - Sem classe (isso e' resultado pos uso do classificador pronto)
amostras, classes = remove_amostras_classe(amostras, classes, 0)
amostras, classes = remove_amostras_classe(amostras, classes, 9)

# Agrupamento de dados conforme a classe informada no treinamento
grupos, classes_g = agrupa_classes(amostras, classes)

# Janelamento
janelas = []
classes_j = []
for i in range(0, grupos.__len__()):
    tamanho=128
    sobreposicao=64
    qtd_janelas, janela, classe_j = extrai_janelas(grupos[i], classes_g[i], tamanho, sobreposicao)
    print "grupo[%d](classe %d): %d janelas extraidas" % (i, classes_g[i][0], qtd_janelas)
    if qtd_janelas:
        janelas.append(janela)
        classes_j.append(classe_j)

# Extracao de caracteristicas
caracteristicas = np.array([])
classes = np.array([])

for i in range(0, janelas.__len__()):
    for j in range(0, janelas[i].__len__()):
        x = janelas[i][j][:, 0]
        y = janelas[i][j][:, 1]
        z = janelas[i][j][:, 2]
        vetor = featuregen.vetor_caracteristicas(x,y,z, len(x))
        c     = classes_j[i][j]
        if 0 == len(caracteristicas):
            caracteristicas = np.array([vetor])
            classes = np.array(c)
        else:
            caracteristicas = np.vstack([caracteristicas, vetor])
            classes = np.append(classes, c)


# Embaralhamento da matriz
indices_aleatorios = np.random.permutation(caracteristicas.shape[0])
caracteristicas = caracteristicas[indices_aleatorios, :]
classes = classes[indices_aleatorios]

# Normalizacao
caracteristicas_n, parametros_n = featuregen.gera_normalizacao_caracteristicas(caracteristicas)

# TODO: Porque chegou-se ao numero de 1287 janelas?
# TODO: Fazer um mock com janelas conhecidas para testar o funcionamento do extrator de janelas
print "Tamanho vetor caracteristicas: %d x %d\n" % (caracteristicas_n.shape[0], caracteristicas_n.shape[1])
print "Parametros de normalizacao:\n"
print parametros_n

np.savez("master_array", caracteristicas, parametros_n, caracteristicas_n, classes)

npzfile = np.load("master_array.npz")

# Aqui temos:
# vetor de entrada: caracteristicas_n
# vetor de alvos:   classes

# Montagem da grade de parametros de treinamento
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
svr = svm.SVC(probability=True)
clf = grid_search.GridSearchCV(estimator=svr, param_grid=tuned_parameters)
clf.fit(caracteristicas_n, classes)
print "Score obtido: " + str(clf.best_score_)
s = clf.score(caracteristicas_n, classes)
pass