import numpy as np

def read_times(filename):

    t = np.fromfile(filename)
    t = t.reshape(-1, 4)

    t1 = t[:, 0]
    t2 = t[:, 1]
    t3 = t[:, 2]
    t4 = t[:, 3]

    return t1, t2, t3, t4


