# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

from eanissSpider.items import GetTypeIdItem, EanissspiderItem


def ConnectMySqlDB():
    mysqlCli = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='victor',
        db='flask',
        charset='utf8'
    )
    return mysqlCli


class GetTypeIdPipline(object):
    def process_item(self, item, spider):
        # 获取游标和数据库对象
        mysqlCli = ConnectMySqlDB()
        cur = mysqlCli.cursor()

        # 判断模型
        if isinstance(item, GetTypeIdItem):
            # SQL语句
            sql = 'insert into typeModels (t_id, t_type) values (%s, %s)'
            # 传入参数
            params = (
                item['typeID'],
                item['typeName']
            )
            try:
                # 使用execute方法执行SQL INSERT语句
                cur.execute(sql, params)
                # 提交事务
                mysqlCli.commit()
                # 关闭操作
                cur.close()
            except Exception as e:
                print(e)
            return item

        elif isinstance(item, EanissspiderItem):
            # sql语句
            sql = 'insert into goodsModels (g_name, g_price, g_click, g_img, g_number, g_type, g_content) values (%s,%s,%s,%s,%s,%s,%s)'
            # 传入参数
            params = (
                item['g_name'],
                item['g_price'],
                item['g_click'],
                item['g_img'],
                item['g_number'],
                item['g_type'],
                item['g_content']
            )
            try:
                # 使用execute方法执行SQL INSERT语句
                cur.execute(sql, params)
                # 提交事务
                mysqlCli.commit()
                # 关闭操作
                cur.close()
            except Exception as e:
                print(e)

            return item

# class EanissspiderPipeline(object):
#     def process_item(self, item, spider):
#         # 获取游标和数据库对象
#         mysqlCli = ConnectMySqlDB()
#         cur = mysqlCli.cursor()
#         # sql语句
#         sql = 'insert into goods_models (g_name, g_price, g_click, g_img, g_number, g_type, g_content, g_type) values (%s,%s,%s,%s,%s,%s,%s,0)'
#         # 传入参数
#         params = (
#             item['g_name'],
#             item['g_price'],
#             item['g_click'],
#             item['g_img'],
#             item['g_number'],
#             item['g_type'],
#             item['g_content']
#         )
#         try:
#             # 使用execute方法执行SQL INSERT语句
#             cur.execute(sql, params)
#             # 提交事务
#             mysqlCli.commit()
#             # 关闭操作
#             cur.close()
#         except Exception as e:
#             print(e)
#
#         return item
