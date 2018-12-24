#!/usr/bin/env python3
import sys
import numpy as np

# Esto es para que no muestre los números con notación científica

np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# txt
# t = np.loadtxt(sys.argv[1], delimiter='|')

# binary
t = np.fromfile(sys.argv[1])

t = t.reshape(-1, 4)

t_final = np.zeros((int(np.round(t[-1, 0]-t[0, 0] + 2)), 4))

j = 0

prev = float('inf'), 0, 0, 0

for t1, t2, t3, t4 in t:
    if t1 - prev[0] > 1.1:
        num_missing_seconds = int(np.round(t1-prev[0]-1))
        t_final[j:j+num_missing_seconds + 1,
                0] = np.linspace(prev[0], t1, num_missing_seconds + 2)[1:]
        t_final[j:j+num_missing_seconds + 1,
                1] = np.linspace(prev[1], t2, num_missing_seconds + 2)[1:]
        t_final[j:j+num_missing_seconds + 1,
                2] = np.linspace(prev[2], t3, num_missing_seconds + 2)[1:]
        t_final[j:j+num_missing_seconds + 1,
                3] = np.linspace(prev[3], t4, num_missing_seconds + 2)[1:]

        j += num_missing_seconds + 1
    else:
        t_final[j, :] = [t1, t2, t3, t4]
        j += 1
    prev = t1, t2, t3, t4

t_final = t_final[:j, :]

t_final.tofile(sys.argv[2])
