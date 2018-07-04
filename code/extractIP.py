import requests
import re
import pymongo


class GET_IP(object):

    def __init__(self, num):
        # 初始化数据
        self.url = 'http://www.89ip.cn/tqdl.html?num={num}'
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
        self.num = num
        conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = conn['proxy']
        self.collection = db['ip']

    # 获取IP
    def parse_ip(self):
        res_text = requests.get(url=self.url.format(num=self.num), headers=self.header).text
        proxy = re.findall(r'(\d+.\d+.\d+.\d+:\d+)<br>', res_text)

        # 验证IP可用性并存入数据库
        for ip in proxy:
            res = requests.get(url='https://weibo.com/', headers=self.header, proxies={'http': ip})
            if res.status_code == 200:
                dict_data = {'ip': ip}
                self.collection.insert(dict_data)

        # 完结撒花❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀❀


if __name__ == '__main__':
    ip = GET_IP(1024)
    ip.parse_ip()
