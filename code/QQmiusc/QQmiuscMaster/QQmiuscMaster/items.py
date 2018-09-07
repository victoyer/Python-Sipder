# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqmiuscmasterItem(scrapy.Item):
    # 歌曲ID
    songid = scrapy.Field()
    # 歌曲名称
    songname = scrapy.Field()
    # 歌曲所属专辑
    songorig = scrapy.Field()
    # 歌曲所属分类ID
    top_id = scrapy.Field()
