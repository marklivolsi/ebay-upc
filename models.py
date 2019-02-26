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
        self.completed_listings = {}
        self.item_details = {}

    def get_completed_listings(self):
        data = fetch(config['finding_api_base'], params=find_parameters(self.upc))
        parsed_data = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
        for item in parsed_data:
            item_id = item['itemId'][0]
            self.completed_listings[item_id] = item

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
                data = json.loads(result)
                item_id = data['Item']['ItemID']
                self.item_details[item_id] = data

        # for item_id in self.completed_listings.keys():
        #     params = shop_parameters(item_id)
        #     print(params)
        #     req = build_request(base, params)
        #     print(req)
        # async with aiohttp.ClientSession(loop=loop) as session:

        # loop = asyncio.get_event_loop()
        # tasks = []
        # for item_id in self.completed_listings.keys():
        #     base = config['shopping_api_base']
        #     params = shop_parameters(item_id)
        #     task = loop.run_in_executor(None, fetch, base, params)
        #     tasks += task
        # await asyncio.gather(*tasks, return_exceptions=True)

    def item_details_main_async_loop(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.get_item_details(loop))
        except client_exceptions.ClientConnectorError as e:
            print(e)


    # def get_item_details(self):

        # async with aiohttp.ClientSession(loop=loop) as session:
        #     tasks = []
        #     for item_id in self.completed_listings.keys():
        #         base = config['shopping_api_base']
        #         params = shop_parameters(item_id)
        #         task = asyncio.ensure_future(fetch(base, params))
        #     await asyncio.gather(*tasks, return_exceptions=True)

        # for item_id in self.completed_listings.keys():
        #     data = fetch(config['shopping_api_base'], params=shop_parameters(item_id))
        #     self.item_details[item_id] = data
