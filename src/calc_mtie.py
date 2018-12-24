#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt


def mtie_calc(te, tau):
    tie = te[tau:] - te[:-tau]
    mtie = np.zeros(len(te)-tau)
    for t_0 in range(len(te)-tau):
        maximum = max(te[t_0:t_0+tau])
        minimum = min(te[t_0:t_0+tau])
        mtie[t_0] = maximum - minimum
    return tie, mtie

def mtie_calc_2(te,tau):
    # otro metodo con las ventanas fijas
    tie = te[tau:] - te[:-tau]
    mtie = np.zeros(len(te)//tau)
    for i in range(len(mtie)):
        t_0 = i*tau
        maximum = max(te[t_0:t_0+tau])
        minimum = min(te[t_0:t_0+tau])
        mtie[i] = maximum - minimum
    return tie, mtie

if __name__ == '__main__':

    real_phi = np.fromfile(sys.argv[1])
    sic_phi = np.fromfile(sys.argv[2])
    sic_phi = np.round(sic_phi)
    t_pps = np.fromfile(sys.argv[3])
    print(real_phi.shape)
    print(sic_phi.shape)
    print(t_pps.shape)

    plt.plot(sic_phi)
    plt.plot(real_phi)
    plt.legend(('sic', 'real'))
    plt.show()

    te = sic_phi - real_phi

    t_pps = t_pps / 1e6

    
    # >>>>> ESTO DE ACÁ ABAJO SE PODRÍA SACAR, NO CAMBIA NADA, PORQUE YA HABIA INTERPOLADO ANTES

    t_pps_final = np.zeros(int(np.round(t_pps[-1] - t_pps[0] + 2)))
    te_final = np.zeros(int(np.round(t_pps[-1] - t_pps[0] + 2)))

    j = 0
    prev = float('inf')
    for i, t in enumerate(t_pps):
        if t - prev > 1.1:
            # Se salteó segundos
            num_missing_seconds = int(np.round(t - prev - 1))
            t_pps_final[j:j + num_missing_seconds +
                        1] = np.linspace(prev, t, num_missing_seconds + 2)[1:]
    #        te_final[j:j+num_missing_seconds+1] = prev
            te_final[j:j+num_missing_seconds +
                     1] = np.linspace(te[i-1], te[i], num_missing_seconds + 2)[1:]
            j += num_missing_seconds + 1
            print("SKIPPED SECONDS")
        else:
            t_pps_final[j] = t
            te_final[j] = te[i]
            j += 1
        prev = t

    t_pps_final = t_pps_final[:j]
    te_final = te_final[:j]

    # <<<<< HASTA ACÁ

    MTIE_WINDOW = 60
    tie, mtie = mtie_calc(te_final, MTIE_WINDOW)
    plt.show()
