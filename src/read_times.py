import numpy as np

def read_times(filename):

    lines = np.loadtxt(filename, dtype=int, delimiter='|')

    t1 = lines[:, 0]
    t2 = lines[:, 1]
    t3 = lines[:, 2]
    t4 = lines[:, 3]

    return t1, t2, t3, t4


