#!/usr/bin/env python3

import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import time
import read_times
from median_calculator import median_window

def phi_estimation(t1, t2, t3, t4):
    return ((t4-t1)-(t3-t2)) / 2


def linear_reg_single(t, phi):
    f, k, _, _, _ = scipy.stats.linregress(t, phi)
    return f, k


def linear_reg(t, phi, w_length):
    f = np.zeros(len(phi) // w_length)
    k = np.zeros(len(phi) // w_length)
    for i in range(len(phi) // w_length):
        w_t = t[i * w_length:(i + 1) * w_length]
        w_phi = phi[i * w_length:(i + 1) * w_length]
        f[i], k[i] = linear_reg_single(w_t, w_phi)
    return f, k


def arma_filter(f, k, alpha):
    f[1:] = alpha * f[:-1] + (1 - alpha) * f[1:]
    k[1:] = alpha * k[:-1] + (1 - alpha) * k[1:]
    return f, k


class Timer(object):
    def __init__(self):
        self.st = 0

    def start(self):
        self.st = time.time()

    def end(self, msg):
        end = time.time()
        print(msg.format(end - self.st))


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: estimate_phi <times file> <output file>")
        sys.exit(0)

    T_FILE = sys.argv[1]
    O_FILE = sys.argv[2]

    timer = Timer()

    timer.start()

    t = np.fromfile(T_FILE)
    t = t.reshape(-1,4)

    
    t1 = t[:,0]
    t2 = t[:,1]
    t3 = t[:,2]
    t4 = t[:,3]

#    t1, t2, t3, t4 = read_times(T_FILE)
    timer.end("Finished reading data ({:.3f}s)")

    timer.start()
    phi_est = phi_estimation(t1, t2, t3, t4)
    timer.end("Finished Phi estimation ({:.3f}s)")


    print(len(t1))
    print(len(t))

    timer.start()
    phi_med_600 = median_window(phi_est, 600)
    timer.end("Finished Phi median 600 ({:.3f}s)")
    # Corto para que sea justo múltiplo de 60 y despueés sea más fácil y entren ventanas completas

    phi_med_600 = phi_med_600[:len(phi_med_600)//60*60]
    t = range(len(phi_med_600))

    timer.start()
    f, k = linear_reg(t, phi_med_600, 60)
    phi_lin = np.zeros(len(t))

    for i in range(len(t) // 60):
        print(i*60)
        print((i+1)*60)
        print(len(phi_lin))
        phi_lin[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi lin reg 60 ({:.3f}s)")

    timer.start()
    alpha = 0.05
    f, k = arma_filter(f, k, alpha)
    phi_arma = np.zeros(len(t))
    for i in range(len(t) // 60):
        phi_arma[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi ARMA ({:.3f}s)")

#    np.savetxt(O_FILE, phi_arma)
    phi_arma.tofile(O_FILE)
