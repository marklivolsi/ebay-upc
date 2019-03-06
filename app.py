import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from numpy import mean, median

from UI.main_window import Ui_Form
from models import UPCProduct
from helpers import *


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):

        # Initial setup
        super().__init__()
        self.setupUi(self)
        self.prod = UPCProduct()
        self.loop_run = False
        self.desc_index = 0
        self.ebay_img_index = 0
        self.saved_img_index = 0
        self.price_dist_img.setScaledContents(True)
        self.ebay_img.setScaledContents(False)
        self.saved_img.setScaledContents(False)

        # Button connections
        self.clear_btn.clicked.connect(self.clear)
        self.fetchlistings_btn.clicked.connect(self.main_loop)
        self.next_desc_btn.clicked.connect(self.next_description)
        self.prev_desc_btn.clicked.connect(self.prev_description)
        self.next_ebay_img_btn.clicked.connect(self.next_ebay_img)
        self.prev_ebay_img_btn.clicked.connect(self.prev_ebay_img)
        self.next_saved_img_btn.clicked.connect(self.next_saved_img)
        self.prev_saved_img_btn.clicked.connect(self.prev_saved_img)
        self.save_img_btn.clicked.connect(self.save_img)
        self.delete_img_btn.clicked.connect(self.delete_img)

        # Combobox connections
        self.title_combobox.activated.connect(self.set_title_field)
        self.catname_combobox.activated.connect(self.set_catname_field)
        self.catid_combobox.activated.connect(self.set_catid_field)

    def main_loop(self):
        """ Main loop. Fetches data and sets fields when provided a valid UPC """
        if not len(self.upc_field.text()) in (12, 13) or not self.upc_field.text().isdigit():
            QtWidgets.QMessageBox.about(self, '', 'Invalid UPC provided. Please enter a valid UPC number.')
            return

        if self.loop_run:
            self.prod = UPCProduct()
            self.clear_contents()
        self.prod.upc = self.upc_field.text()

        try:
            self.prod.main_fetch_loop()
            self.set_price_histogram()
            self.set_combo_box_options()
            self.set_price_statistics()
            self.populate_fields()
            self.loop_run = True
        except TypeError as err:
            print(err)

    # Methods for setting text fields

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

    # Methods for setting image fields

    def set_img(self, img_url, img_field):
        pixmap = QtGui.QPixmap.fromImage(qt_img_from_url(img_url))
        img_field.setPixmap(pixmap.scaled(img_field.size(), QtCore.Qt.KeepAspectRatio))

    def next_ebay_img(self):
        if self.loop_run:
            if self.ebay_img_index == len(self.prod.get_property_list('img_url_arr')) - 1:
                self.ebay_img_index = 0
            else:
                self.ebay_img_index += 1
            img_url = self.prod.get_property_list('img_url_arr')[self.ebay_img_index]
            self.set_img(img_url, self.ebay_img)

    def prev_ebay_img(self):
        if self.loop_run:
            if self.ebay_img_index == 0:
                self.ebay_img_index = len(self.prod.get_property_list('img_url_arr')) - 1
            else:
                self.ebay_img_index -= 1
            img_url = self.prod.get_property_list('img_url_arr')[self.ebay_img_index]
            self.set_img(img_url, self.ebay_img)

    def next_saved_img(self):
        if self.loop_run and self.prod.img_list:
            if self.saved_img_index == len(self.prod.img_list) - 1:
                self.saved_img_index = 0
            else:
                self.saved_img_index += 1
            img_url = self.prod.img_list[self.saved_img_index]
            self.set_img(img_url, self.saved_img)

    def prev_saved_img(self):
        if self.loop_run and self.prod.img_list:
            if self.saved_img_index == 0:
                self.saved_img_index = len(self.prod.img_list) - 1
            else:
                self.saved_img_index -= 1
            img_url = self.prod.img_list[self.saved_img_index]
            self.set_img(img_url, self.saved_img)

    def save_img(self):
        self.prod.img_list.append(self.prod.get_property_list('img_url_arr')[self.ebay_img_index])
        img_url = self.prod.img_list[-1]
        self.saved_img_index = len(self.prod.img_list) - 1
        self.set_img(img_url, self.saved_img)

    def delete_img(self):
        if self.prod.img_list:
            del self.prod.img_list[self.saved_img_index]
            if len(self.prod.img_list) == 0:
                self.saved_img.clear()
            else:
                self.prev_saved_img()

    # Methods for setting price histogram and statistics

    def set_price_histogram(self):
        file_path = self.prod.generate_price_histogram()
        pixmap = QtGui.QPixmap(file_path)
        self.price_dist_img.setPixmap(pixmap.scaled(self.price_dist_img.size(), QtCore.Qt.KeepAspectRatio))

    def set_combo_box_options(self):
        self.title_combobox.addItems(self.prod.get_property_list('title'))
        self.catname_combobox.addItems(self.prod.get_property_list('cat_name'))
        self.catid_combobox.addItems(self.prod.get_property_list('cat_id'))

    def set_price_statistics(self):
        self.minprice_val.setText(self.prod.get_price_statistic(min))
        self.maxprice_val.setText(self.prod.get_price_statistic(max))
        self.meanprice_val.setText(self.prod.get_price_statistic(mean))
        self.medianprice_val.setText(self.prod.get_price_statistic(median))
        self.numlistings_val.setText(str(len(self.prod.completed_listings)))

    # Methods for setting/resetting bulk fields

    def populate_fields(self):
        self.set_title_field()
        self.set_catname_field()
        self.set_catid_field()
        self.shipping_field.setText('0.00')
        self.set_description(0)
        self.set_img(self.prod.get_property_list('img_url_arr')[0], self.ebay_img)
        if self.prod.get_price_statistic(median) is not 'N/A':
            self.price_field.setText(self.prod.get_price_statistic(median))

    def clear_contents(self):
        self.search_field.setText('')
        self.title_field.setText('')
        self.catname_field.setText('')
        self.catid_field.setText('')
        self.price_field.setText('')
        self.shipping_field.setText('')
        self.description_field.setPlainText('')
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

        self.ebay_img.clear()
        self.saved_img.clear()

    def clear(self):
        self.clear_contents()
        self.upc_field.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
