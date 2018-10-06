#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

phi_arma = np.loadtxt("phi_arma")
plt.plot(range(len(phi_arma)), phi_arma)
plt.show()