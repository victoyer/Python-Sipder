from random import choice
from scrapy.conf import settings
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        # 随机你获取一个请求头
        user_agent = choice(settings['USER_AGENT_LIST'])
        # 设置请求头中的User-Agent的参数
        request.headers.setdefault('User-Agent', user_agent)


class RandomProxy(object):
    def process_request(self, request, spider):
        # 随机获取一个IP
        proxy = choice(settings['REQUEST_PROXY_LIST'])
        # 设置请求IP
        request.meta['proxy'] = 'http://' + proxy
