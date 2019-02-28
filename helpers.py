import requests
import json
from config import config
import aiohttp
import aiofiles
import os


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


def fetch(base, params):
    """
    Synchronous HTTP GET request
    Arguments:
        base = base API URL
        params = dictionary of parameters, produced by find_parameters() or shop_parameters()
    Returns:
        string response or None
    """
    try:
        response = requests.get(base, params=params)
        return response.text
    except requests.exceptions.RequestException as error:
        print(error)
        return


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


async def download_image(url, item_id, session):
    async with session.get(url) as response:
        if response.status == 200:

            num = '0'
            for file in os.listdir('images/'):
                if item_id in file:
                    num = file.rsplit('-', 1)[-1]
            num = int(num) + 1
            filename = item_id + '-{}.jpg'.format(num)

            file = await aiofiles.open('images/{}'.format(filename), mode='wb')
            await file.write(await response.read())
            await file.close()
