import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from UI.main_window import Ui_Form
from models import Product


upc = '883929638482'
prod = Product()
prod.upc = upc
prod.retrieve_completed_listings()
prod.item_details_main_async_loop()
prod.update_completed_listing_details()


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.price_dist_img.setScaledContents(True)

        self.newproduct_btn.clicked.connect(self.set_price_histogram)

    def set_price_histogram(self):
        prod.price_histogram()
        filepath = '{}.png'.format(self.upc_field.text())
        pixmap = QtGui.QPixmap(filepath)
        self.price_dist_img.setPixmap(pixmap.scaled(self.price_dist_img.size(), QtCore.Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())





# from models import Product
#
#
# TEST_UPC = '883929638482'
#
#
# def main():
#     # upc = Product(TEST_UPC)
#     # upc.retrieve_completed_listings()
#     # upc.item_details_main_async_loop()
#     # upc.update_completed_listing_details()
#     # print('mean: ', upc.mean_price_completed_listings)
#     # print('median: ', upc.median_price_completed_listings)
#     # print('min: ', upc.min_price_completed_listings)
#     # print('max: ', upc.max_price_completed_listings)
#     # for item in upc.completed_listings:
#     #     print(item.item_id, item.price, item.img_url_arr, item.description)
#
#     import sys
#     from PyQt5 import QtWidgets, uic
#
#     app = QtWidgets.QApplication(sys.argv)
#     window = uic.loadUi('UI/main_window.ui')
#     window.show()
#
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
