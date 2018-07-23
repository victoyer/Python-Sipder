# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PddspiderItem(scrapy.Item):
    # 商品名称
    goods_name = scrapy.Field()
    # 商品价格
    goods_price = scrapy.Field()
    # 商品图片
    goods_imgs = scrapy.Field()
    # 商品库存
    goods_stock = scrapy.Field()
    # 商品详情
    goods_detail = scrapy.Field()
    # 商品所属大类
    goods_maxType = scrapy.Field()
    # 商品所属小类
    goods_minType = scrapy.Field()
    # 商品ID
    goods_ID = scrapy.Field()
