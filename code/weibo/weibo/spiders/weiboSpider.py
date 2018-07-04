# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class WeibospiderSpider(scrapy.Spider):
    name = 'weiboSpider'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/']

    def parse(self, response):
        # print(response.body)
        res = Selector(response)
        if not res.xpath('//*[@id="Pl_Core_F4RightUserList__4"]/div/div/div/div/div[1]/ul').extract():
            tag_links = res.xpath('//*[@id="pl_unlogin_home_hotpersoncategory"]/div//li/a[@class="S_txt1"]/@href').extract()
            print(tag_links)
