import frontend
import sys
from PyQt5 import QtWidgets

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QtWidgets.QApplication([])
    mi_app = frontend.MainWindow()
    mi_app.show()
    app.exec()
