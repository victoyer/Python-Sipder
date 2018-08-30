# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class FenqiSlavePipeline(object):
    # 初始化数据库
    def __init__(self):
        self.mysql = pymysql.connect(host='127.0.0.1',
                                     port=3306,
                                     user='root',
                                     password='victor',
                                     db='bs',
                                     charset='utf8')

    def process_item(self, item, spider):
        # 获取数据库操作游标
        cur = self.mysql.cursor()
        # 定义sql插入数据语句
        sql = 'insert into goods (goods_name, goods_price, goods_cprice, goods_sales, goods_img, goods_stock, goods_click, goods_type, goods_desc) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # 获取对应参数值
        params = [
            item['goods_name'],
            item['goods_price'],
            item['goods_cprice'],
            item['goods_sales'],
            item['goods_img'][0],
            item['goods_stock'],
            item['goods_click'],
            item['goods_type'],
            item['goods_desc']
        ]

        # 执行sql语句
        cur.execute(sql, params)
        # 提交sql事务
        self.mysql.commit()
        # 关闭本次操作
        cur.close()

        return item
