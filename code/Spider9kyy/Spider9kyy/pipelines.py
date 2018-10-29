# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class Spider9KyyPipeline(object):
    def __init__(self):
        self.mysql = pymysql.connect(host='127.0.0.1',
                                     port=3306,
                                     user='root',
                                     passwd='conal',
                                     db='normaldb',
                                     charset='utf8'
                                     )
        # 数据库操作游标
        self.cur = self.mysql.cursor()

    def process_item(self, item, spider):
        sql = "insert into film (title, types, description, path) values (%s,%s,%s,%s)"
        params = [
            item['title'],
            item['types'],
            item['description'],
            item['path']
        ]
        self.cur.execute(sql, params)
        try:
            self.mysql.commit()
        except Exception as e:
            self.mysql.rollback()
            print(e)
        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cur.close()
        # 关闭数据库
        self.mysql.close()
