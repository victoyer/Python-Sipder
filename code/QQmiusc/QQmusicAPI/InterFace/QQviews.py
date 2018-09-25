from flask import Blueprint, jsonify
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

from utils.BD_con import DB_URL

# 创建蓝图
dataAPI = Blueprint('dataAPI', __name__)

# 创建数据连接
engine = create_engine(DB_URL)

# 创建基类
Base = declarative_base()

# 绑定数据库数据接口
metadata = MetaData(bind=engine)

# 创建事务
db_session = create_session(bind=engine)


# 序列化函数
def func_Serialization(datas):
    data = []
    if datas.count() > 0:
        for ch in datas:
            dict_data = {
                'top_id': ch.topID,
                'song_id': ch.songid,
                'songname': ch.songname,
                'songorig': ch.songorig,
                'singerid': ch.singerid,
                'singermid': ch.singermid,
                'singername': ch.singername,
                'ListName': ch.ListName,
                'ListImgs': ch.ListImgs,
                'SongTime': ch.SongTime,
                'songmid': ch.songmid
            }

            data.append(dict_data)

        return jsonify({'code': 200, 'data': data})

    else:
        return jsonify({'code': 0, 'msg': "数据异常请稍后重试"})


# 映射已有的数据库
class QQdb(Base):
    __table__ = Table("SongInfo", metadata, autoload=True)


@dataAPI.route('/<string:top_id>/<string:num>', methods=['GET'])
def data(top_id, num):
    if top_id in ['4', '26', '27', '54', '55', '56', '28', '5', '6', '3', '16', '29', '17', '52', '36', '108',
                  '123', '106', '107', '105', '113', '114']:
        top_all_datas = []
        if num == '0':
            top_all_datas = db_session.query(QQdb).filter_by(topID=top_id)

        else:
            top_all_datas = db_session.query(QQdb).filter_by(topID=top_id).order_by(QQdb.id.desc()).slice(0, int(num))

        return func_Serialization(top_all_datas)
    else:
        return jsonify({'code': 700, 'msg': '请检查传入参数是否正确'})


# 这个是demo，建立一个songType表来读表操作
@dataAPI.route('/', methods=['GET'])
def type():
    types = [
            {"code": 4, "id": 10100108, "name": "流行音乐"},
            {"code": 54, "id": 10100110, "name": "明日之子"}
        ]

    return jsonify({"code": 200, "data": types})
