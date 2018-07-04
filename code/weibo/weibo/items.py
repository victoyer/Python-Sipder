# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # 博主ID
    id = scrapy.Field()
    # 博主名称
    screen_name = scrapy.Field()
    # 关注微博数量
    follow_count = scrapy.Field()
    # 微博认证内容
    verified_reason = scrapy.Field()
    # 博主自我描述
    description = scrapy.Field()
    # 博主粉丝数量
    followers_count = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()

    # 储存数据的表名
    collection = 'user_infos'


class UserRelationItem(scrapy.Item):
    # 储存数据的表名
    collection = 'user_infos'
    # 博主ID
    id = scrapy.Field()
    # 博主关注
    follows = scrapy.Field()
    # 博主粉丝
    fans = scrapy.Field()

