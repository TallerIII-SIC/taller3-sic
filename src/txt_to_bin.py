#!/usr/bin/env python3
import sys
import numpy as np


def txt_to_bin(t1_pps_fname = 't1_pps', t2_pps_fname = 't2_pps', times_fname = 'tiempos'):
    """Receives the txt file names (without extension) and generates the bin files."""
    t1_pps = np.loadtxt(t1_pps_fname + '.txt', dtype=int)
    t2_pps = np.loadtxt(t2_pps_fname + '.txt', dtype=int)
    t = np.loadtxt(times_fname + '.txt', delimiter='|', dtype=int)

    t1_pps.tofile(t1_pps_fname + '.bin')
    t2_pps.tofile(t2_pps_fname + '.bin')
    t.tofile(times_fname + '.bin')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 txt_to_bin.py t1_pps_fname t2_pps_fname times_fname')
        exit(1)

    _, pps1, pps2, times = sys.argv
    txt_to_bin(pps1, pps2, times)
