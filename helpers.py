import requests
import json
from config import config
import asyncio
import aiohttp
import aiofiles
import matplotlib
import matplotlib.pyplot as plt
import re
from PIL import Image
from PIL.ImageQt import ImageQt
from io import BytesIO


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
    plt.ioff()

    # Set colors based on bin height
    N, bins, patches = plt.hist(arr, bins='auto')
    fracs = N / N.max()
    norm = matplotlib.colors.Normalize(fracs.min(), fracs.max())
    for this_frac, this_patch in zip(fracs, patches):
        color = plt.cm.viridis(norm(this_frac))
        this_patch.set_facecolor(color)

    plt.xlabel('Price ($ USD)')
    plt.ylabel('Frequency')
    plt.savefig(file_path, bbox_inches='tight')

def strip_html_tags(html_str):
    print('html str is type:', type(html_str))
    return str(re.sub('<[^<]+?>', '', html_str))


def show_img_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    qt_img = ImageQt(img)
    return qt_img

def build_request_url(request_type, api_base, params):
    req = requests.Request(request_type, api_base, params=params)
    prep = req.prepare()
    return prep.url


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
            if kwargs:
                if 'write_path' in kwargs:
                    task = asyncio.ensure_future(func(session=session, url=url, write_path=kwargs['write_path']))
            else:
                task = asyncio.ensure_future(func(session=session, url=url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)
        if tasks:
            if len(tasks) == 1:
                return tasks[0]
            return tasks

def run_async_loop(func):
    try:
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(func(loop))
        return data
    except aiohttp.client_exceptions.ClientConnectionError as error:
        print(error)
