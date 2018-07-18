import scrapy
import re
from tpsSpider.items import TpsspiderItem


class TpsSpider(scrapy.Spider):
    # 爬虫名称
    name = 'tps'
    # 起始链接
    start_urls = ['https://cctvvip.tps138.com/index/']

    def parse(self, response):
        # 获取分类链接
        rel = scrapy.Selector(response)
        type_link = rel.xpath('//a[@class="category"]/@href').extract()
        # 如果结果不为空
        if len(type_link) > 0:
            # 获取每个分类的最大页数
            for ch in type_link:
                yield scrapy.Request(url=ch, callback=self.get_maxPage, meta={'typeLink': ch})

    def get_maxPage(self, response):
        # 获取每个分类的最大页数
        rel = scrapy.Selector(response)
        max_page_link = rel.xpath('/html/body/main/div/div/div/ul/li/a/@href').extract()
        # 如果结果不为空
        if len(max_page_link) > 0:
            # 获取最大页码数
            max_page = max_page_link[-1]
            max_page_num = max_page.split('=')[-1]

            # 获取meta数据
            typeFlag = response.meta.get('typeLink').split('=')[-1]
            # 拼接链接
            for ch in range(1, int(max_page_num) + 1):
                list_path = 'https://cctvvip.tps138.com' + str(max_page[:max_page.rindex('=')] + '=%d' % ch)
                # 获取详情页链接
                yield scrapy.Request(url=list_path, callback=self.get_detail_link, meta={'typeFlag': typeFlag})

    def get_detail_link(self, response):
        # 获取详情页链接
        rel = scrapy.Selector(response)
        detail_link = rel.xpath('//dl[@class="tit"]//a/@href').extract()
        # 实例化模型对象
        item = TpsspiderItem()
        # 获取商品类型
        item['flag'] = response.meta.get('typeFlag')

        if len(detail_link) > 0:
            # 拼接链接
            for ch in detail_link:
                item['url'] = 'https://cctvvip.tps138.com' + ch
                yield item

