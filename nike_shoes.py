import urllib,urllib2,cookielib
from bs4 import BeautifulSoup
import time,webbrowser


class Shoe_Size_Monitor:##鞋码监控
    def __init__ (self):
        self.url = raw_input("请将鞋子页面的链接复制过来\n")
        self.second = raw_input("请输入刷新间隔时间(单位秒)\n")
        self.html = urllib2.urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html)
        self.title = self.soup.head.title.get_text().encode('gb18030')
        print("您选择的鞋子型号为：%s")%self.title
        self.pre_num = self.num = 0
        self.options = self.soup.find_all("option")
        self.keyword1 = "exp-pdp-size-not-in-stock selectBox-disabled"
        self.keyword2 ="skuId"
        solds = []
        sells = []
        for option in self.options:
            x = option.encode("utf-8").find(self.keyword1)
            if x != -1:
                self.num += 1
                solds.append(option.get_text().encode('gb18030').strip())
            else:
                if option.encode("utf-8").find(self.keyword2) != -1:
                    sells.append(option.get_text().encode('gb18030').strip())
            self.pre_num = self.num
        print "无货尺码:",solds
        print "有货尺码:",sells
    def monitor(self):
        print "监控中"
        while True:
            self.num = 0
            for option in self.options:
                x = option.encode("utf-8").find(self.keyword1)
                if x != -1:
                    self.num += 1
            if self.num > self.pre_num:
                print "新鞋码放出！！"
                webbrowser.open(self.url)
            else:
                print "无变化。"
            #print self.pre_num,"/",self.num
            time.sleep(int(self.second))
    
'''
class Login_In:
    def __init__ (self):
        self.username = ""
        self.password = ""
        self.rememberMe = "false"
        self.url = "http://www.nike.com"
        self.request_body = urllib.urlencode({
            'login':self.username,
            'rememberMe':self.rememberMe,
            'password':self.password
        })
        self.proxy_support = urllib2.ProxyHandler({'http':self.url})
        self.cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(self.proxy_support,self.cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        req = urllib2.Request(
            self.url,
            self.request_body
            )
        self.result = urllib2.urlopen(req).read()
        self.soup = BeautifulSoup(result)
        print self.soup
'''
if __name__ == '__main__':
    shoe_size_monitor = Shoe_Size_Monitor()
    shoe_size_monitor.monitor()
