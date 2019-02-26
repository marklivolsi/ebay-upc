from models import UPCFinder


TEST_UPC = '883929638482'


def main():
    upc = UPCFinder(TEST_UPC)
    upc.retrieve_completed_listings()
    upc.item_details_main_async_loop()
    upc.update_completed_listing_details()
    for item in upc.completed_listings:
        print(item.item_id, item.price, item.img_url_arr, item.description)


if __name__ == '__main__':
    main()
