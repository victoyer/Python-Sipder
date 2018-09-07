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
            time = '_'.join((ch, sh.zfill(2)))
            yield time


# 返回长的时间参数
def longTime():
    # year = ['2014', '2015', '2016', '2017', '2018']
    # month = [str(ch) for ch in range(1, 13)]
    # month09 = [str(ch) for ch in range(9, 13)]
    # days = [str(ch) for ch in range(1, 31)]
    # time = ''
    # for ch in year:
    #     if ch == '2014':
    #         for sh in month09:
    #             for zh in days:
    #                 time = '-'.join((ch, sh.zfill(2), zh.zfill(2)))
    #     else:
    #         for sh in month:
    #             for zh in days:
    #                 time = '-'.join((ch, sh.zfill(2), zh.zfill(2)))
    #     yield time
    year = ['2014', '2015', '2016', '2017', '2018']
    month = [str(ch) for ch in range(1, 13)]
    days = [str(ch) for ch in range(1, 31)]
    for ch in year:
        for sh in month:
            for zh in days:
                time = '-'.join((ch, sh.zfill(2), zh.zfill(2)))
                yield time


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
        parse_link = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?date={time}&topid={id}&type=top'
        # 获取巅峰榜数据
        # jsonpath(dict_data[0], '$..topID')
        for ch in jsonpath(dict_data[0], '$..List')[0]:
            # topID
            top_id = jsonpath(ch, '$..topID')
            # update_key
            upTime = jsonpath(ch, '$..update_key')
            # 返回请求
            if len(str(upTime).split('-')) == 3:
                for ch in longTime():
                    yield Request(url=parse_link.format(time=ch, id=top_id[0]), callback=self.MusicInfos,
                                  meta={'top_id': top_id[0]})
            if len(str(upTime).split('_')) == 2:
                for ch in shortTime():
                    yield Request(url=parse_link.format(time=ch, id=top_id[0]), callback=self.MusicInfos,
                                  meta={'top_id': top_id[0]})
            print(response)
            print(ch)

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
