# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PddspiderItem(scrapy.Item):
    # 详情页链接
    detail_link = scrapy.Field()
    # 对应链接的大小类名
    meta_params = scrapy.Field()

    # # 商品名称
    # goods_name = scrapy.Field()
    # # 商品价格
    # goods_price = scrapy.Field()
    # # 商品图片
    # goods_imgs = scrapy.Field()
    # # 商品库存
    # goods_stock = scrapy.Field()
    # # 商品详情
    # goods_detail = scrapy.Field()
