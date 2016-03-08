import scipy as sp

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

filename = "data/sample_database/User1.dat"
data = importa_arquivo(filename)


