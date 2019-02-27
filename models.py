from helpers import find_parameters, shop_parameters, async_fetch, fetch, format_json
from config import config
import asyncio
import aiohttp
from aiohttp import client_exceptions
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors


class Product:

    def __init__(self):
        self.upc = None
        self.title = ''
        self.cat_name = ''
        self.cat_id = ''
        self.description = ''
        self.price = None
        self.shipping = None
        self.img = ''
        self.completed_listings = []
        self.completed_listing_details = {}

    @property
    def mean_price_completed_listings(self):
        if self.completed_listings:
            prices = [float(listing.price) for listing in self.completed_listings]
            return np.mean(prices)
        else:
            return None

    @property
    def median_price_completed_listings(self):
        if self.completed_listings:
            prices = [float(listing.price) for listing in self.completed_listings]
            return np.median(prices)
        else:
            return None

    @property
    def min_price_completed_listings(self):
        if self.completed_listings:
            return min(float(listing.price) for listing in self.completed_listings)
        else:
            return None

    @property
    def max_price_completed_listings(self):
        if self.completed_listings:
            return max(float(listing.price) for listing in self.completed_listings)
        else:
            return None

    def retrieve_completed_listings(self):
        """ Retrieve completed listings for given UPC """
        params = find_parameters(self.upc)
        response = fetch(config['finding_api_base'], params=params)
        data = format_json(response)
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

    async def retrieve_completed_listing_details(self, loop):
        """ Asynchronously retrieve details for completed listings based on item ID """
        base = config['shopping_api_base']
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = []
            for listing in self.completed_listings:
                params = shop_parameters(listing.item_id)
                task = asyncio.ensure_future(async_fetch(base, params, session))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
            for task in tasks:
                result = task.result()
                data = format_json(result)
                item_id = data['Item']['ItemID']
                self.completed_listing_details[item_id] = data

    def item_details_main_async_loop(self):
        """ Main loop. Call this to retrieve details for completed listings """
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.retrieve_completed_listing_details(loop))
        except client_exceptions.ClientConnectorError as e:
            print(e)

    def update_completed_listing_details(self):
        """ Add description and img urls to ItemListing instances """
        for listing in self.completed_listings:
            data = self.completed_listing_details[listing.item_id]

            description = data['Item'].get('Description', '')
            img_url_arr = data['Item'].get('PictureURL', [])

            listing.description = description
            listing.img_url_arr = img_url_arr

    def price_histogram(self):
        if self.completed_listings:

            matplotlib.use('AGG', force=True)
            plt.ioff()

            prices = [float(listing.price) for listing in self.completed_listings]
            n_bins = 20  # np.arange(min(prices), max(prices) + 1, 1)

            # Set color for each bin based on height.
            N, bins, patches = plt.hist(prices, bins=n_bins)
            fracs = N / N.max()
            norm = colors.Normalize(fracs.min(), fracs.max())
            for thisfrac, thispatch in zip(fracs, patches):
                # noinspection PyUnresolvedReferences
                color = plt.cm.viridis(norm(thisfrac))
                thispatch.set_facecolor(color)

            plt.xlabel('Price ($ USD)')
            plt.ylabel('Frequency')
            plt.savefig('{}.png'.format(self.upc), bbox_inches='tight')


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

