# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FenqiSlaveItem(scrapy.Item):
    # 商品名称
    goods_name = scrapy.Field()
    # 商品现价
    goods_price = scrapy.Field()
    # 商品图片
    goods_img = scrapy.Field()
    # 商品类别
    goods_type = scrapy.Field()
    # 商品描述
    goods_desc = scrapy.Field()
    # 商品原价
    goods_cprice = scrapy.Field()
    # 商品销量
    goods_sales = scrapy.Field()
    # 商品库存
    goods_stock = scrapy.Field()
    # 商品点击次数
    goods_click = scrapy.Field()
