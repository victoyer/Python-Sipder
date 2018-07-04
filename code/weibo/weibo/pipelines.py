# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from datetime import datetime

from weibo.items import WeiboItem, UserRelationItem


class Create_time(object):
    def process_item(self, item, spider):
        # 获取当前时间并写入数据库初始化字段
        if isinstance(item, WeiboItem):
            item['create_time'] = datetime.now().strftime('%Y-%m-%d')
        # 丢弃已保存数据
        return item


class WeiboPipeline(object):

    def __init__(self):
        # 初始化方法建立数据库连接
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[WeiboItem.collection]

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            # 有数据就更新数据库内的内容，没有数据就填充
            self.collection.update({'id': item['id']}, {'$set': item}, True)
        if isinstance(item, UserRelationItem):
            self.collection.update(
                {'id': item['id']},
                {'$addToSet': {
                    'fans': {'$each': item['fans']},
                    'follows': {'$each': item['follows']}
                }
                }
            )

            # 丢弃已保存数据避免重复操作
        return item
