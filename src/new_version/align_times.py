#!/usr/bin/env python3

from read_times import read_times
import sys
import numpy as np

t1_pps = np.fromfile(sys.argv[1],dtype=int)
t2_pps = np.fromfile(sys.argv[2],dtype=int)

print("t1 len: ", len(t1_pps))

t = np.fromfile(sys.argv[3],dtype=int)
print(t.shape)
t = t.reshape(-1,4)
print(t.shape)

print("T1 PPS:",t1_pps)
print("T2 PPS:",t2_pps)
print("T:",t)

print("Finished reading files")

length = min([len(t1_pps),len(t2_pps),len(t)])

t1_pps_ok = np.zeros(length)
t2_pps_ok = np.zeros(length)

t_ok = np.zeros((length,4))
t_ok_ok = np.zeros((length,4))
t1_pps_ok_ok = np.zeros(length)

print("HERE")

m = 0
i = 0
j = 0
print("Max diff in t1: ",np.max(np.abs(t[1:,0]-t[:-1,0]))/1e6)
print("Max diff in t1 PPS: ",np.max(np.abs(t1_pps[1:]-t1_pps[:-1]))/1e6)


while i < len(t) and j < len(t1_pps):

    diff = t[i][0] - t1_pps[j]

    if diff > 0.2e6:
        j += 1
    elif diff < -0.2e6:
        i += 1
    else:
        t1_pps_ok[m] = t1_pps[j]
        t_ok[m,:] = t[i,:]
        m += 1
        i += 1
        j += 1

print("ORIGINAL: ", len(t1_pps))
print("ORIGINAL: ", len(t))
print("TOTAL: ",m)

print("Max diff: ",np.max(np.abs(t_ok[:,0]-t1_pps_ok))/1e6)
print("Max diff in new t1: ",np.max(np.abs(t_ok[1:,0]-t_ok[:-1,0]))/1e6)
print("Max diff in new t1 pps: ",np.max(np.abs(t1_pps_ok[1:]-t1_pps_ok[:-1]))/1e6)


m = 0
i = 0
j = 0
print("Max diff in t2: ",np.max(np.abs(t_ok[1:,1]-t_ok[:-1,1]))/1e6)
print("Max diff in t2 PPS: ",np.max(np.abs(t2_pps[1:]-t2_pps[:-1]))/1e6)


while i < len(t_ok) and j < len(t2_pps):

    diff = t_ok[i][1] - t2_pps[j]

    if diff > 0.2e6:
        j += 1
    elif diff < -0.2e6:
        i += 1
    else:
        t2_pps_ok[m] = t2_pps[j]
        t_ok_ok[m,:] = t_ok[i,:]
        t1_pps_ok_ok[m] = t1_pps_ok[i]
        m += 1
        i += 1
        j += 1

t_ok_ok = t_ok_ok[:m,:]
t1_pps_ok_ok = t1_pps_ok_ok[:m]
t2_pps_ok = t2_pps_ok[:m]

print("ORIGINAL: ", len(t2_pps))
print("ORIGINAL: ", len(t_ok))
print("TOTAL: ",m)

print("Max diff: ",np.max(np.abs(t_ok_ok[:,1]-t2_pps_ok))/1e6)
print("Max diff in new t2: ",np.max(np.abs(t_ok_ok[1:,1]-t_ok_ok[:-1,1]))/1e6)
print("Max diff in new t2 pps: ",np.max(np.abs(t2_pps_ok[1:]-t2_pps_ok[:-1]))/1e6)

import matplotlib.pyplot as plt

phi_est = t_ok_ok[:,0] - t_ok_ok[:,1] - t_ok_ok[:,2] + t_ok_ok[:,3]

phi_est = - phi_est / 2

phi = t2_pps_ok - t1_pps_ok_ok

t_ok = t_ok_ok[:,:]
t1_pps_ok = t1_pps_ok_ok[:]


m = 0

length = int((t1_pps_ok[-1] - t1_pps_ok[0])/1e6 + 1)

print("LENGTH: ",length)

t1_pps_final = np.zeros(length)
t2_pps_final = np.zeros(length)
phi_est_final = np.zeros(length)
t_final = np.zeros((length,4))

t1_pps_final[0] = t1_pps_ok[0]

k = 0
np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:0.2f}'.format})
for i in range(0,len(t_ok) - 1):
    if t1_pps_ok[i+1] - t1_pps_ok[i] > 1.5e6:
        # Se salteó un segundo o más: interpolación lineal

        diff_microsegundos = t1_pps_ok[i+1] - t1_pps_ok[i]
        diff_segundos = int(np.round(diff_microsegundos/1e6)) 

        n = diff_segundos + 1

        aux1 = np.linspace(t1_pps_ok[i],t1_pps_ok[i+1],n)
        aux2 = np.linspace(t2_pps_ok[i],t2_pps_ok[i+1],n)
        aux3 = np.linspace(phi_est[i],phi_est[i+1],n)
    
        t1_pps_final[m:m+n-1] = aux1[:-1]
        t2_pps_final[m:m+n-1] = aux2[:-1]
        phi_est_final[m:m+n-1] = aux3[:-1]
#        print("AHORA QUEDA: ", t1_pps_final[m-5:m+n]/1e6)
        m += n - 1
    else:
        # No se salteó ningún segundo, lo pongo tal cual

        t1_pps_final[m] = t1_pps_ok[i]
        t2_pps_final[m] = t2_pps_ok[i]
        phi_est_final[m] = phi_est[i]
        m += 1


plt.plot(t1_pps_ok_ok//1e6,phi_est,'b')
plt.plot(t1_pps_ok_ok//1e6,phi,'r')
plt.plot(t1_pps_ok_ok[1:]//1e6,t_ok_ok[1:,0]-t_ok_ok[:-1,0],'y')
plt.legend(('estimated','real','big difference'))
plt.show()

plt.plot(t1_pps_final//1e6,phi_est_final,'b')
plt.show()
