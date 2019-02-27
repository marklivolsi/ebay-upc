import requests
import json
from config import config
import urllib.request


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


def download_image(url):
    filename = url.rsplit('/', 1)[-1]
    urllib.request.urlretrieve(url, filename)
