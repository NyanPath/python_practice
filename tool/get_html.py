# -*- coding: UTF-8 -*-
import requests, random, time
from fake_useragent import UserAgent

class HtmlPro:
    def __init__(self):
        self.headers = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']

    def get_headers(self):
        headers_dict = {}
        headers_dict['User-Agent'] = str(ua_.random)
        return headers_dict

    def get_html(self, url, proxies=None):
        link_time = 1
        time.sleep(link_time * 3)
        while True:
            try:
                html = requests.get(url, headers=self.get_headers(), proxies=proxies, timeout=30).text
                return html
            except Exception:
                print ('第%s次连接出错，等待重试' % str(link_time))
                link_time += 1

if __name__ == '__main__':
    hp = HtmlPro()
    ua_ = UserAgent()

else:
    hp = HtmlPro()
    ua_ = UserAgent()