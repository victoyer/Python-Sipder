# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # 房源信息存储表
    collection = 'house_info'
    # 房源ID
    id = scrapy.Field()
    # 房源名称
    title = scrapy.Field()
    # 房源地址
    add = scrapy.Field()
    # 房源信息
    info = scrapy.Field()
    # 房源位置
    floor = scrapy.Field()
    # 房源标签
    tag = scrapy.Field()
    # 房源总价
    total = scrapy.Field()
    # 房源单价
    price = scrapy.Field()
    # 房源区域
    area = scrapy.Field()
