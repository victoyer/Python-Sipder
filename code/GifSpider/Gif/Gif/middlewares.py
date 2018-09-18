from random import choice
from scrapy.conf import settings
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class GifDownloaderMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        # 随机获取一个user-agnet参数
        user_agent = choice(settings['USER_AGENT_LIST'])
        # 设置请求头的User-Agent参数
        request.headers.setdefault('User-Agent', user_agent)
