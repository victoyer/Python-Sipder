import scrapy
from sion.items import SionItem
import json, math
from jsonpath import jsonpath
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Spider
from scrapy import Request


class sionSpider(Spider):
    name = 'weibo'
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    uid_list = [
        '6162866961',
        '2970452952',
        '1669879400',
        '5950061090',
        '1778742953',
        '1270344441'
    ]

    def start_requests(self):
        # 组装URL
        for uid in self.uid_list:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    # 解析用户信息
    def parse_user(self, response):

        # 初始化模型对象
        item = SionItem()
        # 获取返回json
        mydict_info = response.body.decode('utf-8')
        # 转成dict
        myjson_info = json.loads(mydict_info)

        # 判断请求成功与否
        if jsonpath(myjson_info, '$..ok'):
            # 获取json用户信息
            userinfos = jsonpath(myjson_info, '$..userInfo')[0]

            # 定义一个列表储存要获取的字段
            get_list = ['screen_name', 'profile_image_url', 'verified_reason', 'description', 'avatar_hd']
            # 字段赋值
            for ch in get_list:
                item[ch] = userinfos[ch]
            # 返回获值字段
            yield item

            # 当前博主uid
            uid = userinfos['id']
            # 应用parse_follow函数获取当前博主的关注列表
            yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follow,
                          meta={'uid': uid, 'page': 1})

    # 解析博主关注JSON
    def parse_follow(self, response):
        # 转换response为JSON格式数据
        myJsonInfo = json.loads(response.body.decode('utf-8'))
        # jsonpath获取用户信息
        json_data = jsonpath(myJsonInfo, '$..user')[0]
        # 判断当前信息是否为空
        if json_data['id']:
            # 获取当前被关注的博主uid
            uid = json_data['id']
            # 应用parse_user函数获取被关注博主的详情信息
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
        # 被解析关注列表的用户uid
        uid = response.meta.get('uid')
        # 模型实例
        user_item = SionItem()
        # 赋值字段
        user_item['follows'] = [{'id': json_data['id'], 'name': json_data['screen_name']}]
        user_item['id'] = uid
        user_item['fans'] = []
        # 返回字段
        yield user_item

        # 解析下一页关注
        page = response.meta.get('page') + 1
        yield Request(self.follow_url.format(uid=uid, page=page), callback=self.parse_follow,
                      meta={'uid': uid, 'page': page})
