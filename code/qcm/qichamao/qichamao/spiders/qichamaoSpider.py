from scrapy import Spider, Selector, Request
import re, random
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from qichamao.settings import CookieList


def randCookie():
    items = []
    for ch in CookieList:
        dicts = {}
        for sh in str(ch).split(";"):
            dicts[str(sh.split("=")[0]).strip()] = str(sh.split("=")[1]).strip()
            items.append(dicts)
    return random.choice(items)


randCookie()


class qcmSpider(Spider):
    name = "qcm"
    # allowed_domains = ["https://www.qichamao.com"]
    start_urls = ["https://www.qichamao.com/"]
    url = "https://www.qichamao.com"

    def __init__(self):
        super(qcmSpider, self).__init__()
        dispatcher.connect(self.closeSpider, signals.spider_closed)
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url="https://www.qichamao.com/")
        self.driver.add_cookie(cookie_dict={"name": "qz.newsite", "value": randCookie()["qz.newsite"]})

    def closeSpider(self, spider):
        self.driver.close()

    def parse(self, response):
        TypeLink = set(
            Selector(response).xpath('//div[@class="areaquick"]//div[@class="areaquick_con"]//a/@href').extract())
        for ch in TypeLink:
            yield Request(url=self.url + str(ch), callback=self.getPageNum)

    def getPageNum(self, response):
        if Selector(response).xpath('//span[@class="goto"]//input[@id="txtpagegoto"]/@data-max').extract():
            for ch in range(1, int(Selector(response).xpath('//span[@class="goto"]//input[@id="txtpagegoto"]/@data-max').extract()[0])):
                yield Request(url=str(response.url) + "&p={page}".format(page=ch), callback=self.getDetailLink)

    def getDetailLink(self, response):
        if response.url.startswith("https://www.qichamao.com/search/"):
            detailLink = [str(ch).startswith('/orgcompany/') for ch in Selector(response).xpath('//ul[@id="listsec"]//div//a/@href').extract()]
            pass
        else:
            print(response.url)
