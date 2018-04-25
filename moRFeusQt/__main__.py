
import sys

from PyQt4 import QtCore, QtGui
from moRFeusQt import moRFeus_Qt

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    mFQt = QtGui.QApplication(sys.argv)
    window = moRFeus_Qt.moRFeusQt()
    print('--------------------\nmoRFeus Device Stats\n--------------------')
    window.getStats()
    print('--------------------\nDevice Output\n--------------------')
    window.getReg()
    window.show()
    sys.exit(mFQt.exec_())

if __name__ == "__main__":
    main()
