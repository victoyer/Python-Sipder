from scrapy import Spider, Selector, Request
import re, json, math
from Gif.items import GifItemInfo


class GifSpider(Spider):
    name = 'Gif'
    # allowed_domains = ["http://soogif.com"]
    start_urls = ["http://www.soogif.com/sort/124"]
    ImageLinks = "http://www.soogif.com/material/query/?query={keyword}&start={start_num}&size=50"

    def parse(self, response):
        rel = Selector(response)
        cationType = rel.xpath('//div[@class="tab clearfix"]//div[@class="left clearfix"]//a/@href').extract()
        for ch in cationType:
            if ch.startswith("/sort/"):
                yield Request(url="http://www.soogif.com" + ch, callback=self.PageFunc)

    def PageFunc(self, response):
        page = Selector(response).xpath('//input[@id="hidePageCount"]/@value').extract()
        if len(page) > 0:
            for ch in range(1, int(page[0]) + 1):
                yield Request(url=str(response.url) + "?pageNumber=" + str(ch), callback=self.GetTypeName)

    def GetTypeName(self, response):
        SearchName = Selector(response).xpath(
            '//div[@class="module-1 clearfix"]/div[@class="up clearfix"]/a/@href').extract()
        for ch in SearchName:
            keyword = re.findall(r"/search/(.*)", ch)[0]
            start_num = 0
            yield Request(url=self.ImageLinks.format(keyword=keyword, start_num=start_num), callback=self.GetImgLink)

    def GetImgLink(self, response):
        resuLtTotal = json.loads(response.text)["data"]["resuLtTotal"]
        sum = int(math.ceil(resuLtTotal / 50))
        for ch in range(sum):
            yield Request(url=re.sub(r"start=\d+", "start=" + str(50 * ch), response.url), callback=self.GetImages)

    def GetImages(self, response):
        item = GifItemInfo()
        DataList = json.loads(response.text)["data"]["list"]
        for ch in DataList:
            item["url"] = self.get_data(ch, "url")
            item["sid"] = self.get_data(ch, "sid")
            item["size"] = self.get_data(ch, "size")
            item["width"] = self.get_data(ch, "width")
            item["title"] = self.get_data(ch, "title")
            item["height"] = self.get_data(ch, "height")
            item["subText"] = self.get_data(ch, "subText")

            yield item

    def get_data(self, ch, key):
        try:
            return ch[key]
        except KeyError:
            return "NULL"
