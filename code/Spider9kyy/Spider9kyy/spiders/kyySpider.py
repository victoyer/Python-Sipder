# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 19:25
# @Author  : conal
# @FileName: kyySpider.py
# @Software: PyCharm

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Spider9kyy.items import Spider9KyyItem
from urllib.parse import unquote
import re
import os


class KyySpider(CrawlSpider):
    name = "kyy"
    url = "http://www.9kyy.com/index.php/vod/type/id/dianying.html"
    link = "http://www.9kyy.com"

    def start_requests(self):
        yield Request(url=self.url, callback=self.GetPageNum)

    def GetPageNum(self, response):
        # pageNum = Selector(response=response).xpath('/html/body/div[3]/div/div[4]/div[2]/a[7]/text()').extract()
        # if len(pageNum) > 0:
        for ch in range(1, 11):
            yield Request(url=response.url[:response.url.rfind(".")] + '/page/{page}.html'.format(page=ch),
                          callback=self.Get_Film_Link)

    def Get_Film_Link(self, response):
        Links = re.findall(r'<a class="fed-list-title.*?href="(.*)?">', response.text)
        if len(Links) > 0:
            for ch in Links:
                yield Request(url=self.link + ch, callback=self.GetFilmInfo)

    def GetFilmInfo(self, response):
        requestUrl = re.findall(r'<a class="fed-deta-down.*href="(.*)?">', response.text)
        if len(requestUrl) > 0:
            items = Spider9KyyItem()
            rel = Selector(response=response)
            title = rel.xpath('//h1[@class="fed-part-eone fed-font-xvi"]//a/text()').extract()
            if len(title) > 0:
                items['title'] = title[0]
            else:
                items['title'] = "NULL"
            type = rel.xpath('//li[@class="fed-col-xs6 fed-part-eone"]//a/text()').extract()
            if len(type) > 0:
                items["types"] = type[0]
            else:
                items["types"] = "NULL"
            description = rel.xpath('//p[@class="fed-conv-text fed-padding fed-text-muted"]/text()').extract()
            if len(description) > 0:
                items['description'] = description[0].strip()
            else:
                items['description'] = 'NULL'
            for ch in requestUrl:
                yield Request(url=self.link + ch, callback=self.GetDownVideo, meta={"items": items})

    def GetDownVideo(self, response):
        GetLink = re.findall(r'<a target="_blank" class="fed-form-info.*href="(.*)?">', response.text)
        if len(GetLink) > 0:
            # if not GetLink[0].startswith("http://ddd") and not GetLink[0].startswith("http://vip"):
            yield Request(url=GetLink[0], callback=self.SaveVideo, meta={"items": response.meta['items']})
            print("正在下载：", GetLink[0])

    def SaveVideo(self, response):
        items = response.meta["items"]
        BasePath = 'G:/film/'
        if not os.path.isdir(BasePath):
            os.mkdir(BasePath)
        VideoPath = BasePath + unquote(response.url[response.url.rfind("/") + 1:])
        with open(VideoPath, mode="wb+") as f:
            f.write(response.body)
        print("下载 %s 文件成功" % VideoPath)
        items['path'] = VideoPath
        yield items
