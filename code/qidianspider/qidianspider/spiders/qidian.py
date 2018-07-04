import scrapy
from scrapy import Selector

# 创建一个爬虫类
class QidianSpider(scrapy.Spider):
    # 爬虫名称
    name = 'qidian'
    # 限制爬虫爬取范围
    allowed_domains = ['https://www.qidian.com/']
    # 指定爬虫开始爬取路径
    start_urls = ['https://www.qidian.com/']

    # 爬取信息返的回调函数
    def parse(self, response):
        res = Selector(response)
        men_type = res.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        men_href = res.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(men_type)
        print(men_href)

        return response
