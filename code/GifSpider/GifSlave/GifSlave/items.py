# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GifslaveItem(scrapy.Item):
    # 图片名称
    imgName = scrapy.Field()
    # 图片路径
    imgDir = scrapy.Field()
    # 图片链接
    imgUrl = scrapy.Field()
