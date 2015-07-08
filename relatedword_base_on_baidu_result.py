'''
基于百度搜索结果的高频词词云展示
'''
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup
import re
import string
import sys

### 滤除非字母与数字
def OnlyCharNum(s,oth=''):
	    s2 = s.lower();
	    fomart = 'abcdefghijklmnopqrstuvwxyz0123456789'
	    for c in s2:
	        if not c in fomart:
	            s = s.replace(c,'');
	    return s;
	
class baidu_result_filter:
    def __init__(self,myname,keywordsnum):
        self.myname = myname
        self.keywordsnum = keywordsnum
        if int(self.keywordsnum) == 0:
                self.keywords=[self.myname]
        else:
                self.keywords=['']*int(self.keywordsnum) 
                for k in range(int(self.keywordsnum)):
                    self.keywords[k]=raw_input("请输入关联的关键字%d\n"%(k+1))
            
        url1 = "http://www.baidu.com/s?wd="+self.myname
        response1 = urllib2.urlopen(url1)  
        content1 = response1.read() 
        soup1 = BeautifulSoup(content1)
        site1 = soup1.find(class_="nums").get_text()
        self.num = string.atoi(OnlyCharNum(site1[11:-1].strip() .lstrip() .rstrip(',')))
        self.page = self.num/10
        print self.num,self.page
        self.set_pages()
        self.filename = self.myname+".txt"
        self.myfile = open(self.filename,"w")
        self.keywordshownum = 0

        for i in range(int(self.page)):
                self.url="http://www.baidu.com/s?wd="+self.myname+"&pn=%d"%(10*i)
                print ('Page：%d/%d/%d'%((i+1),(int)(self.page),(self.keywordshownum)))
                self.response = urllib2.urlopen(self.url)  
                self.content =self.response.read() 
                self.soup = BeautifulSoup(self.content)
                self.sites = self.soup.find_all(class_="c-abstract")	#find_all返回的是list，find返回的是obj
                self.pretext=' '.encode('gb18030')
                for site in self.sites:
                        self.text = site.get_text().encode('gb18030')
                        if cmp(self.text,self.pretext) == 0:
                            break
                        else:
                            self.pretext=self.text
                            self.after_re_text = re.sub("[A-Za-z0-9\[\ \【\】\＂\-\。\…\★\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", self.text.decode("gb18030")).encode("gb18030")
                            self.myfile.write(self.after_re_text)
                            for keyword in self.keywords:
                                if keyword in self.after_re_text:
                                    print self.after_re_text
                                    self.keywordshownum = self.keywordshownum+1
                                    break

        self.myfile.close()  
    def set_pages(self):
        page_num = 0
        page_num = raw_input("请输入要展示以及统计的页数\n")
        if (page_num) != '':
            self.page = int(page_num)
    

###分词
class PostContent:

    def __init__(self):
        self.url='http://nlp.csai.tsinghua.edu.cn/app/wordSegment/FrontPage.jsp'
        self.proxy_support = urllib2.ProxyHandler({'http':self.url})
        self.opener = urllib2.build_opener(self.proxy_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        self.html = urllib2.urlopen(self.url)
        self.html_content = self.html.read()
        self.soup = BeautifulSoup(self.html_content)
        
    def postcontent(self,up_content): 
        self.SegmentText=up_content.encode('utf-8')
        self.postdata = urllib.urlencode({
            'SegmentText':self.SegmentText
            })
        self.req = urllib2.Request(
            self.url,
            data = self.postdata
            )
        self.result = urllib2.urlopen(self.req).read()
        self.result_soup = BeautifulSoup(self.result)
        self.segmentedword = self.result_soup.find(id = "SegmentedText").get_text().encode("gb18030")
        print self.segmentedword
    def save_result(self,name):
        self.name = "result_"+name+".txt"
        self.myfile = open(self.name,"w")
        self.myfile.write(self.segmentedword)
        self.myfile.close()

###词频统计
class Count:
    def __init__(self):
        self.keyword_show_num = 5
    def create_lis(self,file_before_count):
        self.num = 0
        self.length=len(file_before_count)
        print self.length
        self.lis = []
        self.sorted_lis=[]
        i = 0
        while i < (self.length):        ###根据空格将分好的词加入list
            now_char = ''
            while i < self.length and file_before_count[i] != ' ' :
                now_char = now_char + file_before_count[i]
                i +=1
            if now_char != '' and now_char != ' ':
                flag = 0
                list_len = len(self.lis)
                for k in range(list_len):
                    if cmp(self.lis[k],now_char) == 0:
                        flag = 1
                        self.sorted_lis[k] += 1
                        break
                if flag == 0:
                    self.lis.append(now_char)
                    self.sorted_lis.append(1)
                    print now_char,self.num,"/",self.length
                    #print self.num,"/",self.length
                    self.num += 1
            i += 1
        self.num -= 1
    def get_result(self):
         sorted_lis_len=len(self.lis)
         for i in range(sorted_lis_len):
             if self.sorted_lis[i] > self.keyword_show_num and len(self.lis[i]) > 2 and self.lis[i] != "的" and self.lis[i] != "啊" and self.lis[i] != "月日" and self.lis[i] != "了" :
                 print self.lis[i],self.sorted_lis[i]
        
    def set_keyword_show_num(self,keyword_show_num):
        self.keyword_show_num = int(keyword_show_num)  
          
                               
if __name__ == '__main__':
    myname = raw_input("请输入姓名\n")
    keywordsnum = raw_input("请输入需筛选的关联词个数(一般输入0即可)\n")
    baidu_result = baidu_result_filter(myname,int(keywordsnum))
    xx = PostContent()
    file_name = (myname + ".txt")
    readf = open(file_name,"r")
    readfile = readf.read().decode("gb18030").encode("gb18030")
    sub_readfile = re.sub("[A-Za-z0-9\[\ \、\_\【\＂\】\-\。\…\★\`\~\!\?\@\#\$\^\&\*\(\)\=\|\{\}\'\"\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", readfile.decode("gb18030")) 
    readf.close()
    xx.postcontent(sub_readfile)
    xx.save_result(myname)
    print "================================================"
    keyword_num = Count()
    keyword_num.create_lis(xx.segmentedword)
    keyword_num.set_keyword_show_num(10)
    print "你搜索的关键词为：%s 相关标签如下：\n" %myname
    keyword_num.get_result()
