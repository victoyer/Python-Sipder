from redis import StrictRedis
from pymysql import connect

Rhost = '127.0.0.1'
Rport = 6379
Rdb = 0

#########################

Mhost = '127.0.0.1'
Mport = 3306
Muser = 'root'
Mpasswd = 'victor'
Mcharset = 'utf8'
Mdb = 'QQ'


def main():
    # 初始化redis数据库链接
    redis_client = StrictRedis(host=Rhost, port=Rport, db=Rdb)

    # 初始化MySQL数据库链接
    mysql_client = connect(host=Mhost,
                           port=Mport,
                           db=Mdb,
                           user=Muser,
                           passwd=Mpasswd,
                           charset=Mcharset)

    while True:
        item = eval(redis_client.spop('items').decode('utf-8') if redis_client.spop('items') else '0')
        # 判断跳出
        if item == 0:
            break

        try:
            # 获取MySQL操作游标
            cur = mysql_client.cursor()
            # 定义插入的sql语句
            sql = "insert into SongInfo(songid, songname, songorig, topID) values (%s, %s, %s, %s)"
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
            mysql_client.commit()
            # 关闭游标
            cur.close()
            # 打印过程
            print('插入数据{data}成功'.format(data=item))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
