from helpers import find_parameters, shop_parameters, async_fetch, fetch #, build_request, async_fetch
from config import config
import asyncio
import aiohttp
from aiohttp import client_exceptions
import json


class UPCFinder:

    def __init__(self, upc):
        self.upc = upc
        self.find_params = find_parameters(self.upc)
        # self.completed_listings = {}
        self.item_details = {}
        self.completed_listings = []

    # def get_completed_listings(self):  # Replace with get completed item ids
    #     data = fetch(config['finding_api_base'], params=find_parameters(self.upc))
    #     parsed_data = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
    #     for item in parsed_data:
    #         item_id = item['itemId'][0]
    #         self.completed_listings[item_id] = item

    def retrieve_completed_listings(self):
        """ Retrieve completed listings for given UPC """
        params = find_parameters(self.upc)
        data = fetch(config['finding_api_base'], params=params)
        parsed_data = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
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

    async def get_item_details(self, loop):
        base = config['shopping_api_base']
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = []
            for item_id in self.completed_listings.keys():
                params = shop_parameters(item_id)
                task = asyncio.ensure_future(async_fetch(base, params, session))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
            for task in tasks:
                result = task.result()

                # data = json.loads(result)
                # item_id = data['Item']['ItemID']
                # self.item_details[item_id] = data

    def item_details_main_async_loop(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.get_item_details(loop))
        except client_exceptions.ClientConnectorError as e:
            print(e)


class ItemListing:

    def __init__(self, item_id, title, url, cat_id, cat_name, sell_state, price, ship_cost, currency):
        self.item_id = item_id  # ItemID
        self.title = title  # Title
        self.description = ''  # Description
        self.url = url  # ViewItemURLForNaturalSearch
        self.img_url_arr = []  # PictureURL
        self.cat_id = cat_id  # PrimaryCategoryID
        self.cat_name = cat_name  # PrimaryCategoryName
        self.sell_state = sell_state
        self.price = price  # ConvertedCurrentPrice['Value']
        self.ship_cost = ship_cost
        self.currency = currency  # ConvertedCurrentPrice['CurrencyID']

