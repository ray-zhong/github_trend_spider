# coding:utf-8
from concurrent.futures import ThreadPoolExecutor
import time
import html_downloader
import html_parser
import html_outputer


class SpiderMain(object):
    def __init__(self, root_url):
        self.root_url = root_url
        self.collect_urls = set()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, new_url):
        print('parser %s' % new_url)
        try:
            html_cont = self.downloader.download(new_url)
            new_data = self.parser.parse(new_url, html_cont)
            self.outputer.collect_data(new_data)
            print('ok %s' % new_url)
        except Exception:
            print('%s no trend' % new_url)

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.collect_urls:
            self.collect_urls.add(url)

    def add_new_urls(self, urls):
        print('total: %d' % len(urls))
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def work(self):
        print(root_url)
        html_cont = self.downloader.download(root_url)
        new_urls, new_data = self.parser.parse_first(root_url, html_cont)
        self.add_new_urls(new_urls)
        self.outputer.collect_data(new_data)
        print('ok %s' % root_url)
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.craw, self.collect_urls)


if __name__ == '__main__':
    start = time.time()
    root_url = 'https://github.com/trending'
    spider = SpiderMain(root_url)
    spider.work()
    spider.outputer.save_data()
    end = time.time()
    print("cost time: %s" % (end-start))
