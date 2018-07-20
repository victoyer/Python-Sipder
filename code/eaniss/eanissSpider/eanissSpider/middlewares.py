from scrapy.conf import settings
from random import choice
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        # 获取一个UserAgnet
        UserAgent = choice(settings['USER_AGENT_LIST'])
        # 设置请求头中的UserAgent参数
        request.headers.setdefault('User-Agent', UserAgent)
