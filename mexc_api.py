import time
import json
import requests
import hmac
import hashlib

BASE_URL = 'https://contract.mexc.com'
API_KEY = 'mx0vglIoQqFLx6wZet'
SECRET_KEY = '6d73718cedc3423e9fb1217204b5d38e'


def _get_server_time():
    return int(time.time() * 1000)


def _sign_v1(api_key, api_secret, sign_params=None):
    if sign_params:
        sign = "%s%s%s" % (api_key, _get_server_time(), sign_params)
    else:
        sign = "%s%s" % (api_key, _get_server_time())
    sign = hmac.new(api_secret.encode('utf-8'), sign.encode('utf-8'),
                    hashlib.sha256).hexdigest()
    return sign


def get_ping():
    path = '/api/v1/contract/ping'
    url = '{}{}'.format(BASE_URL, path)
    response = requests.request('GET', url)
    return response.json()


def get_contract_detail(symbol=None):
    """
    获取合约信息
    :param symbol: 合约名
    :return:
    """
    path = '/api/v1/contract/detail'
    if symbol:
        path = f'{path}?symbol={symbol}'
    url = '{}{}'.format(BASE_URL, path)
    response = requests.request('GET', url)
    return response.json()


def get_depth(symbol, limit=None):
    """get depth data"""
    path = '/api/v1/contract/depth'
    path = f'{path}/{symbol}'
    if limit:
        path = f'{path}?limit={limit}'
    url = f'{BASE_URL}/{path}'
    response = requests.request('GET', url)
    return response.json()


# res = get_depth('ETH_USDT', 1)
# print(res)


def get_kline(symbol, interval=None, start=None, end=None):
    """get k-line data"""
    path = '/api/v1/contract/kline'
    path = f'{path}/{symbol}'
    if interval:
        path = f'{path}?interval={interval}'
    if start:
        path = f'{path}&start={start}'
    if end:
        path = f'{path}&end={end}'
    url = f'{BASE_URL}/{path}'
    response = requests.request('GET', url)
    return response.json()


# res = get_kline('ETH_USDT')
# print(res)


def get_account_assets(api_key, api_secret):
    """get account information"""
    method = 'GET'
    path = '/api/v1/private/account/assets'
    url = '{}{}'.format(BASE_URL, path)
    sign = _sign_v1(api_key, api_secret)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, headers=headers)
    return response.json()


# res = get_account_assets()
# print(res)


def get_account_asset_currency(api_key, api_secret, currency):
    """get account information"""
    method = 'GET'
    path = '/api/v1/private/account/asset/' + currency
    url = '{}{}'.format(BASE_URL, path)
    sign = _sign_v1(api_key, api_secret)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, headers=headers)
    return response.json()


# res = get_account_asset_currency(currency='USDT')
# print(res)


def history_positions(api_key, api_secret, page_num, page_size=None, symbol=None):
    """get history positions"""
    method = 'GET'
    path = '/api/v1/private/position/list/history_positions'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {
        'page_num': page_num
    }
    if page_size:
        data_original = {"page_size": page_size}
    if symbol:
        data_original = {"symbol": symbol}
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    url = "%s%s%s" % (url, "?", data)
    response = requests.request(method, url, headers=headers)
    return response.json()


# res = history_positions(page_num=1, symbol="BTC_USDT")
# print(res)


def get_open_positions(api_key, api_secret, symbol=None):
    """get Open Positions"""
    method = 'GET'
    path = '/api/v1/private/position/open_positions'
    url = '{}{}'.format(BASE_URL, path)
    if symbol:
        data_original = {"symbol": symbol}
    else:
        data_original = {}
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    url = "%s%s%s" % (url, "?", data)
    response = requests.request(method, url, headers=headers)
    return response.json()


# res = get_open_positions(symbol="BTC_USDT")
# print(res)


def get_position_funding_records(api_key, api_secret, page_num=None, page_size=None, symbol=None, position_id=None):
    """get funding records"""
    method = 'GET'
    path = '/api/v1/private/position/funding_records'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {}
    if page_num:
        data_original.update({'page_num': page_num})
    if page_size:
        data_original.update({'page_size': page_size})
    if symbol:
        data_original.update({'symbol': symbol})
    if position_id:
        data_original.update({'position_id': position_id})
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, params=data, headers=headers)
    return response.json()


# res = get_position_funding_records()
# print(res)


def get_open_orders(api_key, api_secret, page_num=None, page_size=None, symbol=None):
    """get Open Orders"""
    method = 'GET'
    path = '/api/v1/private/order/list/open_orders'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {}
    if page_num:
        data_original.update({'page_num': page_num})
    if page_size:
        data_original.update({'page_size': page_size})
    if symbol:
        data_original.update({'symbol': symbol})
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, params=data, headers=headers)
    return response.json()


# res = get_open_orders(symbol="ETH_USDT")
# print(res)


def get_history_orders(api_key, api_secret, page_num=None, page_size=None, symbol=None, states=None, category=None,
                       start_time=None, end_time=None, side=None):
    """get History Orders"""
    method = 'GET'
    path = '/api/v1/private/order/list/history_orders'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {}
    if page_num:
        data_original.update({'page_num': page_num})
    if page_size:
        data_original.update({'page_size': page_size})
    if symbol:
        data_original.update({'symbol': symbol})
    if states:
        data_original.update({'states': states})
    if category:
        data_original.update({'category': category})
    if start_time:
        data_original.update({'start_time': start_time})
    if end_time:
        data_original.update({'end_time': end_time})
    if side:
        data_original.update({'side': side})
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, params=data, headers=headers)
    return response.json()


# res = get_history_orders(symbol="BTC_USDT")
# print(res)


def get_orders_by_external(api_key, api_secret, symbol, external_oid):
    """get orders by external_id"""
    method = 'GET'
    path = '/api/v1/private/order/external'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {
        'symbol': symbol,
        'external_oid': external_oid
    }
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, params=data, headers=headers)
    return response.json()


# res = get_orders_by_external(symbol="ETH_USDT", external_oid="xxx")
# print(res)


def get_orders_by_orderId(api_key, api_secret, order_id):
    """get orders by order_id"""
    method = 'GET'
    path = '/api/v1/private/order/get/' + order_id
    url = '{}{}'.format(BASE_URL, path)
    sign = _sign_v1(api_key, api_secret)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, headers=headers)
    return response.json()


# res = get_orders_by_orderId(order_id="xxx")
# print(res)


def get_orders_deals(api_key, api_secret, symbol, page_num=None, page_size=None, start_time=None, end_time=None):
    """get order deals"""
    method = 'GET'
    path = '/api/v1/private/order/list/order_deals'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {
        'symbol': symbol,
    }
    if page_num:
        data_original.update({'page_num': page_num})
    if page_size:
        data_original.update({'page_size': page_size})
    if start_time:
        data_original.update({'start_time': start_time})
    if end_time:
        data_original.update({'end_time': end_time})
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, params=data, headers=headers)
    return response.json()


# res = get_orders_deals(symbol="ETH_USDT")
# print(res)


# under maintenance
def post_place(api_key, api_secret, symbol, price, vol, side, type, openType, leverage=None, positionId=None,
               externalOid=None, stopLossPrice=None, takeProfitPrice=None, positionMode=None, reduceOnlt=None):
    """place new order"""
    method = 'POST'
    path = '/api/v1/private/order/submit'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {
        'symbol': symbol,
        'price': price,
        'vol': vol,
        'side': side,
        'type': type,
        'openType': openType
    }
    if leverage:
        data_original.update({"leverage": leverage})
    if positionId:
        data_original.update({"positionId": positionId})
    if externalOid:
        data_original.update({"externalOid": externalOid})
    if stopLossPrice:
        data_original.update({"stopLossPrice": stopLossPrice})
    if takeProfitPrice:
        data_original.update({"takeProfitPrice": takeProfitPrice})
    if positionMode:
        data_original.update({"positionMode": positionMode})
    if reduceOnlt:
        data_original.update({"reduceOnlt": reduceOnlt})
    data = json.dumps(data_original)
    params = _sign_v1(api_key, api_secret, sign_params=data)
    headers = {
        "ApiKey": api_key,
        "Request-Time": str(_get_server_time()),
        "Signature": params,
        "Content-Type": "application/json"
    }
    response = requests.request(
        method, url, data=data, headers=headers)
    return response.json()


# res = post_place(symbol='BTC_USDT', price='20000', vol='1', side=1, type=1, openType=2)
# print(res)


def main():
    pass


if __name__ == '__main__':
    main()
