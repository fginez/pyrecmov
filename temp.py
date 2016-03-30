import scipy as sp
import numpy as np

npzfile = np.load("master_array.npz")

print npzfile.files
a = npzfile[npzfile.files[0]]
print a
