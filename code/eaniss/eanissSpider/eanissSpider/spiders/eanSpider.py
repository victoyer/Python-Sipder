from scrapy import Selector, Spider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import re, random

from eanissSpider.items import EanissspiderItem, GetTypeIdItem


class eanissSpider(CrawlSpider):
    name = 'eais'
    start_urls = ['http://www.eaniss.com/']

    def parse(self, response):
        rel = Selector(response)
        # 匹配类别链接
        type_link = rel.xpath('//div[@id="J_mainCata"]//li//a/@href').extract()
        # 实例化模型对象
        item = GetTypeIdItem()
        # 匹配类别ID和名称
        type_info = re.findall(r'<h3 style="background.*id=(.*)">(.*)</a></h3', response.text)
        for sh in type_info:
            # 赋值模型
            item['typeID'] = sh[0]
            item['typeName'] = sh[1]

            # 返回有值模型
            yield item

        for ch in type_link:
            # 返回类别链接
            type_id = re.findall(r'\d+', ch)[0]
            yield Request(url='http://www.eaniss.com/' + str(ch), callback=self.get_detail_link,
                          meta={'type_id': type_id})

    def get_detail_link(self, response):
        rel = Selector(response)
        type_id = response.meta.get('type_id')
        detail_link = rel.xpath('//a[@class="productitem"]/@href').extract()
        for ch in detail_link:
            yield Request(url='http://www.eaniss.com/' + str(ch), callback=self.get_detail_data,
                          meta={'type_id': type_id})

    def get_detail_data(self, response):
        rel = Selector(response)

        # 实例化模型对象
        item = EanissspiderItem()
        # 商品名称
        names = rel.xpath('//*[@id="item-info"]/dl/dt/h1/text()').extract()
        # 商品价格
        prices = rel.xpath('//*[@id="ECS_SHOPPRICE"]/text()').extract()
        # 点击次数
        clicks = rel.xpath('//em[@class="red"]/text()').extract()
        # 商品图片
        imgs = rel.xpath('//*[@id="Zoomer"]/img/@src').extract()
        # 商品库存
        numbers = re.search(r'\d+件', response.text)
        # 商品描述
        contents = rel.xpath('//*[@id="item-info"]/dl/dt/p/span/text()').extract()

        # 赋值模型对象
        item['g_name'] = self.get_name(names)
        item['g_price'] = self.get_price(prices)
        item['g_click'] = self.get_click(clicks)
        item['g_img'] = self.get_img(imgs)
        item['g_number'] = self.get_number(numbers)
        item['g_content'] = self.get_content(contents)
        item['g_type'] = int(response.meta.get('type_id'))

        # 返回赋值item
        yield item

    def get_name(self, names):
        if len(names) > 0:
            return str(names[0])

    def get_price(self, prices):
        if len(prices) > 0:
            return int(re.search(r'\d+', prices[0])[0])

    def get_click(self, clicks):
        if len(clicks) > 0:
            return int(clicks[-1])

    def get_img(self, imgs):
        if len(imgs) > 0:
            return str('http://www.eaniss.com/' + str(imgs[0]))

    def get_number(self, numbers):
        if numbers[0]:
            return re.search(r'\d+', numbers[0])[0]

    def get_content(self, contents):
        if len(contents) > 0:
            return str(contents[0])
        else:
            return '无'
