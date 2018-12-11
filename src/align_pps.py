#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import numpy as np



def align_pps(t1, t2):
    t1_f = np.zeros(min(len(t1), len(t2)))
    t2_f = np.zeros(min(len(t1), len(t2)))

    i = 0
    j = 0
    k = 0

    # Suponemos que la diferencia inicial es de menos de 0.5 segundos

    initial_i = 0
    initial_j = 0
    
    while i < len(t1) and j < len(t2):
        if t1[i] - t2[j] > 0.5e6:
            j += 1
        elif t1[i] - t2[j] < -0.5e6:
            i += 1
        else:
            initial_i = i
            initial_j = j
            break

#    print("initial diff: ", t1[initial_i]-t2[initial_j])

    t1 = t1[initial_i:]
    t2 = t2[initial_j:]

    prev_diff = t1[0] - t2[0]

    while i < len(t1) and j < len(t2):
        diff = t1[i] - t2[j]

        if diff > prev_diff + 0.5e6:
            # el t1 esta adelantado, paso al siguiente t2
            j += 1
        elif diff < prev_diff - 0.5e6:
                 # el t1 esta atrasado, paso al siguiente t1
            i += 1
        else:
            t1_f[k] = t1[i]
            t2_f[k] = t2[j]
            prev_diff = diff
            k += 1
            i += 1
            j += 1

    t1_f = t1_f[:k]
    t2_f = t2_f[:k]

    return t1_f, t2_f


if __name__ == "__main__":


    t1 = np.fromfile(sys.argv[1])
    t2 = np.fromfile(sys.argv[2])

    T1_OUT_FILE = sys.argv[3]
    T2_OUT_FILE = sys.argv[4]

    t1_f, t2_f = align_pps(t1, t2)

    maxdiff = np.max(t2_f - t1_f)

    t1_f.tofile(T1_OUT_FILE)
    t2_f.tofile(T2_OUT_FILE)

    print("MAX DIFFERENCE:", maxdiff)
    print("LENGTH: ", len(t2_f))
