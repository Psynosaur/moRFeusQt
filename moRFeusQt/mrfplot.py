import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as mplt


class MorfeusPlot(object):

    @classmethod
    def drawgraph(cls, x, y, l):
        mplt.ion()
        mplt.plot(x, y, '-', label=l)
        mplt.title("Transmission Loss")
        mplt.xlabel('Frequency MHz')
        mplt.ylabel('TL (dB)')
        mplt.legend()
        mplt.tight_layout()
        mplt.pause(0.01)

    @classmethod
    def close(cls):
        mplt.close('all')

    # @classmethod
    # def qtgraph(cls, x, y):
    #     plt = pg.plot(x, y, title='Tx loss', pen='r')




