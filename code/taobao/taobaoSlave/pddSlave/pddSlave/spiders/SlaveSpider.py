from scrapy_redis.spiders import RedisSpider
from scrapy import Selector
from redis import Redis
import re, json
from pddSlave.items import PddspiderItem


class pddSpider(RedisSpider):
    # 爬虫名称
    name = 'slave'
    # 指定爬虫访问的url队列
    redis_key = 'pdd:start_urls'

    def parse(self, response):
        rel = Selector(response)
        # 实例化模型对象
        item = PddspiderItem()
        # 模型实例赋值
        item['goods_name'] = self.get_detail_name(rel)  # //h3[@class="tb-main-title"]/text()
        item['goods_price'] = self.get_detail_price(rel)  # //em[@class="tb-rmb-num"]/text()
        item['goods_imgs'] = self.get_detail_imgs(response)  # //*[@class='tb-pic tb-s50']//img/@src
        item['goods_stock'] = self.get_detail_stock(rel)  # //span[@id="J_SpanStock"]/text()
        item['goods_detail'] = self.get_detail_detail(rel)  # //ul[@class="attributes-list"]/li/text()

        # 取出redis中的类别数据
        redisCli = Redis(host='127.0.0.1', port=6379, db=0)
        data = eval(redisCli.lpop('pdd:meta_params').decode('utf-8'))

        item['goods_maxType'] = data.get('max_type_name')
        item['goods_minType'] = data.get('min_type_name')
        item['goods_ID'] = self.get_detail_id(response)
        # 返回item
        yield item

    def get_detail_name(self, rel):
        datas = rel.xpath('//h3[@class="tb-main-title"]/text()').extract()
        if len(datas) > 0:
            return datas[0].strip()

    def get_detail_price(self, rel):
        datas = rel.xpath('//em[@class="tb-rmb-num"]/text()').extract()
        if len(datas) > 0:
            return datas[0].strip()

    def get_detail_imgs(self, response):
        datas = re.findall(r'"//(.*jpg)"', response.text)
        if len(datas) > 0:
            return [ch.replace('//', '') for ch in datas]

    def get_detail_stock(self, rel):
        datas = rel.xpath('//span[@id="J_SpanStock"]/text()').extract()
        if len(datas) > 0:
            return datas[0].strip()

    def get_detail_detail(self, rel):
        datas = rel.xpath('//ul[@class="attributes-list"]/li/text()').extract()
        if len(datas) > 0:
            detail_data = ','.join([ch.replace('\xa0', '') for ch in datas])
            return detail_data

    def get_detail_id(self, response):
        goods_ids = re.findall(r'id=(\d+?)&', response.url)
        if len(goods_ids) > 0:
            return goods_ids[0]
