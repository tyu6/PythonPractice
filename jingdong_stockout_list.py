import urllib2
from bs4 import BeautifulSoup


f = open("jingdong.txt","w")

for i in range(100001,1250000):
    stock_url = "http://search.jd.com/stock?skus=%d&district=12_904_905&callback=get_stock_cb" %i
    stock_response = urllib2.urlopen(stock_url)  
    stock_content = stock_response.read() 
    stock_soup = BeautifulSoup(stock_content)
    yes = "786465"        #京东数据库里的值
    no = "786466"
    stock_info = stock_soup.get_text().find(no)

    itemname_url = "http://item.jd.com/%d.html" %i
    itemname_response = urllib2.urlopen(itemname_url)  
    itemname_content = itemname_response.read() 
    itemname_soup = BeautifulSoup(itemname_content)
    itemname_info = itemname_soup.body.find(id="product-intro").find(id='name').h1.get_text()


    if stock_info != -1 :
        #print itemname_info,"【缺货】"
        print 1250000-i
        f.write(itemname_info.encode('gb18030')+"【缺货】\n")
    
f.close()
