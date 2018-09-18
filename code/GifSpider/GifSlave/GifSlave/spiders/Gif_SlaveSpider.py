from scrapy_redis.spiders import RedisSpider
from GifSlave.items import GifslaveItem

BASE_DIR = "e:/Gif/"


class gifSlaveSpider(RedisSpider):
    name = 'slave'
    redis_key = "img_url"

    def parse(self, response):
        filename = str(response.url)[str(response.url).rfind("/") + 1:]
        filedir = BASE_DIR + filename
        with open(filedir, "wb") as f:
            f.write(response.body)

        if response.status == 200:
            item = GifslaveItem()
            item["imgName"] = filename
            item["imgDir"] = filedir
            item["imgUrl"] = response.url

            yield item
