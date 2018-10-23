#!/usr/bin/env python3

import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import time


def read_times(filename):

    lines = np.loadtxt(filename, dtype=int, delimiter='|')

    t1 = lines[:, 0]
    t2 = lines[:, 1]
    t3 = lines[:, 2]
    t4 = lines[:, 3]

    return t1, t2, t3, t4

def phi_estimation(t1, t2, t3, t4):
    return (t1 - t2 - t3 + t4) / 2


def median_window(phi, w_length):
    new_phi = np.zeros(len(phi))
    for w_start in range(len(phi) - w_length):
        new_phi[w_start] = np.median(phi[w_start:w_start + w_length])
    return new_phi


def median_window2(phi, w_length):
    new_phi = np.zeros(len(phi))
    window = phi[:w_length]
    sorted_window = np.sort(window)
    for i in range(len(phi) - w_length):
        if i != 0:
            k = 0
            new_window = np.zeros(w_length)
            for j in range(1, w_length):
                if phi[i] > sorted_window[j]:
                    new_window[k] = sorted_window[j]
                    k += 1
                else:
                    new_window[k] = phi[i]
                    new_window[k + 1:] = sorted_window[j:]
                    break
            sorted_window = new_window
        # w_legth is even
        median = 0.5 * (sorted_window[w_length //
                                      2 - 1] + sorted_window[w_length // 2])
        new_phi[i] = median
    return new_phi


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


def mtie_calc(phi_real, phi_arma, tau):
    print("Length: ", len(phi_real), " and ", len(phi_arma))
    te = phi_arma - phi_real
    tie = te[tau:] - te[:-tau]
    mtie = np.zeros(len(phi_arma))
    for t_0 in range(len(phi_arma)):
        mtie[t_0] = max(te[t_0:t_0 + tau]) - min(te[t_0:t_0 + tau])
    return mtie


class Timer(object):
    def __init__(self):
        self.st = 0

    def start(self):
        self.st = time.time()

    def end(self, msg):
        end = time.time()
        print(msg.format(end - self.st))


if __name__ == '__main__':

    T1_PPS_FILE = sys.argv[1]
    T2_PPS_FILE = sys.argv[2]
    T_FILE = sys.argv[3]

    read_pps(T1_PPS_FILE, T2_PPS_FILE)

    sys.exit()


    timer = Timer()

    timer.start()
    t1, t2, t3, t4, t1_pps, t2_pps = read_data(
        T_FILE, T1_PPS_FILE, T2_PPS_FILE)
    timer.end("Finished reading data ({:.3f}s)")

    timer.start()
    phi_est = phi_estimation(t1, t2, t3, t4)
    timer.end("Finished Phi estimation ({:.3f}s)")

    t = range(len(phi_est))

    plot_range = slice(0, 50000)

    plt.plot(t[plot_range], phi_est[plot_range])

    # timer.start()
    # phi_med_120 = median_window(phi_est, 120)
    # timer.end("Finished Phi median 120 ({:.3f}s)")

    # plt.plot(t[plot_range], phi_med_120[plot_range])

    timer.start()
    phi_med_600 = median_window(phi_est, 600)
    timer.end("Finished Phi median 600 ({:.3f}s)")

    timer.start()
    phi_med_600_2 = median_window2(phi_est, 600)
    timer.end("Finished Phi median 600 (2) ({:.3f}s)")

    print("Are the same? ", np.sum(phi_med_600 == phi_med_600_2))

    pp = plt.figure(7)

    plt.plot(t[plot_range], phi_med_600[plot_range])
    plt.plot(t[plot_range], phi_med_600_2[plot_range])

    plt.legend(('ORIGINAL', 'NEW'))

    plt.show()

    timer.start()
    f, k = linear_reg(t, phi_med_600, 60)
    phi_lin = np.zeros(len(t))
    for i in range(len(t) // 60):
        phi_lin[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi lin reg 60 ({:.3f}s)")

    plt.plot(t[plot_range], phi_lin[plot_range])

    timer.start()
    alpha = 0.05
    f, k = arma_filter(f, k, alpha)
    phi_arma = np.zeros(len(t))
    for i in range(len(t) // 60):
        phi_arma[i * 60:(i + 1) * 60] = t[i * 60:(i + 1) * 60] * f[i] + k[i]
    timer.end("Finished Phi ARMA ({:.3f}s)")

    plt.plot(t[plot_range], phi_arma[plot_range])

    phi_real = t1_pps - t2_pps
    plt.plot(t[plot_range], phi_real[plot_range])

    plt.legend(
        (r'$\Phi est$',
         r'$\Phi med 600$',
         r'$\Phi lin 60$', r'$\Phi ARMA$', r'$\Phi real$'))

    plt.show()

    f = plt.figure(1)

    plt.plot(range(len(phi_arma)), phi_arma)
    plt.plot(range(len(phi_real)), phi_real)

    print("ARMA: ", len(phi_arma))
    print("REAL: ", len(phi_real))

    plt.legend((r'$\Phi ARMA$', r'$\Phi real$'))

    f.show()

    print("LAST PLOT IS ARMA VS REAL")

    input()

    h = plt.figure(3)
    plt.plot(range(len(phi_arma)), phi_arma)
    plt.title("ARMA")
    h.show()

    input()

    g = plt.figure(2)

    mtie = mtie_calc(phi_real, phi_arma, tau=60)
    plt.hist(mtie, bins=10, cumulative=True, normed=True)
    g.show()

    # plt.legend(
    #     (r'$\Phi est$',
    #      r'$\Phi med 120$',
    #      r'$\Phi med 600$',
    #      r'$\Phi lin 60$', r'$\Phi ARMA$', r'$\Phi real$'))
