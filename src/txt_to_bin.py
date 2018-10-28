#!/usr/bin/env python3
import sys
from read_times import read_times

import numpy as np

t1_pps = np.loadtxt(sys.argv[1],dtype=int)
t2_pps = np.loadtxt(sys.argv[2],dtype=int)

t = np.loadtxt(sys.argv[3],delimiter='|',dtype=int)

t1_pps.tofile('t1_pps.bin')
t2_pps.tofile('t2_pps.bin')
t.tofile('tiempos.bin')
