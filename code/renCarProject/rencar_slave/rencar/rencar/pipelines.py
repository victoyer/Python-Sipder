# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from datetime import datetime

from rencar.items import RencarItem


class CreateTime(object):
    def process_item(self, item, spider):
        self.datetime = datetime.now().strftime('%Y-%m-%d')
        item['create_time'] = self.datetime

        return item


class RencarPipeline(object):

    def __init__(self):
        # 连接MONGODB数据库
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[RencarItem.collcetion]

    def process_item(self, item, spider):
        # 去重插入
        if isinstance(item, RencarItem):
            self.collection.update({'id': item['id']}, {'$set': item}, True)

        return item
