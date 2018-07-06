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
        item['title'] = rel.xpath('//h1/text()').extract()[0]
        # 车辆价格
        item['price'] = rel.xpath('//p[@class="price detail-title-right-tagP"]/text()').extract()[0]
        # 分期信息
        stages_list = rel.xpath('//div[@class="list"]//p[@class="money detail-title-right-tagP"]/text()').extract()
        item['first_price'] = stages_list[0]
        item['evety_price'] = stages_list[1]
        # 服务费
        item['charge'] = rel.xpath('//p[@class="detail-title-right-tagP"]/strong/text()').extract()[0]
        # 上牌时间
        item['carNumTime'] = rel.xpath('//li[@class="span7"]//strong/text()').extract()[0]
        # 行驶公里
        item['travelMeile'] = rel.xpath('//li[@class="kilometre"]//strong/text()').extract()[0]
        # 外迁
        item['migretion'] = rel.xpath('//li[@class="span5 car-fluid-standard"]//strong/text()').extract()[0]
        # 车辆排量
        item['displacement'] = rel.xpath('//li[@class="span displacement"]//strong/text()').extract()[0]
        # 上牌城市
        item['oncarcity'] = rel.xpath('//strong[@id="car-licensed"]/@licensed-city').extract()[0]
        # 车辆图片
        item['carImgLink'] = rel.xpath('//img[@class="main-pic"]/@src').extract()[0]
        # 车辆ID
        ids = rel.xpath('//p[@class="detail-car-id"]/text()').extract()
        item['id'] = ids[0].strip()[ids[0].strip().rfind('：') + 1:]

        # 返回item
        yield item
