import scipy as sp
import numpy as np

a = np.array([0])
for x in range(1, 5, 1):
    a = np.append(a, x)

b = np.array(a.tolist())

print a
print b