# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from redis import StrictRedis
import pymysql

HOST = '127.0.0.1'
PORT = 6379
DB = 0

##################

mHOST = '127.0.0.1'
mPORT = 3306
mUSER = 'root'
mPASSWD = 'victor'
mDB = 'img'
mCHARSET = 'utf8'


class GifPipeline(object):

    def __init__(self):
        self.redisClient = StrictRedis(host=HOST, port=PORT, db=DB)
        self.mysqlClient = pymysql.connect(host=mHOST, port=mPORT, user=mUSER, passwd=mPASSWD, db=mDB, charset=mCHARSET)

    def process_item(self, item, spider):
        self.redisClient.sadd("img_data", dict(item))
        self.redisClient.sadd("img_url", dict(item)["url"])
        return item

    def close_spider(self, spider):
        # while True:
        #     # item = eval(self.redisClient.SMEMBERS('img_data').decode('utf-8') if self.redisClient.SMEMBERS('img_data') else '0')
        #     item = eval(self.redisClient.spop('img_data').decode('utf-8') if self.redisClient.spop('img_data') else '0')
        #     # 判断跳出
        #     if item == "0":
        #         break
        #     cur = self.mysqlClient.cursor()
        #     sql = "insert into img_data (url, sid, size, width, title, height, subText)values(%s,%s,%s,%s,%s,%s,%s)"
        #     params = [
        #         item["url"],
        #         item["sid"],
        #         item["size"],
        #         item["width"],
        #         item["title"],
        #         item["height"],
        #         item["subText"],
        #     ]
        #     try:
        #         cur.execute(sql, params)
        #         self.mysqlClient.commit()
        #         cur.close()
        #         print("插入{data}成功".format(data=item))
        #     except Exception as e:
        #         self.mysqlClient.rollback()
        #         print(e)
        # 取出Redis数据库中的全部数据 smembers
        item = self.redisClient.smembers('items') if self.redisClient.smembers('items') else '0'
        for ch in item:
            cur = self.mysqlClient.cursor()
            # sql = "insert into SongInfo (singerid, singermid, singername, songid, songmid, songname, songorig, topID) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            sql = "insert into SongInfo (singerid, singermid, singername, songid, songmid, songname, songorig, topID)values(%s,%s,%s,%s,%s,%s,%s,%s)"
            # 处理数据格式
            item = eval(ch.decode("utf-8"))
            parms = [
                str(item["singerid"]),
                str(item["singermid"]),
                str(item["singername"]),
                str(item["songid"]),
                str(item["songmid"]),
                str(item["songname"]),
                str(item["songorig"]),
                str(item["topID"]),
            ]
            try:
                cur.execute(sql, parms)
                self.mysqlClient.commit()
                cur.close()
                print("插入数据{data}成功".format(data=parms))
            except Exception as e:
                self.mysqlClient.rollback()
                print(e)
