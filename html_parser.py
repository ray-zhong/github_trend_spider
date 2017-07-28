from bs4 import BeautifulSoup
import re


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find('div', class_='col-md-3').find_all('a', href=re.compile(r'https://github.com/trending/.+$'))
        for link in links:
            new_url = link['href']
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        repos = []
        lang = page_url[page_url.rindex("/")+1:]
        if lang == 'trending':
            lang = 'all'
        res_data['lang'] = lang
        repo_nodes = soup.find('ol', class_='repo-list').find_all('li')
        for repo_node in repo_nodes:
            repos_data = {}
            title = repo_node.a.get_text(strip=True)
            title_arr = title.split('/')
            repos_data['owner'] = title_arr[0].strip()
            repos_data['name'] = title_arr[1].strip()
            repos_data['summary'] = repo_node.p.get_text(strip=True) if repo_node.p else ' '
            bottom_node = repo_node.select('div.text-gray.mt-2')
            if bottom_node[0].find('span', class_='repo-language-color') is not None:
                repos_data['language'] = bottom_node[0].find('span', class_='repo-language-color').find_next_sibling("span").get_text(strip=True)
                color_str = bottom_node[0].find('span', class_='repo-language-color')['style']
                repos_data['color'] = color_str[color_str.index('#'):-1]
            else:
                repos_data['language'] = 'Unknown'
                repos_data['color'] = '#fff'
            if bottom_node[0].a is not None:
                repos_data['stars'] = bottom_node[0].a.get_text(strip=True)
            if bottom_node[0].find('span', class_='float-sm-right') is not None:
                repos_data['stars_today'] = bottom_node[0].find('span', class_='float-sm-right').get_text(strip=True)
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
