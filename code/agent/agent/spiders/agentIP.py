import scrapy
from scrapy import Request
from scrapy import Selector
import json


class AgentIpSpider(scrapy.Spider):


    def start_requests(self):
        yield Request(self.url.format(page=self.page), callback=self.xiciAgent)

    def xiciAgent(self, response):
        # print(response.text)
        res = Selector(response)

        # print(len(IpList))
        # print(len(IpPort))
        # print(len(IpAgen))

