# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GifItemInfo(scrapy.Item):
    # 图片路径
    url = scrapy.Field()
    # 图片sid
    sid = scrapy.Field()
    # 图片大小
    size = scrapy.Field()
    # 图片宽度
    width = scrapy.Field()
    # 图片标题
    title = scrapy.Field()
    # 图片高度
    height = scrapy.Field()
    # 图片描述
    subText = scrapy.Field()

#
# class GifItemUrl(scrapy.Item):
#     # 下载图片链接
#     downLink = scrapy.Field()
