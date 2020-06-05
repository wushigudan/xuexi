#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
import sys
import re


def Download(href,header,title,path):
    if (os.path.exists(path+title.strip()) and len(os.listdir(path+title.strip())) >= 344):
        print("done" + title)
        return 1
    print("开始爬取" + title)
    os.makedirs(path+title.strip())
    os.chdir(path+title.strip())

    try:
        pic = 'https://t66y.com/' + href
        html = requests.get(pic, headers=header)
        html.encoding = 'GBK'
        bs = BeautifulSoup(html.text, 'html.parser')
        res = bs.find_all('div', class_="tpc_content do_not_catch")
        src = re.findall('<input.*?src="(.*?)"', str(res))
        for i in src:
            print(i)
            html = requests.get(i, headers=header)
            file_name = i.split(r'/')[-1]
            f = open(file_name, 'wb')
            f.write(html.content)
            f.close()
    except requests.exceptions.MissingSchema as e:
        print(e)
    except requests.exceptions.ConnectionError as w:
        print(w)

if __name__=='__main__':
    header = {
              'referer': 'https://t66y.com/thread0806.php?fid=8',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
              }

    all_url = 'https://t66y.com/thread0806.php?fid=8'
    pool = Pool(5)
    start_html = requests.get(all_url, headers=header)
    start_html.encoding = 'GBK'
    path = 'e:/meinv/'
    #print(start_html.text)
    for n in range(2, 344):
        ul = all_url + '&search=&page=' + str(n)
        start_html = requests.get(ul, headers=header)
        start_html.encoding = 'GBK'
        href = re.findall('<a.*?href="(.*?)".*?target="_blank".*?>(.*?)</a>', start_html.text)
        for i in href:
            title = i[1]
            if (title != ''):
                href = i[0]
                pool.apply_async(Download, args=(href, header, title, path))
    pool.close()
    pool.join()
    print('所有图片已下完')
