#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt


def mtie_calc(te, tau):
    # plt.subplot(4, 1, 1)
    # plt.plot(te)
    # plt.title('TE')
    # plt.xlabel("t [s]")
    # plt.ylabel("TE [s]")
    # plt.subplot(4, 1, 2)
    tie = te[tau:] - te[:-tau]
    # print(np.mean(tie))
    # print(np.max(tie))
    # print(np.min(tie))
    # print(tie)
    # plt.plot(tie)
    # plt.title('TIE')
    # plt.xlabel("t [s]")
    # plt.ylabel("TIE [s]")
    # plt.subplot(4, 1, 3)
    mtie = np.zeros(len(te)-tau)
    for t_0 in range(len(te)-tau):
        maximum = max(te[t_0:t_0+tau])
        minimum = min(te[t_0:t_0+tau])
        mtie[t_0] = maximum - minimum
    mtie = mtie  # Paso a microsegundos
    # plt.plot(mtie)
    # plt.title("MTIE")
    # plt.xlabel("t [s]")
    # plt.ylabel("MTIE [us]")
    # plt.subplot(4, 1, 4)
    # plt.hist(mtie, bins=5000, density=True, cumulative=True, histtype='step')
    # print("PERCENTIL 90: ", np.percentile(mtie, 90))
    # plt.title("MTIE histogram")
    # plt.xlabel('MTIE [us]')
    # plt.ylabel('Frec')
    # plt.xlim([0, 100])
    # plt.yticks([0.1*i for i in range(11)])
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

    # print("MIN TE: ", np.min(te))
    # print("MAX TE: ", np.max(te))
    # print("AVG TE: ", np.mean(te))

    t_pps = t_pps / 1e6

    t_pps_final = np.zeros(int(np.round(t_pps[-1] - t_pps[0] + 2)))
    te_final = np.zeros(int(np.round(t_pps[-1] - t_pps[0] + 2)))

    # print(len(t_pps))
    # print(len(te))
    # print(len(t_pps))

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
        else:
            t_pps_final[j] = t
            te_final[j] = te[i]
            j += 1
        prev = t

    t_pps_final = t_pps_final[:j]
    te_final = te_final[:j]
    MTIE_WINDOW = 60
    tie, mtie = mtie_calc(te_final, MTIE_WINDOW)
    plt.show()
