#!/usr/bin/env python3

import numpy as np
import sys
t = np.fromfile(sys.argv[1])
t = t.reshape(-1,4)
t1 = t[:,0]
t1.tofile(sys.argv[2])

