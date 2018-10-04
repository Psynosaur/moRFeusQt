# Main Loop
import sys
import signal
from PyQt5.QtWidgets import QApplication
from moRFeusQt import mrfqt as mRFsApp
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    app = QApplication(sys.argv)
    mrfgui = mRFsApp.MoRFeusQt()
    print('--------------------\nmoRFeus Device Stats\n--------------------')
    mrfgui.getStats()
    print('--------------------\nDevice Output\n--------------------')
    mrfgui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
