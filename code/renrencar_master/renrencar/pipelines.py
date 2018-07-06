# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from redis import Redis


class RenrencarPipeline(object):
    def __init__(self):
        # 连接redis
        self._redis_db = Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])

    def process_item(self, item, spider):
        # 存链接入redis
        self._redis_db.lpush('rencar:start_urls', item['url'])
