# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetTypeIdItem(scrapy.Item):
    # 商品类别ID
    typeID = scrapy.Field()
    # 商品类别名称
    typeName = scrapy.Field()


class EanissspiderItem(scrapy.Item):
    # 商品名称
    g_name = scrapy.Field()
    # 商品价格
    g_price = scrapy.Field()
    # 点击次数
    g_click = scrapy.Field()
    # 商品图片
    g_img = scrapy.Field()
    # 商品库存
    g_number = scrapy.Field()
    # 商品描述
    g_content = scrapy.Field()
    # 商品类别
    g_type = scrapy.Field()
