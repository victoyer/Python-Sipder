# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SionItem(scrapy.Item):
    # 数据库存储表名
    collections = 'user_infos'
    # 博主用户ID
    id = scrapy.Field()
    # 博主名称
    screen_name = scrapy.Field()
    # 微博背景
    profile_image_url = scrapy.Field()
    # 博主认证
    verified_reason = scrapy.Field()
    # 博主描述
    description = scrapy.Field()
    # 博主头像
    avatar_hd = scrapy.Field()
    # 创建时间
    crate_time = scrapy.Field()
    # 博主关注数量
    follows = scrapy.Field()
    # 博主粉丝数量
    fans = scrapy.Field()
