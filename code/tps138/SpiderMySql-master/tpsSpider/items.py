# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TpsspiderItem(scrapy.Item):
    # 链接
    url = scrapy.Field()
    # 类别
    flag = scrapy.Field()


