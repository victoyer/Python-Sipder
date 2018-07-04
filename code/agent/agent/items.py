# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AgentItem(scrapy.Item):
    collection = 'proxy_ip_ware'
    ip = scrapy.Field()
    port = scrapy.Field()
    agent = scrapy.Field()
