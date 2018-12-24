#!/usr/bin/env python3
import sys
import numpy as np

t = np.loadtxt(sys.argv[1], delimiter='|')

t.tofile(sys.argv[2])
