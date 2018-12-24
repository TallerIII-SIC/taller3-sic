#!/usr/bin/env python3

import sys
import numpy as np

t1_pps = np.fromfile(sys.argv[1])
t2_pps = np.fromfile(sys.argv[2])

real_phi = t1_pps - t2_pps

real_phi.tofile(sys.argv[3])