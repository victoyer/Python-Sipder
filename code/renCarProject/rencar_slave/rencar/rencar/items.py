# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RencarItem(scrapy.Item):
    # 车辆名称
    title = scrapy.Field()
    # 车辆价格
    price = scrapy.Field()
    # 分期信息
    stages = scrapy.Field()
    # 服务费
    charge = scrapy.Field()
    # 上牌时间
    carNumTime = scrapy.Field()
    # 行驶公里
    travelMeile = scrapy.Field()
    # 外迁
    migretion = scrapy.Field()
    # 车辆排量
    displacement = scrapy.Field()
    # 上牌城市
    oncarcity = scrapy.Field()
    # 车辆图片
    carImgLink = scrapy.Field()
    # 车辆ID
    id = scrapy.Field()
    # 首付
    first_price = scrapy.Field()
    # 分期金额
    evety_price = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 储存表名
    collcetion = 'CarInfos'
