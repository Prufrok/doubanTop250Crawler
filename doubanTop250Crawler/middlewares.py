# Define here the models for your spider middleware

import requests
import random
import string
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class DoubanMiddleware(RetryMiddleware):
    # proxy pool is built with reference to https://github.com/jhao104/proxy_pool
    @staticmethod
    def get_proxy():
        proxy = requests.get('http://127.0.0.1:5000/get/').json()
        return f'https://{proxy["proxy"]}'

    @staticmethod
    def delete_proxy(proxy):
        requests.get(f'http://127.0.0.1:5000/delete/?proxy={proxy}')

    # randomize bid (cookie) strategy is referred to
    # https://zhuanlan.zhihu.com/p/84554363
    # and https://zhuanlan.zhihu.com/p/24035574
    @staticmethod
    def get_bid():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))

    @staticmethod
    def modify_proxy_cookie(request):
        # remove the proxy which is likely banned
        # and log a warning message
        DoubanMiddleware.delete_proxy(request.meta['proxy'])
        logging.warning('\n'.join([
            f'\nProxy {request.meta["proxy"]} is removed',
            f'due to a bad request for {request.url}']))
        # modify the request proxy and bid cookie
        # before returning back to retry process
        request.meta['proxy'] = DoubanMiddleware.get_proxy()
        request.cookies['bid'] = DoubanMiddleware.get_bid()
        return request

    def process_request(self, request, spider):
        request.headers['Connection'] = 'close'
        request.meta['dont_redirect'] = True
        request.cookies['bid'] = DoubanMiddleware.get_bid()
        request.meta['download_timeout'] = 15
        request.meta['proxy'] = DoubanMiddleware.get_proxy()

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in [500, 502, 503, 504, 522, 524, 408, 403, 400, 302, 301]:
            request = DoubanMiddleware.modify_proxy_cookie(request)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if (
            isinstance(exception, self.EXCEPTIONS_TO_RETRY)
            and not request.meta.get('dont_retry', False)
        ):
            request = DoubanMiddleware.modify_proxy_cookie(request)
            return self._retry(request, exception, spider)
