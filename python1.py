#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
人生苦短,我用Python
'''
###以此怀念###
import re
import os
import time
import lxml
import random
import requests
import multiprocessing
from bs4 import BeautifulSoup

###################### 全局变量 ##############################
url = 'https://www.mzitu.com/all'  # 需要爬取的网页地址
ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
      'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'
      ]
Usera = random.choice(ua)  # 随机一个ua
headers = {'User-Agent': Usera,
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding': 'gzip',
           "Referer": "https://www.mzitu.com/all"}  # 创建头部信息


##############################################################

def get(url):  # 发送网络请求
    a = requests.get(url, headers=headers)
    html = a.text
    return html


def main():
    soup = BeautifulSoup(get(url), 'lxml')  # 解析爬取网址
    all_url = soup.find('div', class_='all').find_all('a')  # 过滤数据到all_url列表中
    for mulu in all_url:  # 遍历url列表
        if mulu.get_text() == '早期图片':
            continue
        else:
            dict_mulu = {
                'title': mulu.get_text(),
                'link': mulu.get('href'),
                'ID': re.findall('\d+', mulu.get('href'))
            }  # 过滤出字典

        mulu_id = dict_mulu['ID']  # 读字典ID开始过滤已下载内容
        with open('已下载列表.txt', 'a+') as file:
            file.seek(0)
            txt = file.read().splitlines()
            aa = list(txt)
            wancheng = [True for a in mulu_id if a not in aa]
            if wancheng:
                mulu_url = dict_mulu['link']
                print('开始下载当前图帖链接:', mulu_url)
                soup2 = BeautifulSoup(get(mulu_url), 'lxml')  # 解析字典中的目录地址
                img_mulu = soup2.find("div", {"class": "main-image"}).find("img")['src']  # 匹配图片地址
                page = soup2.find_all("span")[9]  # 取图贴页数
                max_page = page.get_text()
                os.chdir(img_dir)
                new_dir(dict_mulu['title'])
                imgs = []
                for j in range(1, int(max_page) + 1):
                    pages = str(j).zfill(2)
                    img_url = img_mulu[0:-6] + pages + '.jpg'  # 图片链接
                    # 图片名
                    img_name = dict_mulu['title'] + str(j)
                    img = (img_name, img_url)
                    imgs.append(img)
                cores = multiprocessing.cpu_count()
                p = multiprocessing.Pool(processes=cores)
                p.map(down, imgs)
                p.close()
                p.join()
                get_end(str(dict_mulu['ID']))
            else:
                print(str(dict_mulu['ID']) + '正在跳过已下载内容....')


def down(imgs):
    name = imgs[0]
    image = imgs[1]
    f = open(name + '.jpg', 'wb+')
    img = requests.get(image, headers=headers)
    if str(img) == '<Response [200]>':
        print('下载图片...', name, image)
        f.write(img.content)
    f.close()


def new_dir(name):  # 创建文件夹
    if os.path.exists(name):
        print('"%s"  文件夹已存在' % name)
        os.chdir(name)
    else:
        print('创建文件夹: {}'.format(name))
        os.mkdir(name)
        os.chdir(name)


def get_end(id):  # 写出已下载列表
    os.chdir(img_dir)
    ftxt = open('已下载列表.txt', 'a+')
    txt = id.strip("[']")
    ftxt.write(txt + '\n')
    ftxt.close()


if __name__ == '__main__':
    print("####################################################################")
    print("# 开始执行脚本...                                                   #")
    print("# 支持断点续传,重新执行脚本即可...                                   #")
    print("#                                              by白衬衫  2020.1.16 #")
    print("####################################################################")
    img_dir = 'H:\\untitled1\\学习资料'  # 设定存储爬取图片的路径
    new_dir(img_dir)
    yanshi = 0.3  # 设定抓取图片延时(0.3秒)
    main()

############################## End 2019.11.30 ######################################