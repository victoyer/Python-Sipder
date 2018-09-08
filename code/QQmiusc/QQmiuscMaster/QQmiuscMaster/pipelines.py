# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from redis import Redis
import pymysql


class QqmiuscmasterPipeline(object):
    def __init__(self):
        # self.redis = Redis(host='127.0.0.1', port=6379, db=0)
        self.mysqlClient = pymysql.connect(host='127.0.0.1',
                                           port=3306,
                                           user='root',
                                           passwd='victor',
                                           db='QQ',
                                           charset='utf8')

    def process_item(self, item, spider):
        # self.redis.lpush('url', item['url'])
        # 获取数据库操作游标
        cur = self.mysqlClient.cursor()
        # 定义sql语句
        sql = "insert ignore into SongInfo(songid, songname, songorig, topID) values (%s, %s, %s, %s)"
        # 插入数据库数据
        params = [
            item['songid'],
            item['songname'],
            item['songorig'],
            item['top_id']
        ]
        # 执行SQL语句
        cur.execute(sql, params)
        # 提交事物
        self.mysqlClient.commit()
        # 关闭游标
        cur.close()
        # 抛出已处理数据
        return item

    # def closed_spider(self):
    #     pass
#
# from redis import StrictRedis, Redis
#
#
# class QqmiuscmasterPipeline(object):
#     # 初始化redis
#     def __init__(self):
#         self.host = '127.0.0.1'
#         self.port = '6379'
#         self.db = 0
#         self.redisClient = StrictRedis(host=self.host, port=self.port, db=self.db)
#
#     def process_item(self, item, spider):
#         self.redisClient.sadd('items', dict(item))
#
#     # def close_spider(self, spider):
#     #     pass
