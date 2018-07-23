# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from redis import Redis


class PddspiderPipeline(object):
    def __init__(self):
        # 连接redis数据库
        self.redis = Redis(host='127.0.0.1', port=6379, db=0)

    def process_item(self, item, spider):
        # 将数据写入数据库
        self.redis.lpush('pdd:start_urls', item['detail_link'])
        self.redis.lpush('pdd:meta_params', item['meta_params'])

        return item
