import requests
import shutil
import os
import threading
import random

class Caoliu:
    def __init__(self):
        self.heaer_data = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': '',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.t66y.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36',
        }

        if "torrent_dir" not in os.listdir(os.getcwd()):
            os.mkdir('torrent_dir')
        else:
            shutil.rmtree('torrent_dir') #清空种子文件夹
            os.mkdir('torrent_dir')

    def detail_page(self,url):
        try:
            session = HTMLSession()
            data = session.get(url)
            content = data.html.find('a[target=_blank]')[-1] # 获取种子下载页面链接
            url = content.text
            if 'link.php' in url:
                self.download_page(url)
        except:
            print("detail page:" + url + " get failed")

    def download_page(self, url): #下载种子
        header_data2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'rmdown.com',
            'Referer': url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36'
        }
        try:
            session = HTMLSession()
            data = session.get(url)
            ref = data.html.find('input[name=ref]',first=True).attrs['value']
            reff = data.html.find('input[name=reff]',first=True).attrs['value']
            r = requests.get("http://www.rmdown.com/download.php?reff=" + reff + "&ref=" + ref) # 获取种子下载链接
            with open("torrent_dir\\" + ref + str(random.randint(1, 100)) + ".torrent", "wb") as f:
                f.write(r.content)
        except:
            print("download page " + url + " failed")

    def index_page(self,fid=2,page=1):

            tmp_url = "http://www.t66y.com/thread0806.php?fid=2" + str(fid) + "&search=&page=" + str(page)
            session = HTMLSession()
            data = session.get(tmp_url)
            html = data.html.find("h3 > a")
            base_url = "http://t66y.com/"
            for i in html:
                url = base_url + i.attrs["href"]
                self.detail_page(url)

            print("index page " + str(offset) + " get failed")

    def start(self,downloadtype,page_start=1,page_end=10,max_thread_num=10):
        type_dict = {
            "yazhouwuma":2,
            "yazhouyouma":15,
            "oumeiyuanchuang":4,
            "dongmanyuanchuang":5,
            "guochanyuanchuang":25,
            "zhongziyuanchuang":26,
        }

        if downloadtype in type_dict.keys():
            fid = type_dict[downloadtype]
        else:
            raise ValueError("type wrong!")
        max_thread_num = min(page_end - page_start + 1,max_thread_num)
        thread_list = []
        for i in range(page_start,page_end + 1):
            thread_list.append(threading.Thread(target=self.index_page,args=(fid,i,)))

        for t in range(len(thread_list)):
            thread_list[t].start()
            print("No." + str(t) + " thread start")
            while True:
                if len(threading.enumerate()) < max_thread_num: # 当前正在运行的线程列表数量小于最大运行线程数，则退出循环，继续运行下一个新线程，否则，等待
                    break

if __name__ == "__main__":
    c = Caoliu()
    c.start(downloadtype="yazhouwuma",page_start=1,page_end=10,max_thread_num=50)