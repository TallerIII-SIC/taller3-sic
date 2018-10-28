#!/usr/bin/env python3

from read_times import read_times
import sys
import numpy as np

np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'all': lambda x: str(x)})

t1_pps = np.fromfile(sys.argv[1])
t2_pps = np.fromfile(sys.argv[2])
t = np.fromfile(sys.argv[3])

t = t.reshape(-1, 4)

print(t1_pps)
print(t2_pps)
print(t)


print(len(t1_pps))
print(len(t2_pps))
print(len(t))

print(t1_pps[0], t1_pps[-1])
print(t2_pps[0], t2_pps[-1])
print(t[0], t[-1])

t1_pps_aligned = np.zeros(len(t))
t2_pps_aligned = np.zeros(len(t))

j = 0
k = 0

for i in range(len(t)):
    if t[i, 0] - t1_pps[j] > 0.5:
        j += 1
    if t[i, 1] - t2_pps[k] > 0.5:
        k += 1
    t1_pps_aligned[i] = t1_pps[j]
    t2_pps_aligned[i] = t2_pps[k]

# print(t1_pps_aligned)
# print(t2_pps_aligned)
# print(t)


# print(len(t1_pps_aligned))
# print(len(t2_pps_aligned))
# print(len(t))

# print(t1_pps_aligned[0], t1_pps_aligned[-1])
# print(t2_pps_aligned[0], t2_pps_aligned[-1])
# print(t[0], t[-1])

# print("max diff:")

# print(np.max(t[:, 0] - t1_pps_aligned))
# print(np.max(t[:, 1] - t2_pps_aligned))

# print("THIS;")


# print("max diff:")
# print(np.min(t[:, 0] - t1_pps_aligned))
# print(np.min(t[:, 1] - t2_pps_aligned))
# p = np.argmin(t[:, 1] - t2_pps_aligned)

# print("THIS;")

# print(t[p-1:p+2])
# print(t1_pps_aligned[p-1:p+2])
# print(t2_pps_aligned[p-1:p+2])

t1_pps_aligned.tofile(sys.argv[4])
t2_pps_aligned.tofile(sys.argv[5])
