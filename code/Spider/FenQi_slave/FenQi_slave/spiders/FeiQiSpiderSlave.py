from scrapy_redis.spiders import RedisSpider
from scrapy import Selector
from random import randint

from FenQi_slave.items import FenqiSlaveItem


# 定义一个排除列表空元素的函数
def net_emply(event):
    return event.strip()


class FenQiGetDetallSpider(RedisSpider):
    # 爬虫名称
    name = 'fqs'
    # 指定访问redis中的urls队列
    redis_key = 'fenqi:start_urls'

    # 回调函数
    def parse(self, response):
        rel = Selector(response)
        # 实例化item类
        item = FenqiSlaveItem()
        # item实例模型赋值
        item['goods_name'] = self.get_title(rel)
        item['goods_price'] = self.get_price(rel)
        item['goods_img'] = self.get_imgs(rel)
        item['goods_type'] = self.get_type(rel)
        item['goods_desc'] = self.get_desc(rel)
        item['goods_cprice'] = self.get_cprice(rel)
        item['goods_sales'] = self.get_sales()
        item['goods_stock'] = self.get_stock()
        item['goods_click'] = self.get_click()

        # 返回item
        yield item

    def get_title(self, rel):
        # 获取商品名称
        titles = rel.xpath('//span[@id="product_name"]/text()').extract()
        if len(titles) > 0:
            return titles[0]

    def get_price(self, rel):
        # 获取商品价格
        prices = rel.xpath('//strong[@class="pr-price"]/text()').extract()
        if len(prices) > 0:
            return prices[0]

    def get_imgs(self, rel):
        # 获取商品图片
        imgs = rel.xpath('//li[@data-rel="item"]//img/@src').extract()
        if len(imgs) > 0:
            return imgs

    def get_type(self, rel):
        # 获取商品对应类别
        types = rel.xpath('/html/body/main/div/div/span[5]/a/text()').extract()
        if len(types) > 0:
            return types[0]

    def get_desc(self, rel):
        # 获取商品描述
        desc_list = rel.xpath('//ul[@class="fn-clear"]//li/text()').extract()
        if len(desc_list) > 0:
            # 去除获取到的的商品描述信息列表中的空值
            desc_lsit = list(filter(net_emply, desc_list))
            goods_desc = ''.join(desc_lsit)
            return goods_desc

    def get_cprice(self, rel):
        # 获取商品原价
        cprices = rel.xpath('//strong[@class="pr-price"]/text()').extract()
        if len(cprices) > 0:
            return cprices[0] + '100'

    def get_sales(self):
        # 随机获取商品销量
        return randint(10, 1000)

    def get_stock(self):
        # 随机获取商品库存
        return randint(100, 10000)

    def get_click(self):
        # 随机获取商品的点击次数
        return randint(10, 10000)
