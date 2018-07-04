# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

from agent.items import AgentItem
import json


class AgentPipeline(object):
    def __init__(self):
        # conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        # db = conn[settings['MONGODB_DB']]
        # self.collection = db[AgentItem.collection]

        self.filname = open('IP.json', 'wb')

    def process_item(self, item, spider):
        # if isinstance(item, AgentItem):
        context = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filname.write(context)
            # self.collection.update({'ip': item['ip']}, {'$set': item}, True)

        return item

    def close_spider(self, spider):
        self.filname.close()
