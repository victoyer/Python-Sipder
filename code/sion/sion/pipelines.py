# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from datetime import datetime

from sion.items import SionItem


class Create_time(object):
    # 创建时间
    def process_item(self, itme, spider):
        itme['crate_time'] = datetime.now().strftime('%Y-%m-%d')

        return itme


# 插入数据
class SionPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[SionItem.collections]

    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        # 去重插入
        self.collection.update({'id': item['id']}, {'$set': item}, True)

        return item
