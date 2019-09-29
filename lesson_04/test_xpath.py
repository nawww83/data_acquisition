from lxml import html
import requests
from pprint import pprint as pp
import datetime

# Поисковик mail.ru
ml = 'https://mail.ru'

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

pp('--------------------------')
for _n in news:
    pp(_n)


# Новостной источник lenta.ru
# Вспомогательные функции для преобразования строки с датой и временем для передачи в конструктор datetime()
def getMonthNumber(s):
    if s.find('сентябр'):
        return 9
    if s.find('октябр'):
        return 10
    if s.find('ноябр'):
        return 11
    if s.find('декабр'):
        return 12
    if s.find('январ'):
        return 1
    if s.find('феврал'):
        return 2
    if s.find('март'):
        return 3
    if s.find('апрел'):
        return 4
    if s.find('май') or s.find('мая'):
        return 5
    if s.find('июн'):
        return 6
    if s.find('июл'):
        return 7
    if s.find('август'):
        return 8

    return -1

def getDay(s):
    pos = s.find(',')
    if pos > -1:
        return int(s[pos+1:pos+4])
    else:
        return -1

def getHours(s):
    return int(s[0:2])

def getMinutes(s):
    return int(s[3:5])

lnt = 'https://lenta.ru'
lenta = 'div[@class="span4"]/div[@class="item"]'

root = html.fromstring( requests.get(lnt, headers = ua).text )
links = root.xpath('//' + lenta + '//a/@href')
labels = root.xpath('//' + lenta + '//a/text()')
dt = root.xpath('//' + lenta + '//a/time/@datetime')


labels = list(map(lambda x: x.strip().replace('\xa0', ' '), labels))
links = [lnt + l for l in links]
dt = [d.strip() for d in dt]
dt = [str(datetime.datetime(int(d[-4:]), getMonthNumber(d), getDay(d), getHours(d), getMinutes(d))) for d in dt]

news = [{'source':lnt, 'name':labels[i], 'link':links[i], 'date':dt[i]} for i in range(len(labels))]

pp('--------------------------')
for _n in news:
    pp(_n)

