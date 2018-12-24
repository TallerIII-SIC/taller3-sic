#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

t_real_phi = np.fromfile(sys.argv[1])
real_phi = np.fromfile(sys.argv[2])
t_sic_phi = np.fromfile(sys.argv[3])

real_phi = np.interp(t_sic_phi,t_real_phi,real_phi)

real_phi.tofile(sys.argv[4])
