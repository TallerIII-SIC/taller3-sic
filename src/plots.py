#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

real_phi = np.fromfile(sys.argv[1])
sic_phi = np.fromfile(sys.argv[2])

print(len(real_phi))
print(len(sic_phi))

plt.plot(real_phi)
plt.plot(sic_phi)
plt.legend(('real phi','sic phi'))

plt.show()