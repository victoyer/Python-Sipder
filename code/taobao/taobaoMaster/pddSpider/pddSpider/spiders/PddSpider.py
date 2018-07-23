import scrapy
import json
import re
from jsonpath import jsonpath

from pddSpider.items import PddspiderItem


class PDDSpiderGo(scrapy.Spider):
    name = 'pdd'
    url = 'https://tce.alicdn.com/api/data.htm?ids=222887%2C222890%2C222889%2C222886%2C222906%2C222898%2C222907%2C222885%2C222895%2C222878%2C222908%2C222879%2C222893%2C222896%2C222918%2C222917%2C222888%2C222902%2C222880%2C222913%2C222910%2C222882%2C222883%2C222921%2C222899%2C222905%2C222881%2C222911%2C222894%2C222920%2C222914%2C222877%2C222919%2C222915%2C222922%2C222884%2C222912%2C222892%2C222900%2C222923%2C222909%2C222897%2C222891%2C222903%2C222901%2C222904%2C222916%2C222924'

    # start_urls = [url]

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_item)

    def parse_item(self, response):
        # 切割匹配ID
        type_ids = self.url.split('=')[-1].split('%2C')
        # 处理获取到的请求对象
        dict_data = json.loads(response.text)
        # 根据商品分类ID获取对应数据
        for ch in type_ids:
            print(ch)
            # if int(ch) != 222887 and int(ch) != 222890 and int(ch) != 222889 and int(ch) != 222886:
            # 每个大分类的数据
            max_type_data = dict_data[ch]
            # 每个大分类的名称
            max_type_name = jsonpath(max_type_data, '$..head')[0][0].get('name')
            # 每个小分类数据 max_type_data.get('value').get('head')[0].get('name')
            min_type_datas = max_type_data.get('value').get('list')
            for sh in min_type_datas:
                # 每个小分类名称
                min_type_name = sh.get('name')
                # 每个小分类链接
                min_type_link = sh.get('link')
                # 组装每个小分类的list链接
                for page in range(10):
                    if ':' in str(min_type_link):
                        min_list_link = min_type_link + '&bcoffset=12&s=%d' % page * 60
                        yield scrapy.Request(url=min_list_link,
                                             meta={'max_type_name': max_type_name, 'min_type_name': min_type_name},
                                             callback=self.get_detail_page)

    def get_detail_page(self, response):
        # 获取meta参数的值
        meta_params = response.meta
        # 获取详情页链接
        detail_urls = re.findall(r'"detail_url":"//(.*?)"', response.text)
        # 实例化模型对象
        item = PddspiderItem()
        # 循环取出每个链接
        for th in detail_urls:
            # 拆分链接
            around = th.split('id')
            # 判断每个链接是否存在
            if len(around) == 2:
                # 转码并合并链接
                detail_link = 'https://' + around[0] + 'id' + (around[1].encode('utf-8').decode('unicode_escape'))
                # 返回请求detail链接的请求对象和meta参数
                item['detail_link'] = detail_link
                item['meta_params'] = {'max_type_name': meta_params['max_type_name'],
                                       'min_type_name': meta_params['min_type_name']}
                yield item
