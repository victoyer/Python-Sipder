# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings
from datetime import datetime

from Spider_slave.items import SpiderSlaveItem


class create_time(object):
    def __init__(self):
        self.create = datetime.now()

    def process_item(self, item, spider):
        item['create_time'] = self.create.strftime('%Y-%m-%d')

        return item


class SpiderSlavePipeline(object):
    def __init__(self):

        self.mysql = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=SpiderSlaveItem.collcetion,
            user='root',
            passwd='victor',
            charset='utf8'
        )

    def process_item(self, item, spider):
        try:
            # 获取游标
            cur = self.mysql.cursor()

            # sql语句
            sql = 'insert into goodsinfos (s_name, s_no, s_number, s_price, s_imgPath, s_type, s_time) value (%s,%s,%s,%s,%s,%s,%s)'
            # 写入数据库参数
            params = (
                item['goods_title'],
                item['goods_code'],
                item['goods_price'],
                item['goods_stock'],
                item['goods_image'],
                item['goods_type'],
                item['create_time']
            )
            # 插入数据
            cur.execute(sql, params)

            # 提交sql事务
            self.mysql.commit()

            # 关闭本次操作
            cur.close()

            return item

        except Exception as e:

            print(e)
