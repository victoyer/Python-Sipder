import scrapy, json
from scrapy import Request
from jsonpath import jsonpath

from weibo.items import WeiboItem, UserRelationItem


class SionSpider(scrapy.Spider):
    # 爬虫名称
    name = 'sion'
    # 用户信息待爬取链接
    user_info_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid=100505{uid}'
    # 用户关注
    user_followers_info = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 用户粉丝
    user_fans_info = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'

    # 博主用户ID
    user_ID = [
        # '2970452952',
        # '6162866961',
        # '1669879400',
        # '5950061090',
        # '1778742953',
        '1270344441'
    ]

    # 起始调用URL函数
    def start_requests(self):
        # 组装URL并发送请求
        for uid in self.user_ID:
            # 填接链接中{uid},并调用回调函数
            yield Request(self.user_info_url.format(uid=uid), callback=self.parse_user)

    # 处理请求结果的回调函数
    def parse_user(self, response):
        # print(response)
        # 转换获取数据格式
        json_infos = json.loads(response.text)

        # 判断是否获取到数据
        if json_infos.get('ok'):
            # 已有数据获取data
            user_data = json_infos.get('data').get('userInfo')
            # 数据库储存模型实例化
            db_models = WeiboItem()
            # 储存指定字段数据
            sortage_lsit = ['id', 'screen_name', 'follow_count', 'verified_reason', 'description', 'followers_count']
            for sortage_one in sortage_lsit:
                # 可能字段不会有数据所以建议使用get获取数据
                db_models[sortage_one] = user_data.get(sortage_one)
                # 返回储存数据的itmes
                yield db_models

            # 根据当前博主ID去获取他的关注信息
            # 并且把当前博主的uid和关注页数传参
            uid = db_models['id']
            yield Request(self.user_followers_info.format(uid=uid, page=1), callback=self.parse_followers,
                          meta={'uid': uid, 'page': 1})

            # 根据当前博主ID获取他的粉丝信息
            yield Request(self.user_fans_info.format(uid=uid, page=1), callback=self.parse_fans,
                          meta={'uid': uid, 'page': 1})

    def parse_fans(self, response):
        # 解析当前博主粉丝信息
        # 转换获取到的数据格式
        res = json.loads(response.text)
        # 判断是否获取到数据
        if res['ok']:
            # jsonpath获取当前博主粉丝用户信息
            user_info = jsonpath(res, '$..user')[0]
            # 获取当前粉丝的uid
            uid = user_info['id']
            # 回调获取用户信息的函数获取当前uid对应用户信息
            yield Request(self.user_info_url.format(uid=uid), callback=self.parse_user)

            # 获取当前粉丝关注的博主的uid
            uid = response.meta.get('uid')
            # 实例化数据库模型
            item = UserRelationItem()
            # 数据库字段赋值
            item['follows'] = []
            item['fans'] = [{'id': user_info['id'], 'name': user_info['screen_name']}]
            item['id'] = uid

            # 返回赋值字段
            yield item

            # 获取下一页粉丝信息
            page = response.meta.get('page') + 1
            # 回调获取粉丝信息的函数
            yield Request(self.user_fans_info.format(uid=uid, page=page), callback=self.parse_fans,
                          meta={'uid': uid, 'page': page})

    def parse_followers(self, response):
        # 解析当前博主关注信息
        # 转换获取到的数据
        res = json.loads(response.text)
        # 判断是否获取到数据
        if res['ok']:
            # 用jsonpath获取当前博主关注的用户信息
            user_info = jsonpath(res, '$..user')[0]
            # 当前博主关注的用户uid
            uid = user_info['id']
            # 回调获取用户详细信息的函数
            yield Request(self.user_info_url.format(uid=uid), callback=self.parse_user)

            # 被当前函数获取关注信息的博主uid
            uid = response.meta.get('uid')
            # 实例化数据库模型
            item = UserRelationItem()
            # 数据库字段赋值
            item['follows'] = [{'id': user_info.get('id'), 'name': user_info.get('screen_name')}]
            item['id'] = uid
            item['fans'] = []
            # 返回已赋值数据库模型字段
            yield item

            # 获取下一页关注信息
            page = int(response.meta.get('page')) + 1
            # 回调获取关注信息的函数
            yield Request(self.user_followers_info.format(uid=uid, page=page), callback=self.parse_followers,
                          meta={'uid': uid, 'page': page})
