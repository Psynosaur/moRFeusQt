
import sys

from PyQt5.QtWidgets import QApplication
from moRFeusQt import mRFsQt as mRFsApp

def main():
    app = QApplication(sys.argv)
    morfGUI = mRFsApp.moRFeusQt()
    print('--------------------\nmoRFeus Device Stats\n--------------------')
    morfGUI.getStats()
    print('--------------------\nDevice Output\n--------------------')
    morfGUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
