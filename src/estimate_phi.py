#!/usr/bin/env python3

import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from timer import Timer
from read_times import read_times
from median_calculator import median_window


def phi_estimation(t1, t2, t3, t4):
    return (t1-t2-t3+t4) / 2


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

def interpolate_missing_values(t1,phi_est):
    t1_ok = np.zeros(int(np.round(t1[-1]/1e6 - t1[0]/1e6 + 2)))
    phi_est_ok = np.zeros(int(np.round(t1[-1]/1e6 - t1[0]/1e6 + 2)))

    j = 0

    for i in range(len(t1)):
        # se salteo un segundo
        if t1[i] - t1[i-1] > 1.1e6:
            num_missing_seconds = int(np.round(t1[i]/1e6 - t1[i-1]/1e6 - 1))
            t1_ok[j:j+num_missing_seconds +
                  1] = np.linspace(t1[i-1], t1[i], num_missing_seconds + 2)[1:]
            phi_est_ok[j:j+num_missing_seconds+1] = np.linspace(
                phi_est[i-1], phi_est[i], num_missing_seconds + 2)[1:]
            j += num_missing_seconds + 1
        else:
            t1_ok[j] = t1[i]
            phi_est_ok[j] = phi_est[i]
            j += 1

    return t1_ok[:j], phi_est_ok[:j]


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: estimate_phi <times file> <output file> <time 1 output>")
        sys.exit(0)

    T_FILE = sys.argv[1]
    O_FILE = sys.argv[2]
    T1_OUT_FILE = sys.argv[3]
    timer = Timer()

    timer.start()

    t1, t2, t3, t4 = read_times(T_FILE)
    timer.end("Finished reading data ({:.3f}s)")

    timer.start()
    phi_est = phi_estimation(t1, t2, t3, t4)
    timer.end("Finished Phi estimation ({:.3f}s)")

    # interpolar los datos que faltan

    t1, phi_est = interpolate_missing_values(t1, phi_est)

    timer.start()
    phi_med_600 = median_window(phi_est, 600)
    phi_med_600 = np.array(phi_med_600)
    timer.end("Finished Phi median 600 ({:.3f}s)")
    # Corto para que sea justo múltiplo de 60 y despueés sea más fácil y entren ventanas completas

    phi_med_600 = phi_med_600[:len(phi_med_600)//60*60]
    t1 = t1[:len(phi_med_600)]
    t1.tofile(T1_OUT_FILE)

    timer.start()
    f, k = linear_reg(t1, phi_med_600, 60)
    phi_lin = np.zeros(len(t1))

    for i in range(len(t1) // 60):
        phi_lin[i * 60:(i + 1) * 60] = t1[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi lin reg 60 ({:.3f}s)")

    timer.start()
    alpha = 0.15
    f, k = arma_filter(f, k, alpha)
    phi_arma = np.zeros(len(t1))
    for i in range(len(t1) // 60):
        phi_arma[i * 60:(i + 1) * 60] = t1[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi ARMA ({:.3f}s)")

    phi_arma.tofile(O_FILE)
