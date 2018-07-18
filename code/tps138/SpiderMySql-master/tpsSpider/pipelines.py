# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.conf import settings


class TpsspiderPipeline(object):
    def __init__(self):
        # 链接redis
        self.redis = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db = 0)

    def process_item(self, item, spider):
        # 存入数据到redis
        self.redis.lpush('tps:start_urls', item['url'])
        self.redis.lpush('tps_flag', item['flag'])

        return item
