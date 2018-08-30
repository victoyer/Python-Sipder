# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from redis import Redis


class MasterPipeline(object):
    """
    定义一个储存商品详情页链接的中间件
    """

    def __init__(self):
        # 链接redis
        self.redis = Redis(host='127.0.0.1', port=6379)

    # 重写process_item方法
    def process_item(self, item, spider):
        # 向redis中写入需要爬取的商品详情页链接
        self.redis.lpush('fenqi:start_urls', item['url'])

        # 丢弃已赋值的item
        return item
