from scrapy import Spider, Selector, Request
import re

from renrencar.items import RenrencarItem


# from scrapy.spiders import Rule, CrawlSpider
# from scrapy.linkextractors import LinkExtractor


# //a[@class="province-item"]/@href

class RenCarSpider(Spider):
    # 爬虫名称
    name = 'rencar'
    # 限制域
    allowed_domains = ['renrenche.com']
    # 起始爬取链接
    start_urls = ['https://www.renrenche.com/cn/']
    # 列表页链接
    list_page = 'https://www.renrenche.com{area}ershouche/'

    # 回调函数
    def parse(self, response):
        # 转换数据格式以便XPATH匹配
        rel = Selector(response)
        # 获取地区链接
        area_links = rel.xpath('//div[@class="area-city-letter"]/div/a/@href').extract()
        # 组装链接
        for ch in area_links:
            # 回调get_page_maxnum函数获取最大页数并组装列表页链接
            list_page_link = self.list_page.format(area=ch)
            yield Request(url=list_page_link, callback=self.get_page_maxnum, meta={'list_page_link': list_page_link})

    def get_page_maxnum(self, response):
        # 获取最大页数
        rel = Selector(response)
        max_page = rel.xpath('//ul[@class="pagination js-pagination"]//li[@class=""]').xpath('./a/text()').extract()[0]
        # 获取列表页链接
        list_page_link = response.meta.get('list_page_link')
        # 组装链接
        for ch in range(1, int(max_page) + 1):
            detail_link = list_page_link + 'p' + str(ch)
            # 应用get_detail_link获取页面的详情页链接
            yield Request(url=detail_link, callback=self.get_detail_link, meta={'list_page_link': list_page_link})

    def get_detail_link(self, response):
        # # 获取区域链接
        page_link = str(response.meta.get('list_page_link')).replace('/ershouche/', '')
        # 正则匹配响应文件中的链接
        list_urls = re.findall(r'/car/\w+', response.text)

        # 实例化模型对象
        item = RenrencarItem()

        # 组装为详情页链接并存入redis
        for ch in list_urls:
            detail_link = str(page_link) + str(ch)
            item['url'] = detail_link
            yield item
