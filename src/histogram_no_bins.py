import numpy as np

def histogram_no_bins(x):
    values, frequencies = np.unique(x, return_counts = True)
    histogram = np.cumsum(frequencies)
    histogram = histogram/histogram[-1]
    return values, histogram