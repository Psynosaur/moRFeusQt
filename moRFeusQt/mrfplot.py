import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as mplt
# import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
# ggplot, classic, seaborn-notebook, seaborn-whitegrid


class MorfeusPlot(object):

    @classmethod
    def drawgraph(cls, x, y, l):
        mplt.ion()
        mplt.plot(x, y, '-', label=l)
        mplt.title("Transmission Loss")
        mplt.xlabel('Frequency MHz')
        mplt.ylabel('level [dB]')
        mplt.legend()
        mplt.tight_layout()
        mplt.pause(0.01)
        mplt.draw()

    @classmethod
    def close(cls):
        mplt.close('all')

    # @classmethod
    # def liveplot(cls, x, y):
    #     fig = mplt.figure()
    #     ax1 = fig.add_subplot(1, 1, 1)
    #     # graph_data = open('example.txt', 'r').read()
    #     # lines = graph_data.split('\n')
    #     xs = []
    #     ys = []
    #     xs.append(float(x))
    #     ys.append(float(y))
    #     ax1.clear()
    #     ax1.plot(xs, ys)
    #     ani = animation.FuncAnimation(fig, animate, interval=1000)
    #     mplt.show()

    # @classmethod
    # def qtgraph(cls, x, y):
    #     plt = pg.plot(x, y, title='Tx loss', pen='r')




