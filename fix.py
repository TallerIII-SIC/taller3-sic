#!/usr/bin/env python3

import numpy as np
import sys

t = np.fromfile(sys.argv[1])
t = t.reshape(-1, 4)

# sacar los datos "inconsistentes": t4 < t1 o t3 < t2

t_final = np.zeros((len(t),4))
k = 0
for i in range(len(t)):
#    print(t[i])
    if t[i,3] < t[i,0]:
        print("SACO ",t[i]/1e6)
    elif t[i,2] < t[i,1]:
        print("SACO ",t[i]/1e6)
    else:
        t_final[k] = t[i]
        k += 1

import matplotlib.pyplot as plt

plt.plot(t[:,3]-t[:,0],c='g')
plt.plot(t[:,2]-t[:,1],c='b')
plt.show()

t_final = t_final[:k]

print("SHAPE T FINAL:", t_final.shape)
