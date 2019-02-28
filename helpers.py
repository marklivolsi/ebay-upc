import requests
import json
from config import config
import asyncio
import aiohttp
import aiofiles
import os
import matplotlib


def find_parameters(upc):
    """ Returns dictionary of parameters for use in building eBay finding service API GET request """
    params = {
        'OPERATION-NAME': config['find_operation_name'],
        'SERVICE-VERSION': config['service_version'],
        'SECURITY-APPNAME': config['app_id'],
        'GLOBAL-ID': config['global_id'],
        'RESPONSE-DATA-FORMAT': config['response_format'],
        'categoryId': config['category_id'],
        'keywords': upc
        }
    return params


def shop_parameters(item_id):
    """ Returns dictionary of parameters for use in building eBay shopping API GET request """
    params = {
        'callname': config['shop_operation_name'],
        'version': config['shopping_api_version'],
        'appid': config['app_id'],
        'siteid': config['siteid'],
        'responseencoding': config['response_format'],
        'ItemID': item_id,
        'IncludeSelector': config['IncludeSelector']
        }
    return params


def format_json(text):
    """ Formats text string as JSON (dictionary) """
    data = json.loads(text)
    return data


# def fetch(base, params):
#     """
#     Synchronous HTTP GET request
#     Arguments:
#         base = base API URL
#         params = dictionary of parameters, produced by find_parameters() or shop_parameters()
#     Returns:
#         string response or None
#     """
#     try:
#         response = requests.get(base, params=params)
#         return response.text
#     except requests.exceptions.RequestException as error:
#         print(error)
#         return


async def async_fetch(base, params, session):
    async with session.get(base, params=params) as response:
        return await response.text()


# def download_image(url, filename):
#     try:
#         file = open('images/{}.jpg'.format(filename), 'wb')
#         file.write(requests.get(url).content)
#         file.close()
#     except requests.exceptions.RequestException as error:
#         print(error)


async def download_image(url, file_path, session):
    async with session.get(url) as response:
        if response.status == 200:
            file = await aiofiles.open(file_path, mode='wb')
            await file.write(await response.read())
            await file.close()


def generate_histogram(arr, file_path):
    matplotlib.use('AGG', force=True)
    matplotlib.pyplot.ioff()

    # Set colors based on bin height
    N, bins, patches = matplotlib.pyplot.hist(arr, bins='auto')
    fracs = N / N.max()
    norm = matplotlib.colors.Normalize(fracs.min(), fracs.max())
    for this_frac, this_patch in zip(fracs, patches):
        color = matplotlib.pyplot.cm.viridis(norm(this_frac))
        this_patch.set_facecolor(color)

    matplotlib.pyplot.xlabel('Price ($ USD)')
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.savefig(file_path, bbox_inches='tight')


# Rewriting async functions

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def download_img(session, url, write_path):
    async with session.get(url) as response:
        file = await aiofiles.open(write_path, mode='wb')
        await file.write(await response.read())
        await file.close()


async def async_batch_retrieve(loop, url_arr, func, **kwargs):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = []
        for url in url_arr:
            task = asyncio.ensure_future(func(session=session, url=url, write_path=kwargs['write_path']))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)
        return tasks


def run_async_loop(func):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(loop))
    except aiohttp.client_exceptions.ClientConnectionError as error:
        print(error)
