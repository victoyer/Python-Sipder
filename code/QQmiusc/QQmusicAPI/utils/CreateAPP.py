from flask import Flask
from InterFace.QQviews import dataAPI


def create_app():
    # 初始化API实例
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=dataAPI, url_prefix='/data')

    return app
