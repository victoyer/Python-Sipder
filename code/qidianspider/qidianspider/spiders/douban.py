import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule, CrawlSpider
from qidianspider.items import DouBanspiderItem


class DouBanSpider(CrawlSpider):
    # 指定爬虫名称
    name = 'douban'
    # 限制爬虫爬取范围
    # allowed_domains = ['https://movie.douban.com/']
    # 指定爬虫开始爬取范围
    # crawl_list = []
    # for ch in range(10):
    #     url = 'https://movie.douban.com/top250?start=' + str(ch * 25)
    #     crawl_list.append(url)
    # start_urls = crawl_list

    start_urls = {
        'https://movie.douban.com/top250',
    }

    rules = (
        Rule(LinkExtractor(allow=r'https://movie.douban.com/top250.*'), callback='parse_item'),
    )

    # 爬虫获取资源后的回调函数
    def parse_item(self, response):
        result = Selector(response)
        itmes = DouBanspiderItem()

        # 电影名称
        itmes['name'] = result.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()

        # 电影图片
        itmes['avator'] = result.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()

        # 导演和主演名称
        director = result.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').extract()
        itmes['directors'] = [info.strip().replace('\xa0', '') for info in director]

        # 年份/国家/类型
        movie_info = result.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').extract()
        itmes['year'], itmes['guojia'], itmes['classfication'] = [], [], []
        for info in movie_info:
            itmes['year'] = str(info).split('/')[0].strip()
            itmes['guojia'] = str(info).split('/')[1].strip()
            itmes['classfication'] = str(info).split('/')[2].strip()

        # 电影评分
        itmes['score'] = result.xpath(
            '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()').extract()

        # print(itmes)
        return itmes
