# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.conf import settings
from redis import Redis


class MasterPipeline(object):

    def __init__(self):
        # 链接redis
        self.redis_db = Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])

    def process_item(self, item, spider):
        # 把要爬取的链接存入redis
        self.redis_db.lpush('lianjia:start_urls', item['url'])
        self.redis_db.lpush('lianjia:name', item['name'])
