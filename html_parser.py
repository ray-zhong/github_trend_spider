from bs4 import BeautifulSoup
import re


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find('div', class_='col-md-3').find_all('a', href=re.compile(r'https://github.com/trending/.*$'))
        for link in links:
            new_url = link['href']
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        repos = []
        res_data['url'] = page_url
        repo_nodes = soup.find('ol', class_='repo-list').find_all('li')
        for repo_node in repo_nodes:
            repos_data = {}
            repos_data['title'] = repo_node.a.get_text().strip('\n')
            repos.append(repos_data)
        res_data['data'] = repos
        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup)
        return new_data

    def parse_first(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
