from helpers import *
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from UI.main_window import Ui_Form
from models import Product
from numpy import mean, median


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.price_dist_img.setScaledContents(True)
        self.product_img_1.setScaledContents(False)
        self.product_img_2.setScaledContents(False)

        self.clear_btn.clicked.connect(self.clear_contents)
        self.fetchlistings_btn.clicked.connect(self.main_loop)

        self.title_combobox.activated.connect(self.set_title_field)
        self.catname_combobox.activated.connect(self.set_catname_field)
        self.catid_combobox.activated.connect(self.set_catid_field)
        self.selectimg_combobox_1.activated.connect(self.set_img_combobox_1)
        self.selectimg_combobox_2.activated.connect(self.set_img_combobox_2)

    def main_loop(self):
        prod = Product()
        prod.upc = self.upc_field.text()
        prod.main_fetch_loop()
        self.set_price_histogram(prod)
        # # prod.image_array_main_async_loop()
        self.set_combo_box_options(prod)
        self.set_price_statistics(prod)
        self.populate_fields(prod)

    def set_title_field(self):
        self.title_field.setText(self.title_combobox.currentText())

    def set_catname_field(self):
        self.catname_field.setText(self.catname_combobox.currentText())

    def set_catid_field(self):
        self.catid_field.setText(self.catid_combobox.currentText())

    def set_img_combobox_1(self):
        url = self.selectimg_combobox_1.currentText()
        self.imgurl_field_1.setText(url)
        self.set_product_image(url, self.product_img_1)

    def set_img_combobox_2(self):
        url = self.selectimg_combobox_2.currentText()
        self.imgurl_field_2.setText(url)
        self.set_product_image(url, self.product_img_2)

    def set_product_image(self, url, img_field):
        pixmap = QtGui.QPixmap.fromImage(show_img_from_url(url))
        img_field.setPixmap(pixmap.scaled(img_field.size(), QtCore.Qt.KeepAspectRatio))
    # def set_product_image_1(self):
    #     pixmap = QtGui.QPixmap(show_img_from_url(url))

    def populate_fields(self, prod):
        self.set_title_field()
        self.set_catname_field()
        self.set_catid_field()
        self.price_field.setText(prod.get_price_statistic(median))
        self.shipping_field.setText('0.00')
        self.description_field.setPlainText(strip_html_tags(prod.get_property_list('description')[0]))
        self.set_img_combobox_1()
        self.selectimg_combobox_2.setCurrentIndex(1)
        self.set_img_combobox_2()
        # self.set_product_image(self.selectimg_combobox_1, self.product_img_1)
        # self.set_product_image(self.selectimg_combobox_2, self.product_img_2)

    def set_price_histogram(self, prod):
        file_path = prod.generate_price_histogram()
        pixmap = QtGui.QPixmap(file_path)
        self.price_dist_img.setPixmap(pixmap.scaled(self.price_dist_img.size(), QtCore.Qt.KeepAspectRatio))

    def set_combo_box_options(self, prod):
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
