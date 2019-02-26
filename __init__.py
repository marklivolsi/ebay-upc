from models import UPCFinder


TEST_UPC = '883929638482'


def main():
    upc = UPCFinder(TEST_UPC)
    upc.get_completed_listings()
    print(upc.completed_listings)
    print()
    upc.item_details_main_async_loop()
    print(upc.item_details)


if __name__ == '__main__':
    main()













# from yaml import load, YAMLError
# import requests
# import json
# import sys
#
# app_id = ''
# with open('ebay.yaml', 'r') as stream:
#     try:
#         yaml = load(stream)
#         app_id = yaml['api.ebay.com']['appid']
#     except YAMLError as exc:
#         print(exc)
#         sys.exit()
#
#
# #
# sample_upc = '883929638482'
# dvd_cat = '617'
#
# find_api = 'http://svcs.ebay.com/services/search/FindingService/v1'
# shop_api = 'http://open.api.ebay.com/shopping'
#
# find_operation = 'findCompletedItems'
# item_operation = 'GetSingleItem'
# response_format = 'JSON'
# global_id = 'EBAY-US'
# service_version = '1.13.0'
#
#
# find_params = {
#     'OPERATION-NAME': find_operation,
#     'SERVICE-VERSION': service_version,
#     'SECURITY-APPNAME': app_id,
#     'GLOBAL-ID': global_id,
#     'RESPONSE-DATA-FORMAT': response_format,
#     'categoryId': dvd_cat,
#     'keywords': sample_upc
# }
#
#
#
# response = requests.get(find_api, params=find_params)
# data = json.loads(response.text)
#
# parsed = data['findCompletedItemsResponse'][0]['searchResult'][0]['item']
#
# for item in parsed:
#     print(item)
#     print(type(item))
#
# item_id = parsed[10]['itemId']
# print()
# print()
# print(item_id)
#
#
# shop_params = {
#     'callname': item_operation,
#     'version': '967',
#     'appid': app_id,
#     'siteid': '0',
#     'responseencoding': response_format,
#     'ItemID': item_id,
#     'IncludeSelector': 'Description,ItemSpecifics'
# }
#
# r = requests.get(shop_api, params=shop_params)
# print(r.text)
# print(type(r.text))
# data = json.loads(response.text)
# print(data)

# count = data['findCompletedItemsResponse'][0]['searchResult'][0]['@count']
# print(parsed)


