import allantools
import matplotlib.pyplot as plt
import numpy as np


# Receives the TE in seconds and plots the Allan TDEV
def plotTDEV(TE):
    frequency = np.diff(TE)
    a = allantools.Dataset(data=frequency, data_type='freq')
    a.compute("tdev")

    plotter = allantools.Plot()
    plotter.plot(a, errorbars=True, grid=True)

    plotter.ax.set_xlabel("$\\tau$ [s]")
    plotter.ax.set_ylabel("TDEV [s]")
    plt.title("Varianza de Allan para SIC")
    plotter.show()