from random import choice
from scrapy.conf import settings
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


# 请求头中间件
class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        # 随机获取一个user_agent
        user_agent = choice(settings['USER_AGENT_LIST'])
        # 设置请求头的User-Agent的参数
        request.headers.setdefault('User-Agent', user_agent)
