import scrapy, json
from scrapy import Selector
from scrapy import Request

from lianjiaspider.items import MasterRedisItem


class LianJiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    url = 'https://cd.lianjia.com/ershoufang'

    def start_requests(self):
        yield Request(url=self.url)

    def parse(self, response):
        res = Selector(response)
        # 各区域链接
        area_links = res.xpath('//div[@data-role="ershoufang"]//a/@href').extract()
        area_link = [ch.replace('/ershoufang', '') for ch in area_links]

        # 各区域名称
        area_name = res.xpath('//div[@data-role="ershoufang"]//a/text()').extract()

        # 组装链接发送请求回调函数
        for ch in range(len(area_link)):
            area_url = self.url + area_link[ch]
            yield Request(url=area_url, callback=self.get_page, meta={'name': area_name[ch], 'area_url': area_url})

    def get_page(self, response):
        res = Selector(response)

        # 最大分页数
        max_page = json.loads(res.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])[
            'totalPage']

        # 组装链接发送请求并指定回调函数
        area_url = response.meta.get('area_url')
        area_name = response.meta.get('name')
        for ch in range(1, max_page + 1):
            item = MasterRedisItem()
            item['url'] = area_url + 'pg' + str(ch) + '/'
            item['name'] = area_name
            yield item
