from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

from rencar.items import RencarItem


class RanCarSpider(RedisSpider):
    # 爬虫名称
    name = 'rencar'
    # 指定redis的爬取URL队列
    redis_key = 'rencar:start_urls'

    # 回调函数
    def parse(self, response):
        rel = Selector(response)
        # 实例化储存模型对象
        item = RencarItem()
        # 车辆名称
        title = rel.xpath('//h1/text()').extract()
        if len(title) != 0:
            item['title'] = title[0]
        # 车辆价格
        price = rel.xpath('//p[@class="price detail-title-right-tagP"]/text()').extract()
        if len(price) != 0:
            item['price'] = price[0]
        # 分期信息
        stages_list = rel.xpath('//div[@class="list"]//p[@class="money detail-title-right-tagP"]/text()').extract()
        if len(stages_list) >= 2:
            item['first_price'] = stages_list[0]
            item['evety_price'] = stages_list[1]
        # 服务费
        charge = rel.xpath('//p[@class="detail-title-right-tagP"]/strong/text()').extract()
        if len(charge) != 0:
            item['charge'] = charge[0]
        # 上牌时间
        carNumTime = rel.xpath('//li[@class="span7"]//strong/text()').extract()
        if len(carNumTime) != 0:
            item['carNumTime'] = carNumTime[0]
        # 行驶公里
        travelMeile = rel.xpath('//li[@class="kilometre"]//strong/text()').extract()
        if len(travelMeile) != 0:
            item['travelMeile'] = travelMeile[0]
        # 外迁
        migretion = rel.xpath('//li[@class="span5 car-fluid-standard"]//strong/text()').extract()
        if len(migretion) != 0:
            item['migretion'] = migretion[0]
        # 车辆排量
        displacement = rel.xpath('//li[@class="span displacement"]//strong/text()').extract()
        if len(displacement) != 0:
            item['displacement'] = displacement[0]
        # 上牌城市
        oncarcity = rel.xpath('//strong[@id="car-licensed"]/@licensed-city').extract()
        if len(oncarcity) != 0:
            item['oncarcity'] = oncarcity[0]
        # 车辆图片
        carImgLink = rel.xpath('//img[@class="main-pic"]/@src').extract()
        if len(carImgLink) != 0:
            item['carImgLink'] = carImgLink
        # 车辆ID
        ids = rel.xpath('//p[@class="detail-car-id"]/text()').extract()
        if len(ids) != 0:
            item['id'] = ids[0].strip()[ids[0].strip().rfind('：') + 1:]

        # 返回item
        yield item
