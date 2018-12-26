# Main Loop
import sys
import signal
from PyQt5.QtWidgets import QApplication
from moRFeusQt import mrfqt as mRFsApp
from moRFeusQt import mrf
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    app = QApplication(sys.argv)
    devicecount = mrf.MoRFeus.find()
    devices = []
    for i in range(0, devicecount):
        devices.append(mRFsApp.MoRFeusQt(i))
        print('--------------------\nmoRFeus Dev', i, 'Stats\n--------------------')
        devices[i].getStats()
        print('--------------------\nDevice Output\n--------------------')
        devices[i].show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
