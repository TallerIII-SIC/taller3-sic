#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

phi_sic = np.loadtxt("phi_sic")
plt.plot(range(len(phi_arma)), phi_sic)
plt.show()