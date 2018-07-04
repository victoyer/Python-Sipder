# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencnetItem(scrapy.Item):
    # 职位名称
    jobname = scrapy.Field()
    # 职位类别
    jobtype = scrapy.Field()
    # 招聘人数
    peoplenum = scrapy.Field()
    # 工作地点
    workadder = scrapy.Field()
    # 发布时间
    publishtime = scrapy.Field()
