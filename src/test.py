import numpy as np

def read_pps(pps_file):
    pps = np.loadtxt(pps_file)

    seconds = (pps // 1e6).astype(int)

    first_second = seconds[0]
    last_second = seconds[-1]

    seconds_ok = np.arange(first_second, last_second + 1)

    i = 0

    for j in range(len(seconds_ok)):
        if seconds[i] != seconds_ok[j]:
            # print("Missing second:", seconds_ok[j])
            seconds_ok[j] = 0
        else:
            i += 1

    return seconds_ok


def read_data(t1_file, t2_file):
    t1_pps = read_pps(t1_file)
    t2_pps = read_pps(t2_file)

    max_t1_t2 = max(t1_pps[-1], t2_pps[-1])

    t1_pps_final = np.zeros(min(len(t1_pps), len(t2_pps)))
    t2_pps_final = np.zeros(min(len(t1_pps), len(t2_pps)))

    k = 0

    for i in range(min(len(t1_pps), len(t2_pps))):
        # Si alguno de los 2 es 0, quiere decir que se salteó ese segundo,
        # entonces ese segundo no lo pongo?
        if t1_pps[i] != 0 or t2_pps[i] != 0:
            t1_pps_final[k] = t1_pps[i]
            t2_pps_final[k] = t2_pps[i]
            k += 1
    t1_pps_final = t1_pps_final[:k]
    t2_pps_final = t2_pps_final[:k]

    return t1_pps_final, t2_pps_final


t1_file = '../data/escenario_interior/ventana_600/t1_pps.txt'
t2_file = '../data/escenario_interior/ventana_600/t2_pps.txt'

# read_data(t1_file, t2_file)

pps = np.loadtxt(t1_file)

i = np.argmax(pps[1:] - pps[:-1])

print("1: ",pps[i], " 2: ", pps[i+1])

print("Max difference between PPS: ", np.max(pps[1:] - pps[:-1]))

pps = np.loadtxt(t2_file)
print("Max difference between PPS: ", np.max(pps[1:] - pps[:-1]))
i = np.argmax(pps[1:] - pps[:-1])

print("1: ",pps[i-1], " 2: ", pps[i])