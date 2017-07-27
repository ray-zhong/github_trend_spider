# coding:utf-8
import threading
import queue
import html_downloader
import html_parser
import html_outputer


class SpiderMain(object):
    def __init__(self, tp, root_url):
        self.tp = tp
        self.root_url = root_url
        self.collect_urls = set()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, new_url):
        count = 1
        if count > 20:
            return
        print('count:%d url:%s' % (count, new_url))
        try:
            html_cont = self.downloader.download(new_url)
            print('download')
            new_data = self.parser.parse(new_url, html_cont)
            print('parser')
            self.outputer.collect_data(new_data)
            count += 1
        except Exception as e:
            print(e)
            print('download fail')

    def work(self):
        self.collect_urls.add(self.root_url)
        html_cont = self.downloader.download(root_url)
        print('download')
        new_urls, new_data = self.parser.parse_first(root_url, html_cont)
        for url in new_urls:
            if url is None or url in self.collect_urls:
                continue
            self.collect_urls.add(url)
            self.tp.add_job(self.craw, url)
        print('parser')
        self.outputer.collect_data(new_data)
        self.tp.wait_all_complete()


class ThreadPool(object):
    def __init__(self, maxsize):
        self.url_queue = queue.Queue()
        self.threads = []
        self.maxsize = maxsize
        for i in range(maxsize):
            self.threads.append(Work(self.url_queue))

    def add_job(self, func, new_url):
        self.url_queue.put((func, new_url))

    def wait_all_complete(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.join()


class Work(threading.Thread):
    def __init__(self, url_queue, timeout=2):
        super(Work, self).__init__()
        self.url_queue = url_queue
        self.timeout = timeout
        self.start()

    def run(self):
        while True:
            try:
                func, url = self.url_queue.get(timeout=self.timeout)
                func(url)
                self.url_queue.task_done()
            except Exception as e:
                print(e)
                break


if __name__ == '__main__':
    root_url = 'https://github.com/trending'
    tp = ThreadPool(10)
    spider = SpiderMain(tp, root_url)
    spider.work()
    spider.outputer.output_html()
