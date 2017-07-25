import re

url = re.compile(r'https://github.com/trending/\w*$')

ifmatch = url.match('https://github.com/trending/python')

print(ifmatch)
