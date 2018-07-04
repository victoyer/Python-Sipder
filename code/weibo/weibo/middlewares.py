from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random
from scrapy.conf import settings


class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        user_agent = random.choice(settings['USER_AGENT_LIST'])
        request.headers.setdefault('User-Agent', user_agent)


class RandomProxy(object):
    def process_request(self, request, spider):
        random_proxy = random.choice(settings['PROXY'])
        request.meta['proxy'] = 'http://' + random_proxy
