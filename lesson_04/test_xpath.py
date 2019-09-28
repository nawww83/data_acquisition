from lxml import html
import requests
from pprint import pprint as pp
import datetime

ml = 'https://mail.ru/'

# Это столько браузеров?..
_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'
ua = {'User-agent': _agent}

inline = 'div[contains(@class, "news-item_inline")]'
main = 'div[contains(@class, "news-item_main")]'

root = html.fromstring( requests.get(ml, headers = ua).text )
links = root.xpath('//' + inline + '//a[last()]/@href | //' + main + '//a[last()]/@href')
labels = root.xpath('//' + inline + '//a[last()]/text() | //' + main + '//a[last()]/text()')

dt = str(datetime.datetime.now())

labels = list(map(lambda x: x.strip().replace('\xa0', ' '), labels))

news = [{'source':ml, 'name':labels[i], 'link':links[i], 'date':dt} for i in range(len(labels))]

for _n in news:
    print(_n)
