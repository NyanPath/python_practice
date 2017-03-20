# -*- coding: UTF-8 -*-
import requests, re

class QQTN():
    def __init__(self):
        self.url = ''

if __name__ == '__main__':
    a = u'\u0068\u0074\u0074\u0070\u003a\u002f\u002f\u0063\u006c\u002e\u006d\u006f\u0063\u006c\u002e\u0078\u0079\u007a\u002f'
    print requests.get(a.encode('utf-8'), headers={'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1Safari/534.50'}).content