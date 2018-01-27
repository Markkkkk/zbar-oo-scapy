# coding: utf8

import urllib2
import os  
import re  
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

BASE_FOLDER_PATH = '/hdd/zbar-scapy/pictures'
PORT_HOST = 'http://www.meituri.com/zhongguo/'
HOST_PREFIX = 'http://www.meituri.com/a/'
MAX_PAGE_NUM = 1#0

def input_data():
    print('feed data to tensorflow')
    
# 按URL下载内容
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

# 检查路径，若无，创建文件夹
def checkDir(path):
    if os.path.exists(path) == False:
        os.mkdir(path)

# 入口网页，按专辑下载
def downloadHomePage(url):

    # 获取当前页面数据  
    content = downloadUrl(url)  
    # 传入页面数据content，创建beautifulsoup对象soup  
    soup = BeautifulSoup(content,  
                         'html.parser',  
                         from_encoding='utf-8')  
    # 获取单页中18个图片专辑的父节点  
    album_blocks = soup.findAll('ul')
    for album_block in album_blocks:
        # 获取父节点下图片专辑地址的a节点集  
        album_nodes = album_block.findAll('a',
                                      href=re.compile(r'http://www.meituri.com/t/'))  
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
        
        # 页面是由两段组成，前面是相册，后面是散图
        #hezi_nodes = album_block.findAll('a', href=re.compile(r'http://www.meituri.com/a/')) 
        #for hezi_node in hezi_nodes[::2]:
        #    print(hezi_node.get('href'))
        #    time.sleep(4)
        
# 按相册下载
def downloadAlbum(url):  
    print "album:"+url
    # 获取当前页面数据  
    content = downloadUrl(url)  
    # 传入页面数据content，创建beautifulsoup对象soup  
    soup = BeautifulSoup(content,  
                         'html.parser',  
                         from_encoding='utf-8')  
    # 获取存有图片专辑标题的h2标签  
    album_block = soup.find('div', class_='hezi').find('ul') 

    # 获取专辑的标题，并生成文件夹，防止冲突
    albums = album_block.findAll('li')
    for album in albums:
        photos_path = album.find('a', href=re.compile(r'http://www.meituri.com/a/'))
        if photos_path == None:
            continue
        title_block = album.find('p', class_='biaoti').find('a')
        if title_block == None:
            continue
        album_title = title_block.get_text()
        album_title = album_title.replace('/', ' ')

        # 拼接本地文件夹路径，并检查路径是否存在，防止重复下载  
        path = BASE_FOLDER_PATH + "/" + album_title  
        if os.path.exists(path):  
            return True  
    
        # 新建存放当前专辑的图片文件夹  
        checkDir(path)
    
        time.sleep(5)
        # photos_path是第一张图片所在页面，并且包括页码
        #   根据页码，组成页面，并在一个页面中，循环下载
        page_num = 0
        c = preDownloadPage(photos_path.get('href'))
        soupPage = BeautifulSoup(c, 'html.parser', from_encoding='utf-8')
        #pages_blocks = soupPage.findAll('center')
        #for pages_blockItr in pages_blocks:
        pages_block = soupPage.find('div', id='pages')
            
        pages = pages_block.findAll('a', href=re.compile(r'http://www.meituri.com/a/'))
        if pages == None:
            continue
        page_num = int(pages[len(pages)-2].get_text())
        print('%s%s%s' % (soupPage.title, '页数：', str(page_num)))
        
        for i in range(1, page_num+1):
            if i == 1:
                #第一页就顺便处理了
                downloadPage(soupPage, path)
            else:
                # 以后的调用
                path_url = photos_path.get('href') + str(i) + '.html'
                nextPageContent = preDownloadPage(path_url)
                #nextPageContent = downloadUrl(path_url)
                nextPageCoup = BeautifulSoup(nextPageContent, 'html.parser', from_encoding='utf-8')
                downloadPage(nextPageCoup, path)

# 模拟滚动
def preDownloadPage(url):
    # 操作屏幕滚动
    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1)")
    
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(profile)

    driver.get(url)
    time.sleep(3)
    js="document.body.scrollTop=1000"
    driver.execute_script(js)
    time.sleep(4)
    return driver.page_source
    
# 按当前页面下载            
def downloadPage(pageSoup, path):

    # 获取存有img节点  
    img_nodes = pageSoup.find('div', class_='content').findAll('img', class_='tupian_img')
    for img_node in img_nodes:
        pic_url = img_node.get('src')
        # 调用getPicName()获取图片名称  
        pic_name = getPicName(pic_url).encode('utf-8')
        print('%s%s%s' % (pic_name, ',', pic_url))
        
        try:  
            # 访问图片地址，获取数据  
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
            req = urllib2.Request(pic_url, headers=headers) 
            content = urllib2.urlopen(req).read()  
            # 保存图片到本地  
            with open(path + '/' + pic_name, 'wb') as code:  
                code.write(content)  
            print '  -> ' + pic_name + " download success"  
        #捕获异常  
        except Exception, e:  
            print "exception:"+e.message  
            continue 
    return True
    
    
# 获取相册名称
def getPicName(picUrl) :  
    # 截取地址中最后一个/后面的字符，即图片名
    picName = os.path.basename(picUrl)  
    if '.jpg' in picName:  
        return picName  
    return 'error.jpg'

# 主函数
if __name__ == "__main__":
    # 检查本地下载路径是否存在
    checkDir(BASE_FOLDER_PATH)
    # 循环访问
    for i in range(1, MAX_PAGE_NUM+1):
        if i == 1:
            page_url = PORT_HOST
        # 拼接页地址，fix me
        else:
            page_url = PORT_HOST + str(i) +'.html'
        # 保存当前页码，供查看下载进度
        with open('cur_page.txt', 'w') as fpage:  
            fpage.write(str(i))  
        # 以页为单位进行下载
        downloadHomePage(page_url)       
