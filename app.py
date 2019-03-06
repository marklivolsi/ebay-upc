import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from numpy import mean, median

from UI.main_window import Ui_Form
from models import UPCProduct
from helpers import *


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.prod = UPCProduct()
        self.loop_run = False
        self.desc_index = 0
        self.price_dist_img.setScaledContents(True)
        self.product_img_1.setScaledContents(False)
        self.product_img_2.setScaledContents(False)

        # TODO: Remove second image comboox.
        # TODO: Add 'save image' btn which adds selected url to array.
        # TODO: Add btns to cycle through saved image array.

        # Button connections
        self.clear_btn.clicked.connect(self.clear)
        self.fetchlistings_btn.clicked.connect(self.main_loop)
        self.next_desc_btn.clicked.connect(self.next_description)
        self.prev_desc_btn.clicked.connect(self.prev_description)

        # Combobox connections
        self.title_combobox.activated.connect(self.set_title_field)
        self.catname_combobox.activated.connect(self.set_catname_field)
        self.catid_combobox.activated.connect(self.set_catid_field)
        self.selectimg_combobox_1.activated.connect(self.set_img_combobox_1)
        self.selectimg_combobox_2.activated.connect(self.set_img_combobox_2)

    def main_loop(self):
        if not len(self.upc_field.text()) in (12, 13) or not self.upc_field.text().isdigit():
            QtWidgets.QMessageBox.about(self, '', 'Invalid UPC provided. Please enter a valid UPC number.')
            return

        if self.loop_run:
            self.prod = UPCProduct()
            self.clear_contents()
        self.prod.upc = self.upc_field.text()

        try:
            print(self.prod.upc)
            self.prod.main_fetch_loop()
            self.set_price_histogram()
            self.set_combo_box_options()
            self.set_price_statistics()
            self.populate_fields()
            self.loop_run = True
        except TypeError as err:
            print(err)

    def set_description(self, ind):
        try:
            self.description_field.setPlainText(strip_html_tags(self.prod.get_property_list('description')[ind]))
        except TypeError as err:
            print(err)

    def next_description(self):
        if self.loop_run:
            if self.desc_index == len(self.prod.get_property_list('description')) - 1:
                self.desc_index = 0
            else:
                self.desc_index += 1
            self.set_description(self.desc_index)

    def prev_description(self):
        if self.loop_run:
            self.desc_index -= 1
            self.set_description(self.desc_index)

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
        pixmap = QtGui.QPixmap.fromImage(qt_img_from_url(url))
        img_field.setPixmap(pixmap.scaled(img_field.size(), QtCore.Qt.KeepAspectRatio))

    def set_price_histogram(self):
        file_path = self.prod.generate_price_histogram()
        pixmap = QtGui.QPixmap(file_path)
        self.price_dist_img.setPixmap(pixmap.scaled(self.price_dist_img.size(), QtCore.Qt.KeepAspectRatio))

    def set_combo_box_options(self):
        self.selectimg_combobox_1.addItems(self.prod.get_property_list('img_url_arr'))
        self.selectimg_combobox_2.addItems(self.prod.get_property_list('img_url_arr'))
        self.title_combobox.addItems(self.prod.get_property_list('title'))
        self.catname_combobox.addItems(self.prod.get_property_list('cat_name'))
        self.catid_combobox.addItems(self.prod.get_property_list('cat_id'))

    def set_price_statistics(self):
        self.minprice_val.setText(self.prod.get_price_statistic(min))
        self.maxprice_val.setText(self.prod.get_price_statistic(max))
        self.meanprice_val.setText(self.prod.get_price_statistic(mean))
        self.medianprice_val.setText(self.prod.get_price_statistic(median))
        self.numlistings_val.setText(str(len(self.prod.completed_listings)))

    def populate_fields(self):
        self.set_title_field()
        self.set_catname_field()
        self.set_catid_field()
        self.shipping_field.setText('0.00')
        self.set_description(0)
        self.set_img_combobox_1()
        self.selectimg_combobox_2.setCurrentIndex(1)
        self.set_img_combobox_2()
        if self.prod.get_price_statistic(median) is not 'N/A':
            self.price_field.setText(self.prod.get_price_statistic(median))

    def clear_contents(self):
        self.search_field.setText('')
        # self.upc_field.setText('')
        self.title_field.setText('')
        self.catname_field.setText('')
        self.catid_field.setText('')
        self.price_field.setText('')
        self.shipping_field.setText('')
        self.description_field.setPlainText('')
        self.selectimg_combobox_1.setCurrentText('')
        self.selectimg_combobox_2.setCurrentText('')
        self.imgurl_field_1.setText('')
        self.imgurl_field_2.setText('')
        self.product_img_1.clear()
        self.product_img_2.clear()
        self.price_dist_img.clear()
        self.minprice_val.setText('N/A')
        self.maxprice_val.setText('N/A')
        self.medianprice_val.setText('N/A')
        self.meanprice_val.setText('N/A')
        self.numlistings_val.setText('N/A')
        self.selectimg_combobox_1.clear()
        self.selectimg_combobox_2.clear()
        self.title_combobox.clear()
        self.catname_combobox.clear()
        self.catid_combobox.clear()

        # self.prod = UPCProduct()
        # self.loop_run = False

    def clear(self):
        self.clear_contents()
        self.upc_field.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
