from .client import Client
from .consts import *


class StackingAPI(Client):
    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='1'):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag)

    def get_offers(self,productId = '',protocolType = '',ccy = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy
        }
        return self._request_with_params(GET,STACK_DEFI_OFFERS,params)

    def purchase(self,productId = '',ccy = '',amt = '',term = ''):
        investData = [{
            'ccy':ccy,
            'amt':amt
        }]
        params = {
            'productId':productId,
            'investData':investData,
            'term':term
        }
        return self._request_with_params(POST,STACK_DEFI_PURCHASE,params)

    def redeem(self,ordId = '',protocolType = '',allowEarlyRedeem = ''):
        params = {
            'ordId':ordId,
            'protocolType':protocolType,
            'allowEarlyRedeem':allowEarlyRedeem
        }
        return self._request_with_params(POST,STACK_DEFI_REDEEM,params)

    def cancel(self,ordId = '',protocolType = ''):
        params = {
            'ordId':ordId,
            'protocolType':protocolType
        }
        return self._request_with_params(POST,STACK_DEFI_CANCEL,params)

    def get_activity_orders(self,productId = '',protocolType = '',ccy = '',state = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy,
            'state':state
        }
        return self._request_with_params(GET,STACK_DEFI_ORDERS_ACTIVITY,params)

    def stack_get_order_history(self,productId = '',protocolType = '',ccy = '',after = '',before = '',limit = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy,
            'after':after,
            'before':before,
            'limit':limit
        }
        return self._request_with_params(GET,STACK_DEFI_ORDERS_HISTORY,params)




