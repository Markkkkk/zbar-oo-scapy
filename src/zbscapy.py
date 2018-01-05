# coding: utf8

import urllib2
import os  
import re  
import threading
from bs4 import BeautifulSoup

BASE_FOLDER_PATH = 'picture'
PORT_HOST = 'http://m.meituri.com/'
HOST_PREFIX = 'http://m.meituri.com/t'
MAX_PAGE_NUM = 387

def input_data():
    print('feed data to tensorflow')
    
def downloadUrl(url):
    try:
        response = urllib2.urlopen(url, timeout=10)

        response.encoding = 'utf-8'

        if response.getcode() == 200:
            return response.read()
        else:
            print('error:request failed')
            return ''
    except Exception, e:
        print('exception:'+e.message)
        print('reopen')
        # fix me, dead cycle perhapse
        return downloadUrl(url)

def checkDocuments(path):
    if os.path.exists(path) == False:
        os.mkdir(path)

'''
def downloadPage(url):

    print "page:"+url  
    # 获取当前页面数据  
    content = downloadUrl(url)  
    # 传入页面数据content，创建beautifulsoup对象soup  
    soup = BeautifulSoup(content,  
                         'html.parser',  
                         from_encoding='utf-8')  
    # 获取单页中18个图片专辑的父节点  
    album_block = soup.find('ul', id='images')  
    # 获取父节点下图片专辑地址的a节点集  
    album_nodes = album_block.findAll('a', href=re.compile(r'http://www.znzhi.net/p/'))  
    # 由于每个专辑的a标签有两个，用[::2]获取a节点集中的偶数项，循环下载图片专辑  
    for album_node in album_nodes[::2]:  
        # 调用downloadAlbum  
        # 传入album_node.get('href')获取a节点的href值，即专辑地址  
        downloadAlbum(album_node.get('href'))  
        # 若运行中想终止爬虫程序，可在同父目录下新建stop.txt文件  
        if os.path.exists('stop.txt'):  
            exit(0)  
        # 设置图片专辑下载间隙休眠，防止因访问频繁，被网站拉黑  
        time.sleep(4)
        
def downloadAlbum(url):  
    print "album:"+url
    # 获取当前页面数据  
    content = downloadUrl(url)  
    # 传入页面数据content，创建beautifulsoup对象soup  
    soup = BeautifulSoup(content,  
                         'html.parser',  
                         from_encoding='utf-8')  
    # 获取存有图片专辑标题的h2标签  
    title = soup.find('div', class_='content').find('h2')  
    # 检查是否有内容，在实际爬取中，有遇到过空图片专辑的情况，  
    if title == None:  
        print "error:web content has lost"  
        return  
    # 通过正则筛选出标题中含有的总图片数值  
    title_num = re.findall(r'\d+', title.get_text())  
    pic_count = int(title_num[-1])  
    # 将（1/num)截取去除，并添加总图片数 [num]  
    title_split = title.get_text().split(' (', 1)  
    album_title = title_split[0]+'['+str(pic_count)+']'  
    # 删去标题中的'/'字符，防止在用标题作为名称建图片文件夹时报错  
    album_title = album_title.replace('/', ' ')  
    # 拼接本地文件夹路径，并检查路径是否存在，防止重复下载  
    path = BASE_PATH + "/" + album_title  
    if os.path.exists(path):  
        print '  -> ' + album_title + ' has exists'  
        return True  
    # 新建存放当前专辑的图片文件夹  
    checkDocuments(path)  
    print path  
    # 新建一个html，存有此图片专辑相关信息  
    with open(path+'/source.html','w') as fout:  
        fout.write("<html>")  
        fout.write("<body>")  
        fout.write("<p>"+album_title.encode('utf-8')+"-["+str(pic_count)+"p]"+"</p>")  
        fout.write("<a href=\""+url.encode('utf-8')+"\">来源网址:"+url.encode('utf-8')+"</a>")  
        fout.write("</body>")  
        fout.write("</html>")  
    # 循环下载专辑中各个图片  
    for num in range(1, pic_count+1):  
        pic_url = url+"/"+str(num)+'.html'  
        i=0  
        while downloadOnePic(path, pic_url) == False:  
            print 'redownload'  
            i=i+1  
            if i > 5:  
                print "timeout's time too much"  
                break
# 获取相册名称  
def getPicName(picUrl) :  
    # 截取地址中最后一个/后面的字符，即图片名
    picName = os.path.basename(picUrl)  
    if '.jpg' in picName:  
        return picName  
    return 'error.jpg'

# 下载单张照片
def downloadOnePic(path,url):

    soup = BeautifulSoup(downloadUrl(url),  
                         'html.parser',  
                         from_encoding='utf-8')  
    # 获取存有img节点  
    img_node = soup.find('div', class_='main-image').find('img')  
    # 获取img的src值，即图片地址  
    pic_url = img_node.get('src')  
    # 调用getPicName()获取图片名称  
    pic_name = getPicName(pic_url).encode('utf-8')  
    try:  
        # 访问图片地址，获取数据  
        content = urllib2.urlopen(pic_url, timeout=10).read()  
        # 保存图片到本地  
        with open(path + '/' + pic_name, 'wb') as code:  
            code.write(content)  
        print '  -> ' + pic_name + " download success"  
    #捕获异常  
    except Exception, e:  
        print "exception:"+e.message  
        return False  
    return True 
'''

# 主函数
if __name__ == "__main__":
    # 检查本地下载路径是否存在
    checkDocuments(BASE_FOLDER_PATH)
    
    # 循环访问
    for i in range(1, MAX_PAGE_NUM+1):
        # 拼接页地址，fix me
        page_url = HOST_PREFIX + '/' + str(i) + '.html'  
        # 保存当前页码，供查看下载进度
        with open('cur_page.txt', 'w') as fpage:  
            fpage.write(str(i))  
        # 以页为单位进行下载
        '''downloadPage(page_url)'''       
        
