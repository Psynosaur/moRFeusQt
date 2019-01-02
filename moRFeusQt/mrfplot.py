import matplotlib
import matplotlib.pyplot as mplt
matplotlib.use('Qt5Agg')


class MorfeusPlot(object):

    @classmethod
    def drawgraph(cls, x, y, l):
        mplt.ion()
        mplt.plot(x, y, '-', label=l)  # plotting by columns
        mplt.title("Transmission Loss")
        mplt.xlabel('Frequency MHz')
        mplt.ylabel('TL (dB)')
        mplt.legend()
        mplt.pause(0.01)

    # @classmethod
    # def qtgraph(cls, x, y):
    #     plt = pg.plot(x, y, title='Tx loss', pen='r')




