# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD = 'victor'
DB = 'img'
CHARSET = 'utf8'

import pymysql


class GifslavePipeline(object):
    def __init__(self):
        self.mysqlClient = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)

    def process_item(self, item, spider):
        cur = self.mysqlClient.cursor()
        sql = "insert into img_info (imgName, imgDir, imgUrl)values(%s, %s, %s)"
        params = [item["imgName"], item["imgDir"], item["imgUrl"]]
        try:
            cur.execute(sql, params)
            self.mysqlClient.commit()
            cur.close()
        except Exception as e:
            self.mysqlClient.rollback()
            print(e)

        return item

    # def close_spider(self, spider):
    #     pass
