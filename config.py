from yaml import load, YAMLError

YAML_PATH = 'ebay.yaml'


def get_app_id(path_to_yaml):
    with open(path_to_yaml, 'r') as stream:
        try:
            yaml = load(stream)
            return yaml['api.ebay.com']['appid']
        except YAMLError as exception:
            print(exception)


config = {
        'finding_api_base': 'http://svcs.ebay.com/services/search/FindingService/v1',
        'shopping_api_base': 'http://open.api.ebay.com/shopping',
        'response_format': 'JSON',
        'find_operation_name': 'findCompletedItems',
        'shop_operation_name': 'GetSingleItem',
        'global_id': 'EBAY-US',
        'service_version': '1.13.0',
        'shopping_api_version': '967',
        'category_id': '617',
        'IncludeSelector': 'Description,ItemSpecifics',
        'siteid': '0',
        'app_id': get_app_id(YAML_PATH),
        'image_path': 'images',
        'chart_path': 'charts'
     }
