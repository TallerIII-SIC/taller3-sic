#!/usr/bin/env python3

import sys
import numpy as np

if len(sys.argv) != 3:
    print("Usage: fix_pps <pps> <output>")
    sys.exit()

t_pps = np.loadtxt(sys.argv[1])
t_pps_final = np.zeros(int(np.round(t_pps[-1] - t_pps[0] + 2)))


j = 0
prev = float('inf')
for i, t in enumerate(t_pps):
    if t - prev > 1.1:
        # Se salteó segundos
        num_missing_seconds = int(np.round(t - prev - 1))
        t_pps_final[j:j + num_missing_seconds +
                    1] = np.linspace(prev, t, num_missing_seconds + 2)[1:]
        j += num_missing_seconds + 1
    else:
        t_pps_final[j] = t
        j += 1
    prev = t

t_pps_final = t_pps_final[:j]

print(len(np.setdiff1d(t_pps_final,t_pps)))
print(np.setdiff1d(t_pps,t_pps_final))
print(np.max(np.diff(t_pps)))
print(np.max(np.diff(t_pps_final)))
print(np.min(np.diff(t_pps)))
print(np.min(np.diff(t_pps_final)))
print(t_pps[-1], t_pps[0])
print(t_pps_final[-1], t_pps_final[0])

np.savetxt(sys.argv[2],t_pps_final)
