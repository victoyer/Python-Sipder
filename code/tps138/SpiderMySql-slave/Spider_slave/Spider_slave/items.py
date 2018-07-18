# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderSlaveItem(scrapy.Item):
    # 商品名称
    goods_title = scrapy.Field()
    # 商品编号
    goods_code = scrapy.Field()
    # 商品价格
    goods_price = scrapy.Field()
    # 商品库存
    goods_stock = scrapy.Field()
    # 商品图片
    goods_image = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 商品类别
    goods_type = scrapy.Field()

    # 数据库名
    collcetion = 'flask'
