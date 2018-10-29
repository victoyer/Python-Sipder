# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider9KyyItem(scrapy.Item):
    title = scrapy.Field()
    types = scrapy.Field()
    description = scrapy.Field()
    path = scrapy.Field()
