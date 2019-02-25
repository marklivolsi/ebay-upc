# from ebaysdk.finding import Connection as Finding
# from ebaysdk.exception import ConnectionError
import requests

sample_upc = '883929638482'
dvd_cat = '617'


endpoint = 'https://api.ebay.com/ws/api.dll'


xml = '<GetItemRequest xmlns="urn:'




# product = {
#   'productId': {
#     '#text': sample_upc,
#     '@attrs': {'type': 'UPC'}
#    }
# }
#
# from ebaysdk.utils import dict2xml
# print(dict2xml(product))
#
#
# try:
#     api = Finding(config_file='ebay.yaml')
#     response = api.execute('findItemsByProduct', {'productID type="UPC"': sample_upc}, {'categoryID': dvd_cat})
#     print(response.dict())
# except ConnectionError as e:
#     print(e)
#     print(e.response.dict())
#



