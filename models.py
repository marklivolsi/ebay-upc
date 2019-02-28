from helpers import *
from config import config
import asyncio
import aiohttp
from aiohttp import client_exceptions
import requests
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib import colors
# from itertools import chain


class Product:

    def __init__(self):
        self.upc = ''
        self.title = ''
        self.cat_name = ''
        self.cat_id = ''
        self.description = ''
        self.price = None
        self.shipping = None
        self.img = ''
        self.completed_listings = []
        self.completed_listing_details = {}
        self.img_list = []

    @property
    def price_array(self):
        if self.completed_listings:
            return [float(listing.price) for listing in self.completed_listings]
        else:
            return None

    def get_price_statistic(self, func):
        if self.price_array:
            return str(round(func(self.price_array), 2))
        else:
            return 'N/A'
        # if self.completed_listings:
        #     # price_arr = [float(listing.price) for listing in self.completed_listings]
        #     return str(round(func(self.price_array), 2))
        # else:
        #     return 'N/A'

    async def get_completed_listings(self, loop):
        params = find_parameters(self.upc)
        url = [build_request_url('GET', config['finding_api_base'], params)]
        task = await async_batch_retrieve(loop, url, fetch)
        data = format_json(task.result())

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


    # def retrieve_completed_listings(self):  # parsing should be separate function
    #     """ Retrieve completed listings for given UPC """
    #     params = find_parameters(self.upc)
    #     response = fetch_old(config['finding_api_base'], params=params)
    #     data = format_json(response)
    #     try:
    #         parsed_data = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
    #     except KeyError:
    #         return
    #     for item in parsed_data:
    #         item_id = item.get('itemId', ['N/A'])[0]
    #         title = item.get('title', ['N/A'])[0]
    #         url = item.get('viewItemURL', ['N/A'])[0]
    #         cat_id = item['primaryCategory'][0].get('categoryId', ['N/A'])[0]
    #         cat_name = item['primaryCategory'][0].get('categoryName', ['N/A'])[0]
    #         sell_state = item['sellingStatus'][0].get('sellingState', ['N/A'])[0]
    #         price = item['sellingStatus'][0].get('currentPrice', [{'__value__': ''}])[0]['__value__']
    #         ship_cost = item['shippingInfo'][0].get('shippingServiceCost', [{'__value__': ''}])[0]['__value__']
    #         currency = item['sellingStatus'][0].get('currentPrice', [{'@currencyId': ''}])[0]['@currencyId']
    #
    #         listing = ItemListing(item_id, title, url, cat_id, cat_name, sell_state, price, ship_cost, currency)
    #         self.completed_listings.append(listing)

    # TODO: Use requests to build full URL to pass to generic async retrieve func

    async def get_listing_details(self, loop):
        # Build request URLs
        url_arr = []
        for listing in self.completed_listings:
            params = shop_parameters(listing.item_id)
            # req = requests.Request('GET', config['shopping_api_base'], params=params)
            # prep = req.prepare()
            req = build_request_url('GET', config['shopping_api_base'], params)
            url_arr.append(req)

        tasks = await async_batch_retrieve(loop, url_arr, fetch)
        for task in tasks:
            result = task.result()
            data = format_json(result)
            item_id = data['Item']['ItemID']
            self.completed_listing_details[item_id] = data

    # async def retrieve_completed_listing_details(self, loop):  # combine async download funcs into one helper func
    #     """ Asynchronously retrieve details for completed listings based on item ID """
    #     base = config['shopping_api_base']
    #     async with aiohttp.ClientSession(loop=loop) as session:
    #         tasks = []
    #         for listing in self.completed_listings:
    #             params = shop_parameters(listing.item_id)
    #             task = asyncio.ensure_future(async_fetch(base, params, session))
    #             tasks.append(task)
    #         await asyncio.gather(*tasks, return_exceptions=True)
    #         for task in tasks:
    #             result = task.result()
    #             data = format_json(result)
    #             item_id = data['Item']['ItemID']
    #             self.completed_listing_details[item_id] = data

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
            print(e)

    def update_completed_listing_details(self):
        """ Add description and img urls to ItemListing instances """
        for listing in self.completed_listings:
            data = self.completed_listing_details[listing.item_id]

            description = data['Item'].get('Description', '')
            img_url_arr = data['Item'].get('PictureURL', [])

            listing.description = description
            listing.img_url_arr = img_url_arr

    # TODO: Add make folder for this upc function

    """ Chart Functions """

    def generate_price_histogram(self):
        if self.price_array:
            file_path = '{}/{}.jpg'.format(config['chart_path'], self.upc)
            generate_histogram(self.price_array, file_path)
            return file_path

        # if self.completed_listings:
        #     price_arr = [float(listing.price) for listing in self.completed_listings]
        #     file_path = '{}/{}.jpg'.format(config['chart_path'], self.upc)
        #     generate_histogram(price_arr, file_path)
        #     return file_path
        # else:
        #     pass
            # matplotlib.use('AGG', force=True)
            # plt.ioff()
            #
            # prices = [float(listing.price) for listing in self.completed_listings]
            # # n_bins = 20  # np.arange(min(prices), max(prices) + 1, 1)
            # # n_bins = len(prices)
            #
            # # Set color for each bin based on height.
            # N, bins, patches = plt.hist(prices, bins='auto')
            # fracs = N / N.max()
            # norm = colors.Normalize(fracs.min(), fracs.max())
            # for thisfrac, thispatch in zip(fracs, patches):
            #     # noinspection PyUnresolvedReferences
            #     color = plt.cm.viridis(norm(thisfrac))
            #     thispatch.set_facecolor(color)
            #
            # file_path = '{}/{}.png'.format(config['chart_path'], self.upc)
            # plt.xlabel('Price ($ USD)')
            # plt.ylabel('Frequency')
            # plt.savefig(file_path, bbox_inches='tight')
            #
            # return file_path


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
