from collections import Iterable

from helpers import *
from config import config


class ItemListing:

    def __init__(self, item_id, title, url, cat_id, cat_name, sell_state, price, ship_cost, currency):
        self.item_id = item_id
        self.title = title
        self.description = ''
        self.url = url
        self.img_url_arr = []
        self.cat_id = cat_id
        self.cat_name = cat_name
        self.sell_state = sell_state
        self.price = price
        self.ship_cost = ship_cost
        self.currency = currency

    def __repr__(self):
        return self.title


# TODO: Add sqlite3 functionality to save listings to DB.
# TODO: Add download img functionality

class UPCProduct:

    def __init__(self):
        self.upc = ''
        self.title = ''
        self.cat_name = ''
        self.cat_id = ''
        self.description = ''
        self.price = ''
        self.shipping = ''
        self.img = ''
        self.completed_listings = []
        self.completed_listing_details = {}
        self.img_list = []

    @property
    def price_array(self):
        """ Return array of float listing price values """
        if self.completed_listings:
            return [float(listing.price) for listing in self.completed_listings]
        else:
            return None

    def get_property_list(self, prop):
        """ Return array of given property for completed listings. Flattens if property is a list (i.e. img urls) """
        items = set()
        if self.completed_listings:
            for listing in self.completed_listings:
                item = getattr(listing, prop)
                # if type(item) == list:
                if isinstance(item, Iterable) and not isinstance(item, str):
                    for i in item:
                        items.add(i)
                else:
                    items.add(item)
        if items:
            return list(items)
        else:
            return None

    def get_price_statistic(self, func):
        """ Return string result of performing provided statistic function on price array """
        if self.price_array:
            return '${:.2f}'.format(func(self.price_array))
        else:
            return 'N/A'

    def generate_price_histogram(self):
        """ Generate histogram image and return file path """
        if self.price_array:
            file_path = '{}/{}.png'.format(config['chart_path'], self.upc)
            generate_histogram(self.price_array, file_path)
            return file_path

    # Methods to asynchronously fetch data for completed listings

    def main_fetch_loop(self):
        """ Main loop. Call this to collect all completed listing data for a given UPC """
        data = run_async_loop(self.fetch_completed_listings)
        self.parse_listings(data)
        self.completed_listings.sort(key=lambda x: x.item_id)
        run_async_loop(self.fetch_listing_details)
        self.update_listing_details()

    async def fetch_completed_listings(self, loop):
        """ Return JSON dictionary of completed listings based on product UPC """
        params = find_parameters(self.upc)
        url = [build_request_url('GET', config['finding_api_base'], params)]
        task = await async_batch_retrieve(loop, url, fetch)
        data = format_json(task.result())
        return data

    def parse_listings(self, data):
        """ Parse JSON dictionary of completed listings and append ItemListing objects to completed listings array """
        try:
            parsed_data = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
        except KeyError:
            return

        for item in parsed_data:
            item_id = item.get('itemId', ['N/A'])[0]
            title = item.get('title', ['N/A'])[0]
            url = item.get('viewItemURL', ['N/A'])[0]
            cat_id = item['primaryCategory'][0].get('categoryId', ['N/A'])[0]
            cat_name = item['primaryCategory'][0].get('categoryName', ['N/A'])[0]
            sell_state = item['sellingStatus'][0].get('sellingState', ['N/A'])[0]
            price = item['sellingStatus'][0].get('currentPrice', [{'__value__': ''}])[0]['__value__']
            ship_cost = item['shippingInfo'][0].get('shippingServiceCost', [{'__value__': ''}])[0]['__value__']
            currency = item['sellingStatus'][0].get('currentPrice', [{'@currencyId': ''}])[0]['@currencyId']

            listing = ItemListing(item_id, title, url, cat_id, cat_name, sell_state, price, ship_cost, currency)
            self.completed_listings.append(listing)

    def build_url_arr(self):
        """ Return url request array from completed item listings. """
        url_arr = []
        for listing in self.completed_listings:
            params = shop_parameters(listing.item_id)
            req = build_request_url('GET', config['shopping_api_base'], params)
            url_arr.append(req)
        return url_arr

    async def fetch_listing_details(self, loop):
        """ Async fetch completed listing data and append to completed listing detail dict  """
        url_arr = self.build_url_arr()
        tasks = await async_batch_retrieve(loop, url_arr, fetch)
        if tasks:
            for task in tasks:
                result = task.result()
                data = format_json(result)
                item_id = data['Item']['ItemID']
                self.completed_listing_details[item_id] = data

    def update_listing_details(self):
        """ Add description and image urls to ItemListing instances """
        for listing in self.completed_listings:
            data = self.completed_listing_details[listing.item_id]
            description = data['Item'].get('Description', '')
            img_url_arr = data['Item'].get('PictureURL', [])

            listing.description = description
            listing.img_url_arr = img_url_arr



    # async def download_img_list(self, loop):
    #     url_path_tup_list = []
    #     num = 0
    #     for img_url in self.img_list:
    #         write_path = '{}/{}-{}.jpg'.format(config['image_path'], self.upc, num)
    #         url_path_tup_list.append(img_url, write_path)


    # async def retrieve_image_array(self, loop):
    #     async with aiohttp.ClientSession(loop=loop) as session:
    #         tasks = []
    #         for listing in self.completed_listings:
    #             num = 0
    #             for image in listing.img_url_arr:
    #                 file_path = '{}/{}-{}.jpg'.format(config['image_path'], listing.item_id, num)
    #                 task = asyncio.ensure_future(download_image(image, file_path, session))
    #                 tasks.append(task)
    #                 self.img_list.append(file_path)
    #                 num += 1
    #         await asyncio.gather(*tasks, return_exceptions=True)

    # def image_array_main_async_loop(self):  # replace with run_async_loop
    #     try:
    #         loop = asyncio.get_event_loop()
    #         loop.run_until_complete(self.retrieve_image_array(loop))
    #     except client_exceptions.ClientConnectorError as e:
    #         print(e)
    #
    # def item_details_main_async_loop(self):  # replace with run_async_loop
    #     """ Main loop. Call this to retrieve details for completed listings """
    #     try:
    #         loop = asyncio.get_event_loop()
    #         loop.run_until_complete(self.retrieve_completed_listing_details(loop))
    #     except client_exceptions.ClientConnectorError as e:
    #         print(e)
