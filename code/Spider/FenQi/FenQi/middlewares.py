from scrapy.http import HtmlResponse
from time import sleep


class SeleniumAdChromeMiddleware(object):
    """
    定义一个selenium form Chrome的请求中间件
    """

    # 重写process_request方法
    def process_request(self, request, spider):
        # 判断这个爬虫名来执行获取页面源码操作
        if spider.name == 'fq':
            # 请求request中的url获取服务器响应文件
            spider.driver.get(request.url)
            # 延时一秒
            sleep(1)
            # 定义一个把页面拉取到底的JS
            js = 'var q=document.documentElement.scrollTop=10000'
            # 执行先前定义的JS
            spider.driver.execute_script(js)
            # 延时一秒
            sleep(1)
            # 使用HtmlResponse对象返回获取的请求数据
            return HtmlResponse(spider.driver.current_url, body=spider.driver.page_source.encode('utf-8'),
                                request=request)
        # 不是爬虫则不执行
        else:
            return
