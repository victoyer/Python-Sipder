from scrapy import Spider, Selector, Request
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from FenQi.items import FenqiItem

# 定义一个去处列表空值的函数
def net_empty(elment):
    return elment.strip()


class FenQiSpider(Spider):
    # 定义爬虫名称
    name = 'fq'
    # 限制爬虫的爬取范围
    allowed_domains = ['fenqile.com']
    # 爬虫起始爬取链接
    start_urls = ['https://www.fenqile.com/']

    # 初始化selenium的Chrome对象实例
    def __init__(self):
        super(FenQiSpider, self).__init__()
        # 捕获爬虫关闭时发送的spider_closed信号
        dispatcher.connect(self.closeSpider, signals.spider_closed)
        # 获取一个属于Chrome的options对象
        options = webdriver.ChromeOptions()
        # 设置Chrome浏览器对象实例的请求参数
        options.add_argument('lang=zh_CN.UTF-8')  # 中文 UTF-8
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--disable-gpu')  # 规避BUG
        # 设置好的参数赋值给Chrome
        self.driver = webdriver.Chrome(chrome_options=options)

    # start_urls默认回调函数
    def parse(self, response):
        # 获取请求返回的数据转换为lxml
        rel = Selector(response)
        # 匹配商品分类链接
        goods_type_links = rel.xpath('//div[@class="aside-nav"]//li/a/@href').extract()
        if len(goods_type_links) > 0:
            # 通过list、filter、startswith等函数过滤筛选所需的商品类别链接
            goods_type_list = list(filter(net_empty, [ch if ch.startswith('//channel.fenqile.com/') else '' for ch in goods_type_links]))
            for ch in goods_type_list:
                yield Request(url='http:' + ch, callback=self.get_min_type_link)

    # parse回调函数
    def get_min_type_link(self, response):
        rel = Selector(response)
        # 匹配小分类的链接
        goods_min_type_link = rel.xpath(
            '//div[@class="aside-nav-body"]//div[@class="channel-li-text"]//a/@href').extract()
        if len(goods_min_type_link) > 0:
            # 通过list、filter、startswith等函数过滤筛选所需的商品类别链接
            goods_type_list = list(filter(net_empty, [ch if ch.startswith('http://www.fenqile.com/') else '' for ch in goods_min_type_link]))
            for ch in goods_type_list:
                yield Request(url=ch, callback=self.git_detail_text)

    def git_detail_text(self, response):
        # 匹配商品详情页链接
        rel = Selector(response)
        goods_detall_link = rel.xpath('//ul[@class="list-li fn-clear js-noraml-li"]//li//a/@href').extract()
        if len(goods_detall_link) > 0:
            goods_detall_links = list(filter(net_empty, [ch if ch.startswith('//item.fenqile.com/') else '' for ch in goods_detall_link]))

            # 实例化item对象
            item = FenqiItem()

            for ch in goods_detall_links:
                item['url'] = 'http:' + ch
                yield item

    # 爬虫发送spider_closed信号关闭浏览器
    def closeSpider(self, spider):
        self.driver.close()
