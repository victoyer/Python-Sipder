import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class DouBanSpider(CrawlSpider):
    # 爬虫名称
    name = 'douban'
    # 限制爬虫爬取范围
    allowed_domains = ['book.douban.com']
    # 起始爬取链接
    start_urls = ['https://book.douban.com/tag/?view=type']
    # 匹配链接
    tags_link = LinkExtractor(allow=(r'/tag/\w+'))
    # 对链接集合指定回调函数
    rules = [
        Rule(tags_link, callback='get_bock_link', follow=True)
    ]

    # 回调函数
    def get_bock_link(self, response):
        print(response)
