from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jsonpath import jsonpath
import json
from QQmiuscMaster.items import QqmiuscmasterItem


# 返回短的时间参数
def shortTime():
    year = ['2016', '2017', '2018']
    days = [str(ch) for ch in range(1, 53)]
    for ch in year:
        for sh in days:
            yield '_'.join((ch, sh.zfill(2)))


# 返回长的时间参数
def longTime():
    year = ['2014', '2015', '2016', '2017', '2018']
    month = [str(ch) for ch in range(1, 13)]
    days = [str(ch) for ch in range(1, 31)]
    for ch in year:
        for sh in month:
            for zh in days:
                yield '-'.join((ch, sh.zfill(2), zh.zfill(2)))


# 全球榜时间参数构建函数
def globalTimeFunc(max_time: str):
    longTime = max_time.split('_')
    year = [str(ch) for ch in range(2012, int(longTime[0]))]
    days = [str(ch) for ch in range(1, 54)]
    for ch in year:
        for sh in days:
            yield '_'.join((ch, sh))


# lists = []


class QQmusicSpider(Spider):
    # 爬虫名称
    name = 'QQ'
    # 起始链接
    start_urls = ['https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_opt.fcg?page=index&format=html&v8debug=1']

    # 回调函数
    def parse(self, response):
        dict_data = json.loads(response.text.replace('jsonCallback(', '').replace('\n)', '').strip())
        # 参数链接
        parse_link = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?date={time}&topid={id}&type={type}'
        # 获取巅峰榜数据
        # jsonpath(dict_data[0], '$..topID')
        for on_data in dict_data:
            # 判断是top榜还是global榜
            if jsonpath(on_data, "$..GroupID")[0] == 0:
                for ch in on_data["List"]:
                    # topID
                    top_id = jsonpath(ch, '$..topID')
                    # update_key
                    upTime = jsonpath(ch, '$..update_key')
                    # 返回请求
                    if len(str(upTime).split('-')) == 3:
                        for sh in longTime():
                            yield Request(url=parse_link.format(time=sh, id=top_id[0], type="top"), callback=self.MusicInfos, meta={'top_id': top_id[0]})
                    if len(str(upTime).split('_')) == 2:
                        for sh in shortTime():
                            yield Request(url=parse_link.format(time=sh, id=top_id[0], type="top"), callback=self.MusicInfos, meta={'top_id': top_id[0]})
            elif jsonpath(on_data, "$..GroupID")[0] == 1:
                print('1')
                for ch in on_data["List"]:
                    top_id = jsonpath(ch, "$..topID")
                    upTime = jsonpath(ch, "$..update_key")
                    # 构建请求
                    if len(upTime) > 0:
                        for ch in globalTimeFunc(str(upTime[0])):
                            yield Request(url=parse_link.format(time=ch, id=top_id[0], type="global"), callback=self.MusicInfos, meta={"top_id": top_id[0]})

        # # global榜
        # elif jsonpath(musicInfos, "$..GroupID") == 1:
        #     for ch in on_data["List"]:
        #         # top_id
        #         top_id = jsonpath(ch, '')

    def MusicInfos(self, response):
        # if isinstance(json.loads(response.text), dict):
        # lists.append(response.url)
        if len(response.text) > 10:
            # lists.append(response.url)
            # 实例化item
            item = QqmiuscmasterItem()
            # 格式话数据格式为json
            json_data = jsonpath(json.loads(response.text), '$..data')
            # meta传递数据
            meta_data = response.meta['top_id']
            item['top_id'] = meta_data
            for ch in json_data:
                item['songid'] = jsonpath(ch, '$..songid')[0]
                item['songname'] = jsonpath(ch, '$..songname')[0]
                item['songorig'] = jsonpath(ch, '$..songorig')[0]
                # 返回item实例
                yield item
        # print(len(lists))
