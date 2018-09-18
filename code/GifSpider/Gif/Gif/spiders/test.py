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


def main():
    redisClient = StrictRedis(host=HOST, port=PORT, db=DB)
    mysqlClient = pymysql.connect(host=mHOST, port=mPORT, user=mUSER, passwd=mPASSWD, db=mDB, charset=mCHARSET)

    while True:
        item = eval(redisClient.srandmember('img_data').decode('utf-8') if redisClient.srandmember('img_data') else '0')
        # item = eval(self.redisClient.spop('img_data').decode('utf-8') if self.redisClient.spop('img_data') else '0')
        # 判断跳出
        if item == "0":
            break
        cur = mysqlClient.cursor()
        sql = "insert into img_data (url, sid, size, width, title, height, subText)values(%s,%s,%s,%s,%s,%s,%s)"
        params = [
            item["url"],
            item["sid"],
            item["size"],
            item["width"],
            item["title"],
            item["height"],
            item["subText"],
        ]
        try:
            cur.execute(sql, params)
            mysqlClient.commit()
            cur.close()
        except Exception as e:
            mysqlClient.rollback()
            print(e)


if __name__ == '__main__':
    main()
