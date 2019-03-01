from helpers import *
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from UI.main_window import Ui_Form
from models import Product
from itertools import chain
from numpy import mean, median


# def test_loop(prod):
#     prod.upc = '786936858990'


# upc = '883929638482'
# prod = Product()
# prod.upc = upc
# prod.retrieve_completed_listings()
# prod.item_details_main_async_loop()
# prod.update_listing_details()


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.price_dist_img.setScaledContents(True)

        self.clear_btn.clicked.connect(self.clear_contents)
        self.fetchlistings_btn.clicked.connect(self.main_loop)

    def main_loop(self):
        prod = Product()
        prod.upc = self.upc_field.text()
        prod.main_fetch_loop()
        self.set_price_histogram(prod)
        # # prod.image_array_main_async_loop()
        self.set_combo_box_options(prod)
        self.set_price_statistics(prod)

    def set_price_histogram(self, prod):
        file_path = prod.generate_price_histogram()
        pixmap = QtGui.QPixmap(file_path)
        self.price_dist_img.setPixmap(pixmap.scaled(self.price_dist_img.size(), QtCore.Qt.KeepAspectRatio))

    def set_combo_box_options(self, prod):
        # self.selectimg_combobox.addItems(prod.img_url_list)
        self.selectimg_combobox_1.addItems(prod.get_property_list('img_url_arr'))
        self.selectimg_combobox_2.addItems(prod.get_property_list('img_url_arr'))
        self.title_combobox.addItems(prod.get_property_list('title'))
        self.catname_combobox.addItems(prod.get_property_list('cat_name'))
        self.catid_combobox.addItems(prod.get_property_list('cat_id'))

    def set_price_statistics(self, prod):
        self.minprice_val.setText(prod.get_price_statistic(min))
        self.maxprice_val.setText(prod.get_price_statistic(max))
        self.meanprice_val.setText(prod.get_price_statistic(mean))
        self.medianprice_val.setText(prod.get_price_statistic(median))
        self.numlistings_val.setText(str(len(prod.completed_listings)))

    def clear_contents(self):
        self.search_field.setText('')
        self.upc_field.setText('')
        self.title_field.setText('')
        self.catname_field.setText('')
        self.catid_field.setText('')
        self.price_field.setText('')
        self.shipping_field.setText('')
        self.description_field.setPlainText('')
        self.selectimg_combobox.setCurrentText('')
        self.imgurl_field.setText('')
        self.product_img.clear()
        self.price_dist_img.clear()
        self.minprice_val.setText('N/A')
        self.maxprice_val.setText('N/A')
        self.medianprice_val.setText('N/A')
        self.numlistings_val.setText('N/A')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
