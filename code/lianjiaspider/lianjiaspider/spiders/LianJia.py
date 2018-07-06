import scrapy, json
from scrapy import Selector
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from lianjiaspider.items import LianjiaspiderItem


class LianJiaSpider(RedisSpider):
    name = 'lianjia'
    redis_key = 'lianjia:start_urls'

    def parse(self, response):
        # etreeHTML源码
        sel = Selector(response)

        # 实例化模型
        item = LianjiaspiderItem()

        # 房源名称
        titles = sel.xpath('//div[@class="info clear"]/div/a/text()').extract()

        # 房源地址
        adds = sel.xpath('//div[@class="houseInfo"]//a/text()').extract()

        # 房源信息
        info = sel.xpath('//div[@class="houseInfo"]/text()').extract()
        infos = [ch.strip() for ch in info]

        # 房源位置
        floor = sel.xpath('//div[@class="positionInfo"]/text()').extract()
        floors = [ch.replace('-', '').strip() for ch in floor]

        # 房源标签
        tags = sel.xpath('//div[@class="tag"]/span/text()').extract()

        # 房源总价
        total = sel.xpath('//div[@class="totalPrice"]/span/text()').extract()
        totals = [ch + '万' for ch in total]

        # 房源单价
        prices = sel.xpath('//div[@class="unitPrice"]/span/text()').extract()

        # 房源ID
        ids = sel.xpath('//li[@class="clear"]/a/@data-housecode').extract()

        # 房源区域
        item['area'] = response.meta.get('area_name')

        # 组装数据
        for ch in range(len(titles)):
            item['title'] = titles[ch]
            item['add'] = adds[ch]
            item['info'] = infos[ch]
            item['floor'] = floors[ch]
            item['tag'] = tags[ch]
            item['total'] = totals[ch]
            item['price'] = prices[ch]
            item['id'] = ids[ch]

            # 返回数据
            yield item
