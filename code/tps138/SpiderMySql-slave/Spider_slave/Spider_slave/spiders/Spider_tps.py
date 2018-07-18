from scrapy_redis.spiders import RedisSpider
from scrapy import Selector
from Spider_slave.items import SpiderSlaveItem
from redis import Redis


class tpsDataSpider(RedisSpider):
    name = 'tps'
    # 指定爬虫爬取的URL队列
    redis_key = 'tps:start_urls'

    redis = Redis(host='127.0.0.1', port=6379, db=0)

    def parse(self, response):
        rel = Selector(response)

        # 实例化模型对象
        item = SpiderSlaveItem()

        # 获取所需数据
        # 商品名称
        titles = rel.xpath('/html/body/main/div/div/div/div/h1/text()').extract()
        # 商品编号
        codes = rel.xpath('//span[@class="js-sku d-ib ml-10"]/text()').extract()
        # 商品价格
        prices = rel.xpath('//b[@id="shop_price"]/text()').extract()
        # 商品库存
        stocks = rel.xpath('//span[@id="goods_number"]/text()').extract()
        # 商品图片
        images = rel.xpath('//div[@class="imageMenu"]//img/@src').extract()

        # 模型类字段赋值
        item['goods_title'] = self.get_data(titles)

        item['goods_code'] = self.get_data(codes)

        item['goods_price'] = self.get_data(prices)

        item['goods_stock'] = self.get_data(stocks)

        item['goods_image'] = self.get_data(images)

        source, data = self.redis.blpop('tps_flag')

        item['goods_type'] = data.decode('utf-8')

        # 返回item
        yield item

    # 验证数据函数
    def get_data(self, data):
        if len(data) > 0:
            return data[0].strip().replace("-1", '')

    # def get_title(self, titles):
    #     if len(titles) > 0:
    #         return titles[0]
    #
    # # def get_code(self, codes):
    #     if len(codes) > 0:
    #         return codes[0]
    #
    # def get_price(self, prices):
    #     if len(prices) > 0:
    #         return prices[0].strip()
    #
    # def get_stock(self, stocks):
    #     if len(stocks) > 0:
    #         return stocks[0].strip()
    #
    # def get_image(self, images):
    #     if len(images) > 0:
    #         return images[0]
