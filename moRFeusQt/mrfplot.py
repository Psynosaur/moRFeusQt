import numpy as np
import matplotlib.pyplot as plt


class MorfeusPlot(object):

    @classmethod
    def drawgrap(cls, x, y):
        plt.autoscale()
        plt.plot(x, y)  # plotting by columns
        plt.autoscale()
        plt.show()


