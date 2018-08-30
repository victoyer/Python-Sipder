# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FenqiItem(scrapy.Item):
    # 商品详情页链接
    url = scrapy.Field()
