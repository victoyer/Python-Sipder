import scrapy

from tencnet.items import TencnetItem


class TencentSpider(scrapy.Spider):
    # 爬虫名称
    name = 'tencent'

    offset = 0
    url = 'https://hr.tencent.com/position.php?start='
    # 爬虫其实爬取URL
    start_urls = [url + str(offset)]

    # 爬虫请求资源回调函数
    def parse(self, response):
        # res = Selector(response)
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            # 初始化模型对象
            item = TencnetItem()
            # 职位名称
            jobname = each.xpath('./td[1]/a/text()').extract()
            # 职位类别
            jobtype = each.xpath('./td[2]/text()').extract()
            # 招聘人数
            peoplenum = each.xpath('./td[3]/text()').extract()
            # 工作地点
            workadder = each.xpath('./td[4]/text()').extract()
            # 发布时间
            publishtime = each.xpath('./td[5]/text()').extract()

            # 赋值模型
            item['jobname'] = jobname[0] if jobname[0] else ''
            item['jobtype'] = jobtype[0] if jobtype[0] else ''
            item['peoplenum'] = peoplenum[0] if peoplenum[0] else ''
            item['workadder'] = workadder[0] if workadder[0] else ''
            item['publishtime'] = publishtime[0] if publishtime[0] else ''

            yield item

        if self.offset < 3750:
            self.offset += 10

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
