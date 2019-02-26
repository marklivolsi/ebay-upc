from models import Product


TEST_UPC = '883929638482'


def main():
    upc = Product(TEST_UPC)
    upc.retrieve_completed_listings()
    upc.item_details_main_async_loop()
    upc.update_completed_listing_details()
    print('mean: ', upc.mean_price_completed_listings)
    print('median: ', upc.median_price_completed_listings)
    # for item in upc.completed_listings:
    #     print(item.item_id, item.price, item.img_url_arr, item.description)


if __name__ == '__main__':
    main()
