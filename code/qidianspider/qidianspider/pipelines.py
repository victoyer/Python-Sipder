# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class DouBanspiderPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for ch in range(len(item['name'])):
            data = {}
            data['name'] = item['name'][ch]
            data['avator'] = item['avator'][ch]
            data['directors'] = item['directors'][ch]
            data['year'] = item['year']
            data['guojia'] = item['guojia']
            data['classfication'] = item['classfication']
            data['score'] = item['score'][ch]
            # print(data)
            self.collection.insert(data)
        return item
