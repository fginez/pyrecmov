import scipy as sp

def importa_arquivo(filename):
    data = sp.genfromtxt(filename, delimiter="|", skip_header=1)
    return data

filename = "data/sample_database/User1.dat"
importa_arquivo(filename)