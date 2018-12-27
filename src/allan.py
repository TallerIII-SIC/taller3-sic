import allantools


def plotTDEV(TE):
    a = allantools.Dataset(data=TE)
    a.compute("tdev")

    plotter = allantools.Plot()
    plotter.plot(a, errorbars=True, grid=True)

    plotter.ax.set_xlabel("Tau [s]")
    plotter.ax.set_ylabel("TDEV [us]")
    plt.title("Varianza de Allan para SIC")
    plotter.show()