#!/usr/bin/env python3

from read_times import read_times
import sys
import numpy as np

np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'all': lambda x: str(x)})

t1_pps = np.fromfile(sys.argv[1])
t2_pps = np.fromfile(sys.argv[2])
t = np.fromfile(sys.argv[3])

t = t.reshape(-1, 4)

print(t1_pps)
print(t2_pps)
print(t)


print(len(t1_pps))
print(len(t2_pps))
print(len(t))

print(t1_pps[0], t1_pps[-1])
print(t2_pps[0], t2_pps[-1])
print(t[0], t[-1])

t1_pps_aligned = np.zeros(len(t))
t2_pps_aligned = np.zeros(len(t))

j = 0

t_aligned = np.zeros((len(t), 4))

k = 0

for i in range(len(t)):
    while t[i, 0] - t1_pps[j] > 0.5:
        # Si el t1 esta "adelantado", avanzo en los pps 
        j += 1
    if t[i, 0] > t1_pps[j]:
        t1_pps_aligned[k] = t1_pps[j]
        t_aligned[k] = t[i, :]
        k += 1
    # else skip

t = t_aligned[:k]

print("1 MAX DIFFERENCE T1 :", np.max(np.abs(t[:,0] - t1_pps_aligned)))

k = 0
j = 0

t_aligned = np.zeros((len(t), 4))
t1_pps_aligned_2 = np.zeros(len(t))

for i in range(len(t)):
    while t[i, 1] - t2_pps[j] > 0.5:
        j += 1
    if t[i, 1] > t2_pps[j]:
        t2_pps_aligned[k] = t2_pps[j]
        t_aligned[k] = t[i, :]
        t1_pps_aligned_2[k] = t1_pps_aligned[i]
        k += 1
    # else skip

t_aligned = t_aligned[:k]
t1_pps_aligned_2 = t1_pps_aligned_2[:k]
t2_pps_aligned = t2_pps_aligned[:k]

print("2 MAX DIFFERENCE T1 :", np.max(np.abs(t_aligned[:,0] - t1_pps_aligned_2)))
print("2 MAX DIFFERENCE T2:", np.max(np.abs(t_aligned[:,1] - t2_pps_aligned)))

t1_pps_aligned_2.tofile(sys.argv[4])
t2_pps_aligned.tofile(sys.argv[5])
t_aligned.tofile(sys.argv[6])
