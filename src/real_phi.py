#!/usr/bin/env python3

def read_pps(t1_file, t2_file):
    t1_pps = np.loadtxt(t1_file)
    t2_pps = np.loadtxt(t2_file)
    t1_pps_f = np.zeros(len(t1_pps))
    t2_pps_f = np.zeros(len(t1_pps))

    i = 0
    j = 0
    k = 0
    while i < len(t1_pps) and j < len(t2_pps):
        if t1_pps[i] - t2_pps[j] > 0.9e6:
            j += 1
        elif t2_pps[j] - t1_pps[i] > 0.9e6:
            i += 1
        else:
            # t1_pps_f = np.append(t1_pps_f, t1_pps[i])
            # t2_pps_f = np.append(t2_pps_f, t2_pps[j])

            t1_pps_f[k] = t1_pps[i]
            t2_pps_f[k] = t2_pps[j]

            i += 1
            j += 1
            k += 1

            if k %1000 == 0:
                print(i,j)
        
    t1_pps_f = t1_pps_f[:k]
    t2_pps_f = t2_pps_f[:k]
    
    plt.figure(10)
    plt.plot(range(len(t1_pps_f)),t1_pps_f-t2_pps_f)
    plt.show()



def fix_pps(pps, min_sec, max_sec):
    seconds_ok = np.arange(min_sec, max_sec + 1)

    i = 0

    for j in range(len(seconds_ok)):
        if pps[i] // 1e6 != seconds_ok[j]:
            seconds_ok[j] = 0
        else:
            seconds_ok[j] = pps[i]
            i += 1

    return seconds_ok


def read_data(t_file, t1_file, t2_file):
    t1, t2, t3, t4 = read_times(t_file)

    

    pps1 = np.loadtxt(t1_file)
    pps2 = np.loadtxt(t2_file)

    min_sec = min(pps1[0], pps2[0]) // 1e6
    max_sec = max(pps1[-1], pps2[-1]) // 1e6

    print("Min sec: ", min_sec)
    print("Max sec: ", max_sec)

    t1_pps = fix_pps(pps1, min_sec, max_sec)
    t2_pps = fix_pps(pps2, min_sec, max_sec)

    print("PPS:")
    np.set_printoptions(suppress=True,formatter={'float_kind':'{:f}'.format})
    print(t1_pps[75500:75650]/1e6)
    print(t2_pps[75500:75650]/1e6)
    np.set_printoptions(suppress=False)

    print("US:")
    print(t1_pps%1e6)
    print(t2_pps%1e6)

    valid = np.logical_and(t1_pps != 0, t2_pps != 0)

    print("DIFFERENT FROM ZERO:")

    print(t1_pps != 0)
    print(t2_pps != 0)

    print(valid)

    t1_pps_final = t1_pps[valid]
    t2_pps_final = t2_pps[valid]

    # t1_pps_final = np.zeros(min(len(t1_pps), len(t2_pps)))
    # t2_pps_final = np.zeros(min(len(t1_pps), len(t2_pps)))

    # k = 0

    # min_t1 = np.min(t1_pps).astype(int)
    # min_t2 = np.min(t1_pps).astype(int)

    # for i in range(min(len(t1_pps), len(t2_pps))):
    #     # Si alguno de los 2 es 0, quiere decir que se salteó ese segundo,
    #     # entonces ese segundo no lo pongo?
    #     if t1_pps[i] != 0 and t2_pps[i] != 0:
    #         t1_pps_final[k] = t1_pps[i]
    #         t2_pps_final[k] = t2_pps[i]
    #         k += 1
    # t1_pps_final = t1_pps_final[:k]
    # t2_pps_final = t2_pps_final[:k]

    # for i in range(len(t1_pps_final)):
    #     if (t1_pps_final[i]//1e6 != t2_pps_final[i]//1e6):
    #         print("Different:")
    #         print(t1_pps_final[i])
    #         print(t2_pps_final[i])
    #         input()

    return t1, t2, t3, t4, t1_pps_final, t2_pps_final