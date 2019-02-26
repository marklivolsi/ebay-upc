import requests
from requests import Session, Request
import json
from config import config
import asyncio
import aiohttp


def find_parameters(upc):
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


def fetch(base, params):
    try:
        response = requests.get(base, params=params)
        data = json.loads(response.text)
        return data
    except requests.exceptions.RequestException as error:
        print(error)
        return


async def async_fetch(base, params, session):
    async with session.get(base, params=params) as response:
        return await response.text()
        # data = json.loads(response.text())
        # return await data



# def build_request(base, params):
#     req = Request('GET', base, params).prepare()
#     return req
#     # print(req.url)
