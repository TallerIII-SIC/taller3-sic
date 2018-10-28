#!/usr/bin/env python3

import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import time
import read_times


def phi_estimation(t1, t2, t3, t4):
    return (t1 - t2 - t3 + t4) / 2


def median_window(phi, w_length):
    new_phi = np.zeros(len(phi))
    for w_start in range(len(phi) - w_length):
        new_phi[w_start] = np.median(phi[w_start:w_start + w_length])
    return new_phi

# OTRA VERSION DE LO DE ARRIBA, HAY QUE VER SI FUNCIONA BIEN Y SI REALMENTE ES MÁS RÁPIDA
# def median_window2(phi, w_length):
#     new_phi = np.zeros(len(phi))
#     window = phi[:w_length]
#     sorted_window = np.sort(window)
#     for i in range(len(phi) - w_length):
#         if i != 0:
#             k = 0
#             new_window = np.zeros(w_length)
#             for j in range(1, w_length):
#                 if phi[i] > sorted_window[j]:
#                     new_window[k] = sorted_window[j]
#                     k += 1
#                 else:
#                     new_window[k] = phi[i]
#                     new_window[k + 1:] = sorted_window[j:]
#                     break
#             sorted_window = new_window
#         # w_legth is even
#         median = 0.5 * (sorted_window[w_length //
#                                       2 - 1] + sorted_window[w_length // 2])
#         new_phi[i] = median
#     return new_phi


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
    t1, t2, t3, t4 = read_times(T_FILE)
    timer.end("Finished reading data ({:.3f}s)")

    timer.start()
    phi_est = phi_estimation(t1, t2, t3, t4)
    timer.end("Finished Phi estimation ({:.3f}s)")

    t = range(len(phi_est))

    timer.start()
    phi_med_600 = median_window(phi_est, 600)
    timer.end("Finished Phi median 600 ({:.3f}s)")

    timer.start()
    f, k = linear_reg(t, phi_med_600, 60)
    phi_lin = np.zeros(len(t))
    for i in range(len(t) // 60):
        phi_lin[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi lin reg 60 ({:.3f}s)")

    timer.start()
    alpha = 0.05
    f, k = arma_filter(f, k, alpha)
    phi_arma = np.zeros(len(t))
    for i in range(len(t) // 60):
        phi_arma[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi ARMA ({:.3f}s)")

    np.savetxt(O_FILE, phi_arma)
