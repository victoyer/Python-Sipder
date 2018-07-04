# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouBanspiderItem(scrapy.Item):
    name = scrapy.Field()
    avator = scrapy.Field()
    directors = scrapy.Field()
    year = scrapy.Field()
    guojia = scrapy.Field()
    classfication = scrapy.Field()
    score = scrapy.Field()
