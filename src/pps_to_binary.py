#!/usr/bin/env python3
import sys
import numpy as np

t_pps = np.loadtxt(sys.argv[1])

t_pps.tofile(sys.argv[2])
