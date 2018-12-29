import numpy as np
import matplotlib.pyplot as plt


class MorfeusPlot(object):

    @classmethod
    def drawgrap(cls, x, y, l):
        plt.autoscale()
        plt.plot(x, y, '-', label=l)  # plotting by columns
        plt.title("Transmission Loss")
        plt.xlabel('Frequency MHz')
        plt.ylabel('TL (dB)')
        plt.autoscale()
        plt.legend()
        plt.show()


