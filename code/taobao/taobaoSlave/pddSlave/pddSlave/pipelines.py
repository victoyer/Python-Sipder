# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from pddSlave.items import PddspiderItem


class PddslavePipeline(object):
    def __init__(self):
        # 链接mongodb数据库
        mongodbCli = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = mongodbCli['taobao']
        self.collection = db['taobao_goods_data']

    def process_item(self, item, spider):
        if isinstance(item, PddspiderItem):
            # 写入数据库
            self.collection.update({'goods_ID': item['goods_ID']}, {'$set': item}, True)

        return item
