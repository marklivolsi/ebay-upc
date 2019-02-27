import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UI.main_window import Ui_Form


class App(QWidget, Ui_Form):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.search_btn.clicked.connect(self.print_hello)

    def print_hello(self):
        print("HELLO!!")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())



# import sys
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import pyqtSlot
#
#
# class App(QtWidgets.QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.ui = uic.loadUi('UI/main_window.ui')
#         self.ui.show()
#
#     @pyqtSlot()
#     def test_btn(self):
#         self.connect(self.ui.maxprice_val)
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = App()
#     sys.exit(app.exec_())

